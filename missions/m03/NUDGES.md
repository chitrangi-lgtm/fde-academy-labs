# Nudges (open only if stuck)

1. `conn.executescript(text)` runs a file with several statements; `conn.execute` runs one.

2. Never build SQL with f-strings from user input: pass values as parameters, `conn.execute(sql, (name,))`.

## The approach, in plain English (open last)

1. Read shop.sql and run the whole file against the connection; it holds several statements.
2. For revenue, join orders to customers, keep only paid orders, group by region and order by the total, largest first.
3. For customers without orders, start from customers, left join orders, and keep the rows where no order matched. Sort the names.
4. For the lookup, write the query with a placeholder for the name and pass the name separately as a parameter.
5. Run each function and print its result before checking.
