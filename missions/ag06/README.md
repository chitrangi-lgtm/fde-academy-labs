# Check the planning agent's plan

**From:** Ama Boateng, Delivery Manager, Northgate Retail

A planning agent produced the task list for our document-search launch, with durations in days and dependencies. Before we commit to a date, I need the plan checked like a project manager would: which tasks can run in parallel, whether the dependencies contain a cycle (the agent once produced one), and the critical path with its length. Our environment has no graph library, so plain Python please.

## Done when

- `waves(tasks, depends_on)` returns lists of task names that can run together, wave by wave, each sorted
- `has_cycle(tasks, depends_on)` is True when the dependencies can never all be satisfied
- `critical_path(tasks, depends_on)` returns (the longest chain of tasks by total duration, its total days)

## Files

`plan.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag06
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module ag06) records your score.
