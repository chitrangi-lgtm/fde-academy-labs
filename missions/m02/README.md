# Make a quote that cannot add up wrongly

**From:** Tomás Herrera, Head of Sales Operations, Brightline Events

Our quoting spreadsheet keeps producing totals that are a cent out, quotes with zero-quantity lines, and once a quote that mixed dollars and euros. We're moving quoting into Python. I want money that can't be mixed by accident or changed after it's created, quote lines that reject nonsense, and a total our finance team will sign: discounts up to 30 percent, rounded to the cent the way accountants round (half up). Finance also wants each quote as a dictionary for the invoicing system, with the total as text like "1755.00".

## Done when

- `Money(amount, currency)` holds a Decimal, cannot be changed after creation, adds only to the same currency (ValueError otherwise) and multiplies by a whole number
- `QuoteLine(description, qty, unit)` rejects a quantity that is not a positive whole number (ValueError)
- `Quote(lines, discount_pct=0)` rejects mixed currencies and a discount outside 0 to 30 (ValueError)
- `Quote.total()` returns Money rounded half up to the cent after the discount
- `Quote.to_dict()` returns lines, discount_pct, total as text with two decimals, and currency

## Files

none

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m02
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
