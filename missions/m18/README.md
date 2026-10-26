# Find the retrieval regression and the trace leak

**From:** Ayaan Kapoor, ML Platform Lead, Lumen Bank

Since Tuesday's index rebuild, our assistant's answers feel worse, and our privacy team found that some traces contain customer prompts. Attached are the retrieval evaluation results before and after the rebuild, and a sample of spans. Please give me hit rate at 3 and mean reciprocal rank for both runs so we can see the regression, the p95 latency per span name, and the ids of spans that leak prompt or completion text.

## Done when

- `hit_rate(results, k=3)`: share of questions with any gold document in the top k retrieved, rounded to 3
- `mrr(results)`: mean of 1/rank of the first gold document (0 when none), rounded to 3
- `p95(values)`: the nearest-rank 95th percentile (sort, take the value at position ceil(0.95 n))
- `p95_by_span(spans)`: {span name: p95 of its duration_ms}
- `leaks(spans)`: sorted span ids with any attribute key containing 'prompt' or 'completion'

## Files

`eval.json`, `spans.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m18
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module m18) records your score.
