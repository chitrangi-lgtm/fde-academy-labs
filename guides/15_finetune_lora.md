# Lab 15: Fine-tune a small open model with LoRA on a free GPU

**Time:** 45–75 minutes on a free GPU · **Level:** Advanced · **Builds on:** FDE Module 19 (open-weights small models), FDE Module 13 (structured outputs), Professional Practice P8 and P11

## The problem

Summit Agro Foods receives about 30,000 invoice details a month as free text: e-mails, WhatsApp forwards and OCR
output. Accounts staff retype five fields into the ERP: tax ID, invoice number, date, amount and tax rate. A hosted
frontier model could do it, but the finance director objects to the running cost and wants supplier and price data to
stay on infrastructure the company controls.

Your question as the FDE: can a **small open model**, fine-tuned cheaply, extract the fields accurately enough, and how
do you prove it to the client? This lab answers it with evidence: a baseline, a LoRA fine-tune, the same test again and
a results card.

## What you'll learn

- How to build a labelled dataset with normalised labels, and a test set that can't be passed by memorising.
- How to measure a baseline before training, with a clear metric (field accuracy and valid-JSON rate).
- How LoRA trains small adapter matrices instead of the whole model, and why that fits on a free GPU.
- Why prompt tokens are masked out of the loss, and why the model is trained without the worked example.
- How to present the result to a client: what improved, what still fails, and what you recommend.

## Before you start

Open `realtools/notebooks/15_finetune_lora.ipynb` in one of these:

1. **Google Colab:** File → Upload notebook, then Runtime → Change runtime type → T4 GPU.
2. **Kaggle:** Create → New notebook → File → Import notebook; under Settings choose Accelerator → GPU T4 and turn
   Internet on.
3. **Your own NVIDIA GPU** with at least 6 GB of memory, Python and PyTorch.
4. **CPU only:** the notebook switches to a smaller model, 48 training examples and one epoch, so you can follow every
   step. Scores will be much lower; that's expected.

You can also download the notebook from the course's real-tools page. The first cell installs `transformers`, `peft`
and `accelerate` if they're missing.

## Key ideas

**Baseline first.** Before training, the notebook measures the base model with the prompt you'd write on day one: an
instruction plus one worked example. Without this number you can't show the fine-tune was worth it.

**Normalised labels teach the house style.** Invoices write dates four ways and amounts with "$", "US$" or "USD",
with or without thousands separators. The labels are always ISO dates and integer dollars. Normalising is where general models slip, and
where a fine-tuned model gains most.

**A fair test set.** Test invoices come from suppliers that never appear in training, so a high score means the model
learned the pattern, not the names.

**LoRA trains a small adapter.** The base weights are frozen; LoRA adds small matrices (rank 16 here) beside the
attention and feed-forward projections. `print_trainable_parameters()` shows you're training only a few per cent of the
parameters. The saved adapter is a few megabytes.

**Train on the answer only.** The prompt's tokens get the label −100, so the loss ignores them. The model learns to
write the JSON, not to repeat the invoice. Training without the worked example means you don't pay for its tokens on
every invoice at serving time.

## Steps

1. **Set up (cell 1).** Run it and check the device line. On a T4 or similar it says `device: cuda | Tesla T4` and uses
   480 training and 100 test examples for 2 epochs.

2. **Build the dataset (cell 2).** Read the three samples. Each invoice text is followed by its label: notice the date
   format changes but the label is always `YYYY-MM-DD`.

3. **Measure the baseline (cell 3).** This prints field accuracy, the valid-JSON rate and accuracy per field, and a few
   errors as `(field, expected, got)`. The base model usually gets the tax ID and invoice number right, because they're
   copied from the text, and slips on dates and amounts, which need converting.

4. **Fine-tune (cell 4).** Watch the loss fall over the steps; it should drop steeply in the first few dozen steps and
   then level off. On a T4 training takes a few minutes.

5. **Measure again (cell 5).** The same test set, now without the worked example. Compare the final line,
   `field accuracy: X% -> Y%; valid JSON: A% -> B%`. Then read the remaining errors: they show which kinds of example to
   add in the next round.

6. **Save and write the card (cell 6).** The adapter is saved to `invoice-extractor-lora/` and the results card prints as
   JSON, with a recommendation: pilot behind a human check if field accuracy is at least 90%, otherwise add examples and
   retrain.

7. **Try one change.** Pick one: train on 120 examples instead of 480; set `r=4`; or train one epoch. Re-run cells 2–5
   and compare. Write down which change mattered most.

## Check yourself

<details><summary>Why measure the base model with a worked example, but the tuned model without one?</summary>
The baseline should be the best simple prompt you'd write without training, which includes an example. The tuned model
has learned the format, so it doesn't need the example, which also makes every request cheaper.
</details>

<details><summary>Why mask the prompt tokens in the labels?</summary>
So the loss only measures how well the model writes the answer. Otherwise much of the training effort would go into
predicting the invoice text and the instruction, which the model doesn't need to learn.
</details>

<details><summary>The tuned model reaches 96% field accuracy. Is it ready for production?</summary>
Not by itself. Check which fields fail: a wrong amount matters more than a wrong invoice number. Add validation in code
(tax ID format and region code, a sensible date range, an amount cross-check against the purchase order) and route doubtful
cases to a person. Then test on real, labelled client invoices.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `CUDA out of memory` | The micro-batch is too large for your GPU | Lower `MICRO` to 1 (keep `BATCH` at 8), or use the 135M model |
| No GPU found on Colab or Kaggle | The runtime is CPU only | Change the runtime or accelerator to a T4 GPU and restart |
| The loss doesn't fall | The labels are fully masked or the learning rate is too low | Check that the labels contain the answer tokens; try a learning rate of 3e-4 |
| Valid JSON gets worse after training | The answers have no end-of-sequence token, so generation runs on | Append `tok.eos_token` to every answer, as `encode` does |
| A great test score but poor results on real invoices | Synthetic data is cleaner than reality | Add real labelled examples and keep a held-out real test set |

## Take it further

- Train on 50, 100, 240 and 480 examples and plot accuracy against data size. Where does it stop improving?
- Merge the adapter with `model.merge_and_unload()`, convert it to GGUF and serve it with Ollama on a CPU. Time it.
- Compare the cost per 1,000 invoices for this model on a small server and for a hosted model, using FDE Module 20's
  cost model.

## In a real client project

- Start from a few hundred real invoices labelled by the client's accounts staff, with a written labelling guide.
- Keep the test set fixed between versions so results are comparable, and record the base model, data and settings.
- Monitor production accuracy with a sample checked by people each week, and retrain when it drifts.
