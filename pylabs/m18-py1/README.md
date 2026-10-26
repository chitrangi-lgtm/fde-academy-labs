# Find the slow span: p95 latency from traces

**Libraries:** pandas, matplotlib · **Level:** Intermediate · about 30 minutes

Users of a claims assistant say it is 'sometimes slow'. You have 24 traces, each with five spans. Find each span's 95th-percentile latency, which span dominates, and which traces breached the 2.5-second budget. Draw a chart the client's operations lead can read in ten seconds.

Write your code in `lab.py`, then run `python tools/fde_check.py m18-py1` from the kit's folder.

<details><summary>Hints</summary>

1. `traces.groupby('span')['ms'].quantile(0.95)` gives every span's p95 at once.
2. Total per trace: `traces.groupby('trace_id')['ms'].sum()`; keep the ids over 2500.
3. Look at the retrieve span of the two slow traces: the p95 alone hides that the cause is two outliers, not the model.
</details>

## Why it matters

Percentiles per span turn 'sometimes slow' into a named cause. Then look at the outlier traces themselves: here retrieval stalls in two traces, a different fix from making generation faster.
