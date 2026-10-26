"""Builds 15_finetune_lora.ipynb (and 15_finetune_lora_check.py, the same code cells as a script that CI or a GPU box can run).

    python build_finetune_notebook.py

Edit the cells here, not in the notebook, so the notebook and the tested script never drift apart.
"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CELLS = [
("md", r"""# Lab 15: Fine-tune a small open model with LoRA to extract invoice fields

**Time:** 45–75 minutes on a free GPU · **Level:** Advanced · **Builds on:** FDE Module 19 (open-weights small models), Module 13 (structured outputs), P8 (evaluation)

## The problem

Summit Agro Foods receives invoice details as free text: e-mails, WhatsApp forwards and OCR output. Accounts staff
retype five fields into the ERP: tax ID, invoice number, date, amount and tax rate. Sending every invoice to a hosted
frontier model works, but the client's finance director has two objections:
- **Cost and latency:** about 30,000 invoices a month.
- **Data:** supplier and price data should stay on infrastructure the company controls.

The question for you as the FDE: can a **small open model**, fine-tuned cheaply, extract the fields accurately enough,
and how do you prove it?

## What you'll do

1. Generate a realistic, labelled dataset of invoice texts. The labels are normalised: ISO dates, dollar amounts as
   integers.
2. Measure the base model **before** training. Never skip the baseline.
3. Fine-tune with **LoRA**, which trains small adapter matrices instead of all the weights. That takes minutes on a free
   GPU.
4. Measure again with the same test set and the same metric, then analyse the errors.
5. Save the adapter (a few MB) and write a results card you could put in front of the client.

## Where to run it

- **Google Colab:** File → Upload notebook, then Runtime → Change runtime type → T4 GPU.
- **Kaggle:** Create → New notebook → File → Import notebook. Then, under Settings, choose Accelerator → GPU T4 and turn
  Internet on.
- **Your own NVIDIA GPU:** at least 6 GB of memory, with Python and PyTorch installed.
- **CPU only:** works with a smaller dataset and a short training run, so you can follow the steps. Expect lower scores.
"""),
("md", r"""## 1. Set up

Install the libraries:
- **transformers** loads the model and tokenizer.
- **peft** adds LoRA adapters.
- **accelerate** helps transformers place the model on the GPU.

PyTorch is already installed on Colab and Kaggle. The cell also detects your GPU and picks settings that fit it.
"""),
("code", r"""import importlib.util, subprocess, sys
for pkg in ("transformers", "peft", "accelerate"):
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])

import json, os, random, re, time
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", DEVICE, "|", torch.cuda.get_device_name(0) if DEVICE == "cuda" else "no GPU: using the short CPU settings")
FULL = DEVICE == "cuda"
N_TRAIN, N_TEST, EPOCHS = (480, 100, 2) if FULL else (48, 20, 1)
SEED = 7
random.seed(SEED); torch.manual_seed(SEED)
"""),
("md", r"""## 2. Build a labelled dataset

Real projects start from a few hundred real examples labelled by the client's staff. Here a generator produces invoice
texts in the messy styles accounts teams see, so you can run the lab without client data:
- dates in four formats;
- amounts with "$", "US$" or "USD", with or without thousands separators;
- sales tax written in different ways.

The **labels are normalised**: ISO dates (YYYY-MM-DD), integer dollars and the rate as a number. Normalisation is where a
general model usually slips, and a fine-tuned one learns the house style.

The test set uses **different suppliers** from the training set, so a good score can't come from memorising names.
"""),
("code", r"""REGIONS = ["27", "29", "33", "24", "07", "09"]
TRAIN_SUPPLIERS = ["Harbor Spice Traders", "Highland Packaging", "Ashford Agro Inputs", "Valley Cold Chain", "Kingsport Sugar Co",
                   "Sandbay Spice Mart", "Riverton Label Works", "Stratford Logistics"]
