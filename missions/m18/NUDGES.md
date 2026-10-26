# Nudges (open only if stuck)

1. For MRR, find the 1-based position of the first retrieved document that is in gold; add 1/position (or 0).

2. Nearest-rank: sort, then take the element at index ceil(0.95 * n) - 1.

## The approach, in plain English (open last)

1. Load the evaluation results and spans once.
2. For hit rate, count the questions where the gold set and the first k retrieved documents overlap, and divide.
3. For MRR, find the position (from 1) of the first retrieved document that is gold, add one over that position, or zero, and average.
4. For p95, sort the values and take the one at position ceil(0.95 × n), counting from 1.
5. Group span durations by name and apply p95 to each; for leaks, check every attribute key in lower case.
