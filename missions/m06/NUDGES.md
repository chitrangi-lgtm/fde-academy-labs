# Nudges (open only if stuck)

1. Try every distinct score as a threshold; for each, count tp, fp and fn once and derive the rest.

2. Filter to thresholds that meet the precision floor, then pick the highest recall; break ties with the higher threshold (fewer alerts).

## The approach, in plain English (open last)

1. Read the scores and outcomes once into a list of pairs.
2. For confusion, loop over the pairs and put each into one of the four counts, flagging at or above the threshold.
3. Derive precision and recall from the counts, returning 0.0 when the denominator is zero.
4. For alerts a day, divide the number flagged by the number of rows and multiply by the volume.
5. For the best threshold, try every distinct score, keep those meeting the precision floor, and pick the highest recall, breaking ties with the higher threshold.
