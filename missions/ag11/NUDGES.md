# Nudges (open only if stuck)

1. Accumulate cost per feature, per day and per (day, feature) in one pass with dictionaries.

2. Nearest-rank p95: sort the step's latencies and take index ceil(0.95 * n) - 1.
