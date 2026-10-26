# Profile a messy sales extract with pandas

**Libraries:** pandas · **Level:** Beginner · about 30 minutes

Northwind Retail's operations lead sends a sales extract and asks two questions before tomorrow's stand-up: which region earns the most, and which products sell best? The file is typical of client data: one order appears twice, a region has stray spaces and lower case, one row has no quantity and one has no real date. Clean it, explain what you dropped, and answer both questions.

Write your code in `lab.py`, then run `python tools/fde_check.py m01-py1` from the kit's folder.

<details><summary>Hints</summary>

1. `raw.drop_duplicates()` removes rows that are identical in every column.
2. `df['region'].str.strip().str.title()` fixes spaces and case. `pd.to_datetime(df['date'], errors='coerce')` turns a bad date into NaT, which `.isna()` finds.
3. Build `revenue` on the clean rows, then `clean.groupby('region')['revenue'].sum()`; `.sort_values(ascending=False).index` gives the ranking.
</details>

## Why it matters

Profile before you answer: duplicates, inconsistent labels and unparseable values change the numbers a client sees. Say what you dropped and why, in the same message as the answer.