TEST_SUPPLIERS = ["Coastline Pepper House", "Seacliff Mango Exports", "Bramley Bottling", "Oakridge Cartons"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def tax_id(rng):
    # TX, a two-digit region code and a seven-digit registration number
    return "TX" + rng.choice(REGIONS) + "".join(rng.choice("0123456789") for _ in range(7))

def example(rng, suppliers):
    y, m, d = 2026, rng.randint(1, 12), rng.randint(1, 28)
    date_iso = f"{y}-{m:02d}-{d:02d}"
    date_txt = rng.choice([f"{d:02d}/{m:02d}/{y}", f"{d} {MONTHS[m-1]} {y}", date_iso, f"{d:02d}-{MONTHS[m-1]}-{str(y)[2:]}"])
    amount = rng.choice([rng.randint(800, 9999), rng.randint(10000, 99999), rng.randint(100000, 2500000)])
    amt_txt = rng.choice([f"${amount:,}", f"US$ {amount}", f"USD {amount:,}.00", f"{amount:,} USD"])
    rate = rng.choice([5, 10, 12, 20])
    rate_txt = rng.choice([f"Sales tax @{rate}%", f"{rate}% sales tax", f"Sales tax {rate} percent", f"VAT {rate}%"])
    inv = rng.choice(["INV", "SAF", "TI", "BILL"]) + "-" + str(rng.randint(100, 99999))
    g, s = tax_id(rng), rng.choice(suppliers)
    text = rng.choice([
        f"Invoice {inv} from {s} (Tax ID {g}) dated {date_txt}: total {amt_txt} incl. {rate_txt}.",
        f"Pls process bill no {inv} dt {date_txt}, supplier {s}, tax ID: {g}. Amount payable {amt_txt}, {rate_txt}.",
        f"{s} | tax ID {g} | Tax invoice {inv} | {date_txt} | {rate_txt} | Grand total {amt_txt}",
        f"Received invoice {inv} ({date_txt}) for {amt_txt} from {s}. Their sales tax no. is {g}; {rate_txt} applied.",
    ])
    label = {"tax_id": g, "invoice_no": inv, "date": date_iso, "amount_usd": amount, "tax_rate": rate}
    return text, label

rng = random.Random(SEED)
train = [example(rng, TRAIN_SUPPLIERS) for _ in range(N_TRAIN)]
test = [example(rng, TEST_SUPPLIERS) for _ in range(N_TEST)]
print(len(train), "training and", len(test), "test examples. A sample:\n")
for t, l in train[:3]:
    print(t, "\n  ->", json.dumps(l), "\n")
"""),
("md", r"""## 3. Load a small open model and measure the baseline

`SmolLM2-360M-Instruct` is an Apache-2.0 model with 360 million parameters. That is small enough to fine-tune in
minutes and to serve on a CPU. On a GPU the lab loads it in half precision.

The baseline prompt is the one you'd write on day one: the instruction plus a single worked example. The metric is
**field accuracy**: the share of the five fields that exactly match the label, with invalid JSON scoring zero. The cell
also reports how many outputs parse as JSON at all.
"""),
("code", r"""from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "HuggingFaceTB/SmolLM2-360M-Instruct" if FULL else "HuggingFaceTB/SmolLM2-135M-Instruct"
tok = AutoTokenizer.from_pretrained(MODEL)
tok.padding_side = "left"
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float16 if FULL else torch.float32).to(DEVICE)
model.eval()

SYSTEM = ("Extract the invoice fields and reply with JSON only, with keys tax_id, invoice_no, date (YYYY-MM-DD), "
          "amount_usd (integer dollars) and tax_rate (number).")
SHOT_T, SHOT_L = train[0]

def prompt(text, shots=True):
    msgs = [{"role": "system", "content": SYSTEM}]
    if shots:
        msgs += [{"role": "user", "content": SHOT_T}, {"role": "assistant", "content": json.dumps(SHOT_L)}]
    msgs.append({"role": "user", "content": text})
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)

