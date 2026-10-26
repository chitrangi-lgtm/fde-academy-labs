# Nudges (open only if stuck)

1. Compute both error rates as errors / requests, then check the rollback conditions before anything else.

2. Collect reasons in a list per severity; the first non-empty list decides.

## The approach, in plain English (open last)

1. Compute both error rates as errors over requests, guarding against zero requests.
2. Collect rollback reasons: error increase above the absolute threshold, evaluation drop above its threshold. If there are any, roll back with those reasons, sorted.
3. Otherwise collect hold reasons: requests below the minimum, p95 above the baseline by more than the relative threshold. If there are any, hold with those reasons, sorted.
4. Otherwise promote with no reasons. next_stage returns the first stage above the current one, or 100.
