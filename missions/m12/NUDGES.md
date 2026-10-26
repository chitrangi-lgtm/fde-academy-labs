# Nudges (open only if stuck)

1. Try each date format in turn with `datetime.strptime`; `%d %b %Y` reads '3 Mar 2026'.

2. Strip '$', ',' and spaces before `Decimal(...)`, and catch `decimal.InvalidOperation` to quarantine text amounts.
