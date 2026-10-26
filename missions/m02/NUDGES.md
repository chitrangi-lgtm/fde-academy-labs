# Nudges (open only if stuck)

1. `@dataclass(frozen=True)` makes instances read-only; validate in `__post_init__` and raise ValueError there.

2. Do the arithmetic in Decimal and round once at the end with `.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)`.
