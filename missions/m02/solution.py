from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP


class Money:
    """An amount and a currency. Design it so it cannot be changed or mixed by accident."""


class QuoteLine:
    """description, qty (a positive whole number) and unit (Money)."""


class Quote:
    """lines and discount_pct (0 to 30). total() and to_dict()."""


# Try your classes here, for example:
# q = Quote([QuoteLine("Venue", 1, Money(Decimal("1200.00"), "USD"))], 10)
# print(q.total(), q.to_dict())
