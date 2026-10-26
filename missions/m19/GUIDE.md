# Self-study guide: Will the fine-tune fit on a free GPU?

Clients often want to fine-tune before anyone has checked whether the model fits the hardware they can get. A sizing helper with honest rules of thumb answers that in minutes, and the answer often decides the whole approach: full fine-tuning, LoRA, QLoRA, or not fine-tuning at all. Free GPUs such as Kaggle's or Colab's make the question very practical.

## Revise first (in the course)

- GPU memory sizing formulas
- LoRA trainable parameters and QLoRA memory
- when fine-tuning beats retrieval, and when it does not

## Read the email like an FDE

The CTO gives you the target hardware (a 16 GB T4) and points you to a sizing sheet with the rules of thumb. The acceptance criteria repeat them: bytes per parameter for each method, plus a fixed overhead for LoRA and QLoRA, with one gigabyte meaning 10^9 bytes, so billions of parameters times bytes per parameter gives gigabytes directly. The order 'full, LoRA, QLoRA' matters: the plan picks the first method that fits, because fuller methods are preferred when the memory is there. An unknown method must be refused, not guessed.

## Questions to ask the client first

- **How long are your transcripts, and what sequence length will training use?** Activation memory grows with sequence length; the rules of thumb assume a modest one.
- **Is the free GPU's weekly allowance enough for the training runs you plan?** Kaggle gives about 30 GPU hours a week; several runs and evaluations must fit inside it.
- **Have you measured how well retrieval alone answers your questions?** Fine-tuning is costly to maintain; retrieval may already meet the target.

## How each criterion is checked

1. **Full fine-tuning estimate:** vram_gb for a 7-billion-parameter model with full fine-tuning must follow the sheet's bytes per parameter.
2. **LoRA and QLoRA estimates:** vram_gb for LoRA and QLoRA must add the fixed overhead and round to one decimal, including a small model.
3. **An unknown method is refused:** An unknown method must raise ValueError.
4. **LoRA trains a tiny share of the model:** lora_params for a typical model shape must give the expected number of trainable parameters.
5. **The right method for a free 16 GB GPU:** plan must choose the first method that fits a 16 GB GPU for a small, a 7-billion and a 13-billion model.
6. **Some models do not fit at all:** plan must return 'none' for a model too large for any method on that GPU.

## How to work it

1. Read the email twice: once for the story, then with a pen, underlining every number, every rule and every 'must' or 'never'. Those words become the checks.
2. Turn the acceptance criteria into your own checklist, one line per criterion, and decide how you will see each one working before you build it.
3. Open the data files and the provided code before writing anything. Real files hold the awkward cases (blanks, duplicates, odd formats) the checks use.
4. Build the smallest piece that runs, print its result, and compare it with what you worked out by hand.
5. Add the next rule, run again, and keep each business rule in one obvious, named place.
6. Press Check only when your own prints agree with the criteria, then read each failing criterion's message before you change any code.
7. When it passes, read your code as the client's reviewer would, then compare it with the debrief.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| Estimates are a billion times too large | Parameters were converted to units and then to bytes twice. | Billions of parameters times bytes per parameter is already gigabytes. |
| QLoRA for 1.5B gives 2.75 | The result was not rounded. | Round to one decimal as the criteria say. |
| plan picks QLoRA when LoRA fits | The methods were tried from the smallest. | Try them in the order full, LoRA, QLoRA. |
| A model that exactly fills the GPU is rejected | Fits was tested with less-than. | An estimate equal to the GPU's memory fits. |

## Test yourself before you check

- Work the 7-billion estimates for all three methods by hand.
- Compute what share of a 7-billion model LoRA trains with the example shape.
- Run plan for model sizes from 0.5 to 70 billion and look at where the method changes.
- Try a misspelled method name.

## What a senior reviewer also looks for

A reviewer would ask for the rules' source and their limits to be stated next to the numbers, because rules of thumb ignore sequence length, batch size and optimiser choices. They would want the plan to explain its choice ('LoRA: 16.0 GB of 16 GB') so the team does not start a run that fails after an hour.

## Stretch goal

Add a safety margin argument (for example 10 percent of the GPU kept free) and show how it changes the plan for the 7-billion model.
