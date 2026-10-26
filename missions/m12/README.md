# Load the drifting partner feed without losing a row

**From:** Chen Wei, Data Platform Lead, Ravello Payments

A partner sends daily payment records as JSON lines. Over the months their field names drifted (amount, amt, total_amount), dates arrive in three formats, and amounts sometimes have a currency symbol or thousands separators. Finance needs every record either loaded cleanly or quarantined with a reason: nothing silently dropped, nothing guessed, and money in Decimal, never floats.

## Done when

- `normalize(record)` returns {"id", "date" (YYYY-MM-DD), "amount" (Decimal), "currency"} or raises ValueError with a short reason
- Amount comes from amount, amt or total_amount; "$1,250.50" becomes Decimal("1250.50") with currency USD; a three-letter currency field wins when present
- Dates may be 2026-03-01, 03/01/2026 (month first) or 1 Mar 2026
- `load(path)` returns (good, quarantine) where quarantine is [(line_number, reason)] counting from 1, and every line ends up in exactly one of them

## Files

`feed.jsonl`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m12
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
