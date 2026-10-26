# Plan the first sprint within capacity

**From:** Grace Adeyemi, Programme Director, Thornbury Housing Association

We have more ideas than capacity for the first two-week sprint of the tenant-repairs assistant. The backlog with our scores is attached. Please rank it the way our portfolio office does (weighted shortest job first: business value plus time criticality plus risk reduction, divided by effort) and propose the sprint: take the best-ranked item whose prerequisites are already in the sprint and that still fits, and keep going until nothing else fits. Show me the WSJF scores too.

## Done when

- `wsjf(item)` returns (value + time_criticality + risk_reduction) / effort, rounded to 2 places
- `plan(backlog, capacity)` returns item ids in the order they are picked: each time, the highest-WSJF item (ties by id) whose dependencies are already picked and whose effort fits the remaining capacity

## Files

`backlog.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m10
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module m10) records your score.
