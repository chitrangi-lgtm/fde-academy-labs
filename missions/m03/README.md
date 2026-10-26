# Answer the CFO's questions, safely

**From:** Hana Kowalski, CFO, Corbel Outfitters

Before the board meeting I need three answers from our shop database: paid revenue by region, highest first; customers who have never placed an order; and a lookup our support team can use to list a customer's order numbers by name. Last year a contractor's lookup let someone type a quote mark and list every order in the system, so please make sure that can't happen. The database export is attached as SQL.

## Done when

- `load(conn)` creates and fills the tables from shop.sql in a sqlite3 connection
- `revenue_by_region(conn)` returns [(region, revenue)] counting only paid orders, highest first, and only regions with paid revenue
- `customers_without_orders(conn)` returns the sorted names of customers with no orders at all
- `orders_for(conn, name)` returns that customer's order ids, sorted, and is safe against SQL injection

## Files

`shop.sql`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m03
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
