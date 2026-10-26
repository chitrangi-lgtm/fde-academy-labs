# Nudges (open only if stuck)

1. Billions of parameters times bytes per parameter gives gigabytes directly (with 1 GB = 1e9 bytes).

2. LoRA adds two matrices, d x r and r x d, to each targeted weight matrix in each layer.

## The approach, in plain English (open last)

1. Keep the sheet's rules as data: bytes per parameter and fixed overhead for each method.
2. In vram_gb, refuse unknown methods, then multiply billions of parameters by bytes per parameter, add the overhead and round to one decimal.
3. In lora_params, count two small matrices per targeted weight matrix per layer, each with d_model × r entries.
4. In plan, try the methods in order and return the first whose estimate is no more than the GPU's memory, or 'none'.
