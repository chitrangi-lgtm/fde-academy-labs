# Will the fine-tune fit on a free GPU?

**From:** Kwame Asante, CTO, Tamsin Agritech

We want to fine-tune an open model on our crop-advisory transcripts using free GPUs (a 16 GB T4 on Kaggle or Colab). I need a sizing helper our team can trust: estimated GPU memory for full fine-tuning, LoRA and QLoRA using the rules of thumb in the attached sheet, the number of parameters LoRA actually trains, and the first method in order full, LoRA, QLoRA that fits a given GPU.

## Done when

- `vram_gb(params_billion, method)` follows the sheet: full = 16 bytes per parameter; lora = 2 bytes per parameter + 2 GB; qlora = 0.5 bytes per parameter + 2 GB (1 GB = 1e9 bytes); rounded to 1 decimal; an unknown method raises ValueError
- `lora_params(d_model, layers, r, targets=4)` returns layers x targets x 2 x d_model x r
- `plan(params_billion, gpu_gb)` returns the first of "full", "lora", "qlora" whose estimate fits, else "none"

## Files

`sizing_sheet.txt`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m19
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module m19) records your score.
