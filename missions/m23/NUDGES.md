# Nudges (open only if stuck)

1. Keep three pieces of state: the mode, the consecutive-failure count, and when the breaker opened (from the clock).

2. On each call while open: if the timeout has passed switch to half open and try once; otherwise raise CircuitOpen before calling fn.

## The approach, in plain English (open last)

1. Store the state, the count of failures in a row, and the time the breaker opened, read from the given clock.
2. When a call arrives while open: if the timeout has not passed, raise CircuitOpen before calling anything; if it has, switch to half open and let this call through.
3. Call the function. On success, close the breaker and reset the count, then return the result.
4. On failure, count it; if the breaker was half open or the count reached the threshold, open it and record the time. Re-raise the original error.
