# Nudges (open only if stuck)

1. Subtract the largest score before `math.exp`: the result is the same and nothing overflows.

2. For the mask, set scores of later tokens (j > i) to `float('-inf')` before the softmax.
