# Answer the finance team's questions with DuckDB SQL

**Libraries:** DuckDB, pandas · **Level:** Intermediate · about 35 minutes

Bayport Supplies' finance team wants three numbers for the quarterly review: revenue by city, the customers who never ordered, and revenue by month with a running total. DuckDB runs SQL straight over pandas DataFrames (and over CSV and Parquet files), which is how many analysts now work. Write each answer as one SQL query.

Write your code in `lab.py`, then run `python tools/fde_check.py m03-py1` from the kit's folder.

<details><summary>Hints</summary>

1. `JOIN customers c USING (customer_id)` joins on the shared column; `GROUP BY c.city ORDER BY revenue DESC`.
2. Customers with no orders: `LEFT JOIN orders o USING (customer_id) WHERE o.order_id IS NULL`.
3. A running total is a window over the grouped sums: `SUM(SUM(amount)) OVER (ORDER BY month)`, with `strftime(order_date, '%Y-%m') AS month`.
</details>

## Why it matters

SQL is still the fastest way to answer a business question, and DuckDB brings it to DataFrames and files with no database server. LEFT JOIN ... IS NULL and window functions come up in almost every client review.
