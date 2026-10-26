# Choose the alert threshold the fraud team can live with

**From:** Dr. Amara Nwosu, Head of Fraud Analytics, Kestrel Card Services

Our new fraud model gives every payment a score between 0 and 1. My team can investigate a limited number of alerts, and they lose trust when more than one in five alerts is a false alarm. Attached are last month's scores with the true outcome. Tell me, for any threshold, the confusion matrix, precision and recall, how many alerts a day it would produce at our volume of 10,000 payments, and which threshold catches the most fraud while keeping precision at 0.8 or better.

## Done when

- `confusion(threshold)` returns {"tp", "fp", "fn", "tn"}, flagging a payment when score >= threshold
- `precision_recall(threshold)` returns (precision, recall) rounded to 3 places (0.0 when undefined)
- `alerts_per_day(threshold, daily_volume=10000)` returns the share flagged times the volume, as a whole number
- `best_threshold(min_precision=0.8)` returns the score threshold (one of the scores in the file) with the highest recall whose precision is at least min_precision; on a tie, the higher threshold

## Files

`scores.csv`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m06
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module m06) records your score.
