import asyncio

# Provided: behaves like the real supplier client. s7 and s11 are slow today.
_DELAYS = {f"s{i}": 0.05 for i in range(1, 13)}
_DELAYS["s7"] = _DELAYS["s11"] = 1.0
_IN_FLIGHT = {"now": 0, "peak": 0}


async def fetch_quote(supplier):
    _IN_FLIGHT["now"] += 1
    _IN_FLIGHT["peak"] = max(_IN_FLIGHT["peak"], _IN_FLIGHT["now"])
    try:
        await asyncio.sleep(_DELAYS[supplier])
        return {"supplier": supplier, "price": 100.0 + int(supplier[1:])}
    finally:
        _IN_FLIGHT["now"] -= 1