def parse(reply):
    m = re.search(r"\{.*\}", reply, re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None

@torch.no_grad()
def evaluate(rows, shots=True, batch=16):
    fields = ["tax_id", "invoice_no", "date", "amount_usd", "tax_rate"]
    correct = valid = 0
    per_field = {f: 0 for f in fields}
    errors = []
    for i in range(0, len(rows), batch):
        chunk = rows[i:i + batch]
        enc = tok([prompt(t, shots) for t, _ in chunk], return_tensors="pt", padding=True).to(DEVICE)
        out = model.generate(**enc, max_new_tokens=90, do_sample=False, pad_token_id=tok.pad_token_id)
        for (text, label), seq in zip(chunk, out):
            got = parse(tok.decode(seq[enc["input_ids"].shape[1]:], skip_special_tokens=True)) or {}
            valid += bool(got)
            for f in fields:
                ok = str(got.get(f, "")).strip() == str(label[f])
                per_field[f] += ok
                correct += ok
                if not ok and len(errors) < 6:
                    errors.append((f, label[f], got.get(f)))
    n = len(rows)
    return {"field_accuracy": round(correct / (5 * n), 3), "valid_json": round(valid / n, 3),
            "per_field": {f: round(c / n, 3) for f, c in per_field.items()}, "errors": errors}

t0 = time.time()
baseline = evaluate(test)
print(f"baseline ({time.time() - t0:.0f}s):", json.dumps({k: v for k, v in baseline.items() if k != "errors"}, indent=1))
print("examples of baseline errors (field, expected, got):", baseline["errors"])
"""),
("md", r"""## 4. Fine-tune with LoRA

**LoRA** (low-rank adaptation) freezes the model's weights and learns two small matrices beside chosen layers, here
the attention and feed-forward projections. You train well under 5% of the parameters, so training fits on a free GPU
and the result is a small adapter file.

Two details matter:
- **Train only on the answer.** The prompt tokens are masked out of the loss (label −100), so the model learns to
  produce the JSON, not to repeat the question.
- **Train without the worked example.** At serving time you then don't pay for the example's tokens on every invoice.
"""),
("code", r"""from peft import LoraConfig, get_peft_model

if FULL:
    model = model.float()                     # train the adapters in float32 for stability; autocast keeps it fast
lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM",
                  target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"])
model = get_peft_model(model, lora)
model.print_trainable_parameters()

def encode(text, label):
    p = prompt(text, shots=False)
    answer = json.dumps(label) + tok.eos_token
    p_ids = tok(p, add_special_tokens=False)["input_ids"]
    a_ids = tok(answer, add_special_tokens=False)["input_ids"]
    return p_ids + a_ids, [-100] * len(p_ids) + a_ids

data = [encode(t, l) for t, l in train]
opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=2e-4)
BATCH = 8                                     # examples per optimiser step
MICRO = 2                                     # examples per forward pass: 2 fits a shared 6 GB GPU; use 4 or 8 on a 16 GB T4
steps = EPOCHS * (len(data) // BATCH)
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / 10) * max(0.0, 1 - s / max(1, steps)))
model.train()
t0, step = time.time(), 0
for epoch in range(EPOCHS):
    random.Random(epoch).shuffle(data)
    for i in range(0, len(data) - BATCH + 1, BATCH):
        step_loss = 0.0
        for j in range(i, i + BATCH, MICRO):
            chunk = data[j:j + MICRO]
            width = max(len(ids) for ids, _ in chunk)
            ids = torch.tensor([x + [tok.pad_token_id] * (width - len(x)) for x, _ in chunk], device=DEVICE)
            labels = torch.tensor([y + [-100] * (width - len(y)) for _, y in chunk], device=DEVICE)
            mask = torch.tensor([[1] * len(x) + [0] * (width - len(x)) for x, _ in chunk], device=DEVICE)
            with torch.autocast(device_type=DEVICE, dtype=torch.float16, enabled=FULL):
                loss = model(input_ids=ids, attention_mask=mask, labels=labels).loss * MICRO / BATCH
            loss.backward()                   # gradients add up across the micro-batches
            step_loss += loss.item()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); sched.step(); opt.zero_grad()
        step += 1
        if step % 10 == 0 or step == steps:
            print(f"epoch {epoch + 1} step {step}/{steps} loss {step_loss:.3f}")
print(f"training took {time.time() - t0:.0f}s")
model.eval()
"""),
("md", r"""## 5. Measure again and analyse the errors

The same test set and the same metric, but now **without** the worked example, because the fine-tuned model has learned
the format. If the score doesn't beat the baseline clearly, the fine-tune isn't worth deploying.

Look at the remaining errors field by field. Typical leftovers are dates written as "03-Mar-26" or amounts with an
unusual suffix. Those tell you which examples to add in the next round.
"""),
("code", r"""tuned = evaluate(test, shots=False)
print("after fine-tuning:", json.dumps({k: v for k, v in tuned.items() if k != "errors"}, indent=1))
print("remaining errors (field, expected, got):", tuned["errors"])
print(f"\nfield accuracy: {baseline['field_accuracy']:.1%} -> {tuned['field_accuracy']:.1%}; "
      f"valid JSON: {baseline['valid_json']:.0%} -> {tuned['valid_json']:.0%}")
