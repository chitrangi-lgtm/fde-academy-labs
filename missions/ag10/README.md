# Score the agent runs the way the board will ask

**From:** Mira Castellanos, Head of Automation, CrestFin Lending Operations

We ran our loan-document agent three times on each of eight tasks. Before the board review I need the numbers they will ask about: overall success rate, the share of tasks it can do at least once in three tries, the share it does reliably every time, average steps, tool-call accuracy and the cost of each success. The run log is attached.

## Done when

- `evaluate(runs)` returns a dict rounded to 3 places: success_rate (successful runs / runs), pass_at_k (tasks with at least one success / tasks), pass_hat_k (tasks where every run succeeded / tasks), avg_steps, tool_accuracy (correct tool calls / all tool calls) and cost_per_success (total cost / successes)
- `unreliable(runs)` returns the sorted tasks that succeeded at least once but not every time

## Files

`runs.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag10
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
