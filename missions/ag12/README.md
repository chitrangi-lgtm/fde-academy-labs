# Canary, hold or roll back?

**From:** Tobias Brandt, Payments Platform Owner, CrestFin Lending Operations

We ship a new version of the loan agent to a small share of traffic first. Today someone eyeballs a dashboard and decides. I want the decision written down as code we review: roll back if errors or evaluation quality get clearly worse; hold if there isn't enough traffic yet or latency got worse; otherwise promote to the next stage of the rollout. The thresholds we agreed are attached.

## Done when

- `canary_decision(baseline, canary, rules)` returns (decision, reasons) with decision "rollback", "hold" or "promote" and reasons a sorted list of short strings
- Rollback when the canary's error rate exceeds the baseline's by more than max_error_increase (absolute), or its eval_score is lower by more than max_eval_drop
- Otherwise hold when the canary has fewer than min_requests requests, or its p95 is more than max_latency_increase (relative) above the baseline's
- Otherwise promote, with reasons []. `next_stage(pct)` returns the next of 1, 5, 25, 50, 100 (100 stays 100)

## Files

`rules.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag12
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module ag12) records your score.