"""),
("md", r"""## 6. Save the adapter and write the results card

The adapter is a few megabytes. In production you load the base model once and attach the adapter, or merge them into
one model for serving with vLLM or Ollama.

The results card is what you take to the client's steering meeting. It holds:
- the task and the data;
- the baseline and the result;
- the cost and time to train;
- the known gaps;
- the recommendation.

Copy the printed JSON into your project notes, or into the course's FDE Module 19 assessment.
"""),
("code", r"""model.save_pretrained("invoice-extractor-lora")
size_mb = sum(os.path.getsize(os.path.join("invoice-extractor-lora", f)) for f in os.listdir("invoice-extractor-lora")) / 1e6
card = {
    "task": "invoice field extraction (5 fields, normalised)", "base_model": MODEL, "method": "LoRA r=16 on attention and MLP projections",
    "train_examples": len(train), "test_examples": len(test), "test_suppliers_unseen": True,
    "baseline_field_accuracy": baseline["field_accuracy"], "tuned_field_accuracy": tuned["field_accuracy"],
    "baseline_valid_json": baseline["valid_json"], "tuned_valid_json": tuned["valid_json"],
    "per_field_after": tuned["per_field"], "adapter_mb": round(size_mb, 1), "device": DEVICE,
    "recommendation": ("pilot behind a human check on low-confidence fields" if tuned["field_accuracy"] >= 0.9
                       else "not ready: add examples for the failing fields and retrain"),
}
print(json.dumps(card, indent=1))
"""),
("md", r"""## Check yourself

1. **Why measure the base model first?** Without a baseline you can't show the fine-tune helped, or that it was worth
   the effort and the operational cost of running your own model.
2. **Why mask the prompt tokens in the labels?** So the loss teaches the model to produce the answer, not to reproduce
   the instruction and the invoice text.
3. **Why use different suppliers in the test set?** To test generalisation. With overlapping suppliers, a model could
   score well by memorising names and tax IDs.
4. **The tuned model scores 96% field accuracy. Is it ready?** Not on its own. Check which fields fail and how badly. A
   wrong amount is worse than a wrong invoice number. Add a validation step: the tax ID checksum and format, a date
   range, and an amount cross-check against the ERP. Also route low-confidence cases to a person.

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `CUDA out of memory` | Micro-batch too large for the GPU | Lower `MICRO` to 1 (keep `BATCH` at 8), or use the 135M model |
| Loss doesn't fall | Learning rate too low, or labels fully masked | Check that labels contain the answer tokens; try a 3e-4 learning rate |
| Valid JSON falls after training | The answer had no end-of-sequence token, so generation runs on | Append `tok.eos_token` to every answer, as `encode` does |
| Great test score, poor on real invoices | Synthetic data is too clean | Add real, labelled examples from the client; keep a held-out real test set |

## Take it further

- Train on 50, 100, 240 and 480 examples and plot accuracy against data size. Where does it stop improving?
- Merge the adapter (`model.merge_and_unload()`), export to GGUF, and serve it with Ollama on a CPU. Time the requests.
- Compare cost per 1,000 invoices for this model on a small CPU server and for a hosted model, using FDE Module 20's
  cost model.
"""),
]


def notebook() -> dict:
    cells = []
    for kind, src in CELLS:
        lines = src.strip("\n").splitlines(keepends=True)
        cell = {"cell_type": "markdown" if kind == "md" else "code", "metadata": {}, "source": lines}
        if kind == "code":
            cell.update(execution_count=None, outputs=[])
        cells.append(cell)
    return {"cells": cells, "metadata": {"accelerator": "GPU", "colab": {"provenance": []},
                                         "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                         "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}


if __name__ == "__main__":
    with open(os.path.join(HERE, "15_finetune_lora.ipynb"), "w", encoding="utf-8") as f:
        json.dump(notebook(), f, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "15_finetune_lora_check.py"), "w", encoding="utf-8") as f:
        f.write('"""Generated from build_finetune_notebook.py: the notebook\'s code cells as one script, for testing on a GPU box."""\n')
        f.write("\n\n".join(src.strip("\n") for kind, src in CELLS if kind == "code") + "\n")
    print("wrote 15_finetune_lora.ipynb and 15_finetune_lora_check.py")
