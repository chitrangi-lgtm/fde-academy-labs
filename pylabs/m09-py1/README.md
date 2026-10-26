# Validate model output with pydantic

**Libraries:** pydantic · **Level:** Intermediate · about 35 minutes

An invoice-extraction prompt returns JSON most of the time. Finance has found invoices whose total does not match the lines, lower-case currency codes, a zero quantity, and one answer wrapped in chatty text and a code fence. Write a pydantic schema that catches every one of these, and a parser that rescues the wrapped answer.

Write your code in `lab.py`, then run `python tools/fde_check.py m09-py1` from the kit's folder. `GUIDE.md` has the ideas, the steps check by check and the common mistakes.

<details><summary>Hints</summary>

1. `Field(gt=0)` and `Field(ge=0)` add bounds; `Literal['USD', 'EUR', 'GBP']` restricts the currency.
2. Cross-field rules go in `@model_validator(mode='after')`: compare the sum of qty x unit_price with total (allow 0.01) and raise ValueError.
3. To rescue wrapped JSON: `re.search(r'\{.*\}', raw, re.S)` finds the outermost braces.
</details>

## Why it matters

Never trust model output because it looks like JSON. A schema with types, bounds, allowed values and cross-field rules turns silent bad data into a clear error you can retry, log or route to a person.
