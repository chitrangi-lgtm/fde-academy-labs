# Self-study guide: Answer the CFO's questions, safely

Executives ask for answers from operational databases all the time, and an FDE is often the person who writes the query in front of them. Two things decide whether the client trusts you afterwards: numbers that count the right rows, and lookups that cannot be abused. SQL injection is still one of the most common findings in enterprise security reviews.

## Revise first (in the course)

- parameterised queries and why they stop SQL injection
- joins, NULLs and the double-counting trap
- anti-joins: finding rows with no match

## Read the email like an FDE

The CFO asks three precise questions. 'Paid revenue by region, highest first' carries a filter (paid only) and an order. 'Customers who have never placed an order' is a question about missing rows, which an ordinary join cannot answer. 'A lookup our support team can use by name' is user input going into SQL, and the next sentence tells you an earlier version was broken by a quote mark: the lookup must treat the name as data, never as part of the query. 'The export is attached as SQL' means you load it by running the file, not by parsing it yourself.

## Questions to ask the client first

- **Should refunded or partly paid orders count towards revenue?** 'Paid' can mean several statuses; the CFO's number must match finance's definition.
- **Can two customers share a name, and should the lookup return both?** Support will search by name, so duplicates decide whether the result is safe to act on.
- **Is the support lookup allowed to show order amounts or only order numbers?** Least privilege applies to internal tools too.

## How each criterion is checked

1. **The tables load from the export:** A fresh in-memory database is loaded with your load(), then the customers table must hold 5 rows.
2. **Paid revenue by region, highest first:** revenue_by_region must return exactly two regions with their paid totals, highest first. Unpaid orders counted, or a region with no paid revenue, fail it.
3. **Customers who never ordered:** customers_without_orders must return only the customer with no orders at all, as a sorted list of names.
4. **Support's lookup works:** orders_for for a known customer must return that customer's order ids, sorted.
5. **A quote-mark trick returns nothing:** orders_for is called with a name containing a quote-mark trick. A safe lookup finds no customer by that name and returns an empty list.
6. **A destructive input leaves the data intact:** orders_for is called with an input that tries to delete the orders table. Afterwards the table must still hold all 6 orders.

## How to work it

1. Read the email twice: once for the story, then with a pen, underlining every number, every rule and every 'must' or 'never'. Those words become the checks.
2. Turn the acceptance criteria into your own checklist, one line per criterion, and decide how you will see each one working before you build it.
3. Open the data files and the provided code before writing anything. Real files hold the awkward cases (blanks, duplicates, odd formats) the checks use.
4. Build the smallest piece that runs, print its result, and compare it with what you worked out by hand.
5. Add the next rule, run again, and keep each business rule in one obvious, named place.
6. Press Check only when your own prints agree with the criteria, then read each failing criterion's message before you change any code.
7. When it passes, read your code as the client's reviewer would, then compare it with the debrief.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| Revenue is too high | The status filter is missing, so pending and refunded orders are counted. | Filter on paid orders before grouping. |
| customers_without_orders returns nothing | An inner join drops customers who have no orders. | Use a left join and test the order side for NULL. |
| The quote-mark test lists every order | The name was pasted into the SQL text with an f-string. | Use a placeholder and pass the name as a parameter. |
| sqlite3 says you can only execute one statement at a time | The whole file was run with execute. | Use the method that runs a script of several statements. |

## Test yourself before you check

- Count the orders and customers yourself after load(), and compare with the export file.
- Work out North's and South's paid totals by hand from the export.
- Call orders_for with a name containing a quote mark and confirm you get an empty list, not an error or every order.
- Print the query you send for the lookup: the name must not appear inside it.

## What a senior reviewer also looks for

A reviewer would read every query that takes user input first, looking for placeholders. They would also check that queries name their columns instead of selecting everything, that the paid filter is explicit, and that results come back as plain Python values the support tool can use, not database rows with hidden types.

## Stretch goal

Add revenue by region and month for the board pack, and a case-insensitive lookup that still uses parameters, then explain in a comment why LIKE with user input needs its wildcards escaped.
