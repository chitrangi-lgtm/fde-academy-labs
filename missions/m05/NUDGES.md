# Nudges (open only if stuck)

1. An `asyncio.Semaphore(limit)` used with `async with` caps how many calls are in progress.

2. `asyncio.wait_for(coro, timeout)` raises TimeoutError and cancels the call; `asyncio.gather` keeps the input order.
