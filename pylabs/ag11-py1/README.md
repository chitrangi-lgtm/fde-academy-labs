# Where did the money go? Model cost by feature

**Libraries:** pandas · **Level:** Intermediate · about 30 minutes

The finance team saw last week's model bill jump on one day. You have a week of usage by feature and model, and the price table (example prices per million tokens; cached input tokens are cheaper). Find what each feature cost, the spike day, the feature behind it, and the share of input tokens served from the cache.

Write your code in `lab.py`, then run `python tools/fde_check.py ag11-py1` from the kit's folder.

<details><summary>Hints</summary>

1. Cost of a row: uncached input x input price + cached x cached price + output x output price, all divided by 1,000,000.
2. `calls.apply(fn, axis=1)` computes it row by row; then `groupby('feature')['cost'].sum()`.
3. Spike: `calls.groupby('day')['cost'].sum().idxmax()`, then filter that day and take the feature with the highest cost.
</details>

## Why it matters

Tag every model call with its feature and you can answer a finance question in minutes. Here one feature on one day, on the most expensive model with almost no caching, explains the whole spike.
