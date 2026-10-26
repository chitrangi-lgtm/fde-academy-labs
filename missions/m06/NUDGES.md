# Nudges (open only if stuck)

1. Try every distinct score as a threshold; for each, count tp, fp and fn once and derive the rest.

2. Filter to thresholds that meet the precision floor, then pick the highest recall; break ties with the higher threshold (fewer alerts).
