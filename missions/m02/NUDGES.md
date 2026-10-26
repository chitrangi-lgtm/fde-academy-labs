# Nudges (open only if stuck)

1. `@dataclass(frozen=True)` makes instances read-only; validate in `__post_init__` and raise ValueError there.

2. Do the arithmetic in Decimal and round once at the end with `.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)`.

## The approach, in plain English (open last)

1. Make Money a frozen dataclass with an amount and a currency, and convert the amount to Decimal when it is created.
2. Give Money an addition that refuses a different currency and a multiplication that accepts only a whole number.
3. Make QuoteLine frozen too, and refuse a quantity that is not a positive whole number when it is created.
4. In Quote, check the discount range and that all lines share one currency as soon as the quote is created.
5. For the total, add the line subtotals in Decimal, apply the discount, then round once to the cent, half up.
6. Build to_dict from total(), formatting the amount with exactly two decimals.
