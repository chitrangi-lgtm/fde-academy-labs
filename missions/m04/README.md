# Why did the integration create duplicate orders?

**From:** Marcus Bell, Integration Manager, Fennick Logistics

Our partner's order integration created the same order twice last night and we can't tell why. Attached is the API log, one JSON object per line. I need to know: the error rate for each kind of call, which orders were created more than once, and a retry policy we can give the partner: which status codes are worth retrying, and how long to wait (respect the server's Retry-After when it sends one; otherwise exponential backoff starting at half a second, capped at eight seconds).

## Done when

- `load(path)` returns the log as a list of dicts
- `error_rates(records)` returns {"METHOD /resource": share of 5xx responses, rounded to 3 places}, grouping by method and the first path segment (GET /orders/A-1 counts as "GET /orders")
- `duplicate_creates(records)` returns the sorted order_refs created (201) more than once without an idempotency key
- `retryable(status)` is True only for 408, 429, 500, 502, 503 and 504
- `backoff(attempt, retry_after=None)` returns retry_after when given, else min(8, 0.5 * 2**attempt)

## Files

`api_log.jsonl`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m04
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
