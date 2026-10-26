# Nudges (open only if stuck)

1. Group the runs by task first: pass@k asks 'any success', pass^k asks 'all successes'.

2. Cost per success divides the cost of every run (failures cost money too) by the number of successes.

## The approach, in plain English (open last)

1. Group the runs by task, keeping each run's success.
2. Success rate: successes over runs. pass at k: tasks with any success over tasks. pass hat k: tasks with all successes over tasks.
3. Average steps over runs; tool accuracy as total correct calls over total calls.
4. Cost per success: total cost of all runs over the number of successes.
5. unreliable: tasks with some successes but not all, sorted.
