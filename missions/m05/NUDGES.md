# Nudges (open only if stuck)

1. An `asyncio.Semaphore(limit)` used with `async with` caps how many calls are in progress.

2. `asyncio.wait_for(coro, timeout)` raises TimeoutError and cancels the call; `asyncio.gather` keeps the input order.

## The approach, in plain English (open last)

1. Create one limiter for the whole call, sized by the limit argument.
2. Write an inner coroutine for one supplier: wait for a free slot, then call fetch_quote with a timeout.
3. If the timeout fires, return the supplier with the error 'timeout' instead of letting the exception escape.
4. Start one inner call per supplier and gather them all, which keeps the input order.
5. Return the gathered results as a list.
