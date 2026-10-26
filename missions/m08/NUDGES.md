# Nudges (open only if stuck)

1. Subtract the largest score before `math.exp`: the result is the same and nothing overflows.

2. For the mask, set scores of later tokens (j > i) to `float('-inf')` before the softmax.

## The approach, in plain English (open last)

1. Write softmax: subtract the largest score from every score, take exponentials, and divide by their sum.
2. In attention, for each query compute its dot product with every key and divide by the square root of the vector length.
3. With the mask on, replace the scores of later tokens with minus infinity before the softmax; their weight becomes zero.
4. Each output is the weighted sum of the value vectors, column by column.
5. most_attended returns the index of the largest weight in each row.
