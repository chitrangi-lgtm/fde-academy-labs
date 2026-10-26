# Find the cost spike and the slow step

**From:** Ama Boateng, Delivery Manager, Northgate Retail

Finance flagged a jump in our agent platform bill, and customers say the shopping assistant is sometimes slow. You have a sample of model-call records. I need cost by feature, the day the bill spiked and the feature behind it, the share of input tokens served from cache, and the p95 latency of each step so we know where time goes.

## Done when

- `cost(record)` returns dollars for one call: (input - cached) x input price + cached x cached price + output x output price, prices per million tokens from PRICES
- `report(records)` returns {"by_feature": {feature: dollars rounded to 2}, "spike_day", "spike_feature", "cache_hit_rate" (rounded to 3), "p95_ms": {step: nearest-rank p95}}

## Files

`calls.json`

`provided.py` holds code the client gives you; the checker runs it before your code.

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag11
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
