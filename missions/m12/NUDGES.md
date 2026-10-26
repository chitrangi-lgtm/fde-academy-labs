# Nudges (open only if stuck)

1. Try each date format in turn with `datetime.strptime`; `%d %b %Y` reads '3 Mar 2026'.

2. Strip '$', ',' and spaces before `Decimal(...)`, and catch `decimal.InvalidOperation` to quarantine text amounts.

## The approach, in plain English (open last)

1. List the accepted date formats in one place and try them in turn, returning the ISO form or raising ValueError with a reason.
2. In normalize, check the id, find the amount under any of the three names, and work out the currency: the field if present, otherwise USD for a dollar sign, otherwise refuse.
3. Clean the amount text (symbol, separators, spaces) and convert it to Decimal, turning a failed conversion into ValueError.
4. In load, read the file line by line with line numbers, and put each line either in good or in quarantine with the reason, including lines that are not valid JSON.
