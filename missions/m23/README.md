# A circuit breaker that survives the chaos drill

**From:** Fatima Zahra, Site Reliability Lead, Albion Claims (capstone client)

In Friday's chaos drill we'll make the policy service fail. Last time, our assistant kept hammering it and made the outage worse. Please put a circuit breaker in front of the call: after three failures in a row, stop calling for 30 seconds and fail fast; then let one trial call through; if it works, go back to normal, if not, wait another 30 seconds. The drill uses a fake clock, so take the time from the clock you're given.

## Done when

- `CircuitBreaker(failure_threshold=3, reset_timeout=30, clock=time.monotonic)` with a `state` attribute: "closed", "open" or "half_open"
- `call(fn)` returns fn()'s result; failures are counted in a row and reset by a success
- After failure_threshold failures it opens: calls raise CircuitOpen without calling fn
- After reset_timeout (by the clock) one trial call is allowed (half open): success closes it, failure reopens it for another reset_timeout

## Files

none

`provided.py` holds code the client gives you; the checker runs it before your code.

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m23
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
