# Self-study guide: Heal three suppliers' schema drift with pandas

Three suppliers send price files for the pricing team. supplier_a.csv uses sku, price and updated; supplier_b.csv uses SKU, 'Price (USD)' with dollar signs and thousands separators, and US-style dates (month first); supplier_c.csv uses item_code, cost and full timestamps. SKUs arrive in mixed case with spaces, one price is 'n/a' and one row has no SKU. You build one clean table and quarantine, with a reason, every row you cannot trust.

## Revise first (in the course)

- healing schema drift with an alias map
- auto-healing versus dead-letter quarantine
- the pathologies of real enterprise data

## Questions to ask the client first

- **When two suppliers quote the same SKU, which price should the pricing team see?** One clean table invites a second question: which source wins.
- **Who receives the quarantine list, and how fast must rows be fixed?** A quarantine nobody reads becomes silent data loss.
- **Will more suppliers join, each with its own columns?** If so, the column mapping should be data, not code, so adding one is a small change.

## Ideas you will use

- **One target contract:** Decide the clean table's columns first (supplier, sku, price, updated) and map each supplier's columns onto it with rename. Every later step then works on one shape.
- **Reading as text:** dtype=str keeps every value as written, so pandas does not guess types differently for each file. You convert prices and dates yourself, on purpose.
- **Coercing numbers:** After removing dollar signs and commas, pd.to_numeric with errors='coerce' turns anything that is still not a number (like 'n/a') into NaN, which you can quarantine.
- **Parsing each date format:** Each supplier's dates are parsed with that supplier's own format before the tables are combined, then written as YYYY-MM-DD text. Guessing formats across mixed files swaps days and months.

## Steps, check by check

1. **The clean table has the agreed columns:** Rename each supplier's columns to supplier, sku, price and updated so the clean table has exactly those columns.
2. **Six rows are clean:** Combine the three suppliers and keep only the rows with a SKU and a readable price: six rows.
3. **'$1,250.00' becomes 1250.0:** Remove the dollar sign and thousands separator before converting prices, so '$1,250.00' becomes 1250.0.
4. **Every SKU looks like AB-100:** Strip spaces and upper-case every SKU so they all look like AB-100.
5. **Dates are ISO strings from all three formats:** Parse each supplier's dates with its own format and write them as YYYY-MM-DD.
6. **Two rows are quarantined with reasons:** Put the row with no SKU and the row with an unreadable price into quarantine, each with its reason.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If the row count is wrong, print the combined table before filtering and look at each row's SKU and price. If dates are wrong, print each supplier's parsed dates separately: a month-first date read day-first moves to another month. If the SKU check fails, print the SKUs that do not match the pattern.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| Supplier b's dates come out as February instead of March | The month-first format was not given. | Parse supplier b's dates with a month-first format. |
| '$1,250.00' becomes NaN | Only the dollar sign was removed. | Remove the thousands separator too. |
| The row without a SKU is quarantined as a bad price | Checks ran in the wrong order. | Check for a missing SKU first, and give each row one reason. |
| Timestamps keep their time | Supplier c's dates were not converted to dates. | Parse them as UTC and format as YYYY-MM-DD. |

## What the result means for the client

The pricing team gets six trustworthy prices in one table, and the two rows that could not be trusted come back with reasons the suppliers can act on: a missing SKU and a price written as 'n/a'. Send the quarantine to the supplier managers, not only the clean table to pricing, because the fix belongs at the source.

## What to send the client

The clean table for the pricing team and the quarantine list for the supplier managers, each row with its supplier, line and reason, plus the column mapping used for each supplier.

## Stretch goal

Move the three column mappings and date formats into one dictionary of supplier settings, so a fourth supplier needs only a new entry, and add a count of quarantined rows per supplier.
