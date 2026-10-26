# Nudges (open only if stuck)

1. For MRR, find the 1-based position of the first retrieved document that is in gold; add 1/position (or 0).

2. Nearest-rank: sort, then take the element at index ceil(0.95 * n) - 1.
