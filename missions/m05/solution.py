from provided import *  # the client's code (the checker runs provided.py first)

import asyncio
import time

SUPPLIERS = [f"s{i}" for i in range(1, 13)]


# Today's code, for reference: correct, but slow, and it waits a full second on each slow supplier.
#     results = []
#     for s in suppliers:
#         results.append(await fetch_quote(s))
#     return results


async def gather_quotes(suppliers, limit=4, timeout=0.2):
    """One dict per supplier, in input order, with at most `limit` calls in flight and a per-call timeout."""
    return []


start = time.perf_counter()
quotes = asyncio.run(gather_quotes(SUPPLIERS))
print(f"{time.perf_counter() - start:.2f} s", quotes)
