"""Generated from build_finetune_notebook.py: the notebook's code cells as one script, for testing on a GPU box."""
import importlib.util, subprocess, sys
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

REGIONS = ["27", "29", "33", "24", "07", "09"]
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

from transformers import AutoModelForCausalLM, AutoTokenizer

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

from peft import LoraConfig, get_peft_model

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

tuned = evaluate(test, shots=False)
print("after fine-tuning:", json.dumps({k: v for k, v in tuned.items() if k != "errors"}, indent=1))
print("remaining errors (field, expected, got):", tuned["errors"])
print(f"\nfield accuracy: {baseline['field_accuracy']:.1%} -> {tuned['field_accuracy']:.1%}; "
      f"valid JSON: {baseline['valid_json']:.0%} -> {tuned['valid_json']:.0%}")

model.save_pretrained("invoice-extractor-lora")
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
