# The cheapest model setup that meets the latency target

**From:** Dr. Sofia Lindqvist, Product Director, Vireo Health Navigator

Our symptom-navigation assistant handles 40,000 conversations a day. Each request sends a 3,000-token system prompt and policy pack that never changes, 500 tokens of conversation, and gets 300 tokens back. We're choosing between three hosted models (prices and measured latency attached). Prompt caching bills repeated prefix tokens at the cached rate. Tell me what each option costs a month (30 days) with and without caching, and which is cheapest while keeping p95 latency within 1,500 ms.

## Done when

- `request_cost(model, traffic, cache_hit_rate)` returns dollars for one request: uncached input at the input price, the cached share of the fixed prefix at the cached price, output at the output price (prices are per million tokens)
- `monthly_cost(model, traffic, cache_hit_rate)` returns 30 days of requests, rounded to 2 decimals
- `cheapest(models, traffic, slo_ms, cache_hit_rate)` returns the name of the cheapest model whose p95 is within the target, or None

## Files

`models.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m13
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
