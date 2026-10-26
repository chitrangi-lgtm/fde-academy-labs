# Heal three suppliers' schema drift with pandas

**Libraries:** pandas · **Level:** Intermediate · about 40 minutes

Three suppliers send price files. Each uses different column names, date formats and price formats ('$1,250.00', 'n/a'), and SKUs arrive in mixed case with spaces. Build one clean table for the pricing team, and quarantine, with a reason, every row you cannot trust instead of guessing.

Write your code in `lab.py`, then run `python tools/fde_check.py m12-py1` from the kit's folder. `GUIDE.md` has the ideas, the steps check by check and the common mistakes.

<details><summary>Hints</summary>

1. Rename each file's columns to sku, price, updated with `df.rename(columns={...})`, add a supplier column, then `pd.concat`.
2. Prices: remove '$' and ',' with `.str.replace(r'[$,]', '', regex=True)`, then `pd.to_numeric(..., errors='coerce')`: 'n/a' becomes NaN.
3. Dates: parse each supplier with its own format (`format='%m/%d/%Y'` for b, `utc=True` for c) before concatenating, then `.dt.strftime('%Y-%m-%d')`.
</details>

## Why it matters

Schema drift is normal in client data. Map each source to one contract explicitly, parse each format on purpose, and quarantine what you cannot trust with a reason the client can act on.
