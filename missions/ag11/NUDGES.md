# Nudges (open only if stuck)

1. Accumulate cost per feature, per day and per (day, feature) in one pass with dictionaries.

2. Nearest-rank p95: sort the step's latencies and take index ceil(0.95 * n) - 1.

## The approach, in plain English (open last)

1. In cost, split the input tokens into uncached and cached, price each with its own rate, add output, and divide by a million.
2. In report, go through the calls once and add each call's cost to its feature, its day and its day-and-feature pair, and collect latencies per step.
3. The spike day is the day with the highest cost; the spike feature is the feature with the highest cost on that day.
4. The cache hit rate is cached input tokens over all input tokens. Apply nearest-rank p95 to each step's latencies.
