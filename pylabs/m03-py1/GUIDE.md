# Self-study guide: Answer the finance team's questions with DuckDB SQL

Finance wants three numbers for the quarterly review: revenue by city, the customers who never ordered, and revenue by month with a running total. customers.csv holds each customer's id, name and city; orders.csv holds each order's id, customer id, date and amount. DuckDB runs SQL directly over the pandas DataFrames, so each answer can be one query.

## Revise first (in the course)

- joins, NULLs and the double-counting trap
- anti-joins and window functions
- relational tables and keys

## Questions to ask the client first

- **Does revenue mean order amounts, or amounts after refunds and cancellations?** Finance's definition decides which orders count.
- **Should customers who signed up this quarter appear in the 'never ordered' list?** A new customer who has not ordered yet is not the same sales problem as a lapsed one.
- **Which calendar does finance use for months and quarters?** A fiscal year that starts in another month changes every quarterly figure.

## Ideas you will use

- **DuckDB over DataFrames:** duckdb.sql('SELECT ... FROM orders') finds the DataFrame called orders in your Python variables and queries it. .df() turns the result back into a DataFrame and .fetchall() into a list of tuples.
- **Joins:** An inner join keeps rows that match on both sides; USING (customer_id) joins on the column both tables share. A left join keeps every row from the left table, with NULLs where nothing matched.
- **Anti-join:** Customers who never ordered are the left-join rows where the order side is NULL. An inner join can never find them, because it drops them.
- **Window functions:** SUM(...) OVER (ORDER BY month) adds up the values of all rows up to the current one. Applied to monthly sums, it gives a running total without a loop.

## Steps, check by check

1. **Bayport is the top city:** Join orders to customers, add up revenue per city and order the result from highest to lowest, so the top city is first.
2. **Bayport's revenue is 490.25:** Keep the revenue as the plain sum of the order amounts for that city.
3. **Only the three cities with orders appear:** Use an inner join so cities with no orders do not appear at all.
4. **The customer with no orders is found with a LEFT JOIN:** Find customers with no orders with a left join and a NULL test, and return their names sorted.
5. **Monthly revenue has a running total:** Group orders by month (as text like 2026-01), add up revenue, and add a running total with a window function, in month order.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

Print each DataFrame you build. If the city count is wrong, check which join you used. If the running total is wrong, print the monthly sums first and add them up by hand: the window must run over the monthly totals, in month order. If a query fails to run at all, read DuckDB's message: it names the column or keyword it did not understand, and the position in the query.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| Riverton appears with no revenue | A left join was used for revenue by city. | Use an inner join for revenue; save the left join for customers without orders. |
| no_orders is empty | An inner join drops customers without orders. | Use a left join and keep rows where the order id is NULL. |
| The running total resets every month | The window was partitioned by month. | Order the window by month without partitioning it. |
| Months sort wrongly | Month names were used instead of year-month text. | Format the date as year-month so it sorts as text. |

## What the result means for the client

Bayport is the biggest city, one customer has never ordered, and revenue grew each month, reaching the quarter's total in March. For finance, show the running total next to the monthly figures and name the customer with no orders as a sales follow-up rather than a data problem. Keep the three queries with the numbers: when finance asks how a figure was produced, the query is the answer, and they can rerun it next quarter on new files without asking you.

## What to send the client

The three tables for the quarterly review, each with the query that produced it, and a note naming the customer with no orders for the sales team to contact.

## Stretch goal

Add each city's share of total revenue as a percentage, and the average order value per customer, in the same style of single queries.
