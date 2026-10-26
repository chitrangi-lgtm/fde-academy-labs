# Reconcile the supplier price list

**From:** Priya Natarajan, Pricing Operations Lead, Larkspur Home Goods

Our price file is a mess. The same product appears several times, sometimes with spaces or lower-case codes, and when a supplier changes a price we just add a row with the new effective date. Last week two people quoted different prices for the same item. I need two things I can call from our quoting tool: today's price for every product, and a list of products where the file itself disagrees with itself. Please treat the catalog as the source of truth when two rows clash on the same date, and skip rows with no price rather than inventing one. This quarter's file is attached; next quarter's will look the same, so don't hard-code anything.

## Done when

- `current_prices(path)` returns {sku: price} with SKUs in upper case and trimmed, prices as floats, using each SKU's latest effective date
- When rows clash on that latest date, the catalog row's price wins
- Rows without a price are skipped
- `conflicts(path)` returns the sorted SKUs whose latest date has more than one distinct price
- Both functions work on any file in the same format (a second file is attached to test with)

## Files

`prices.csv`, `prices_q2.csv`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m01
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module m01) records your score.
