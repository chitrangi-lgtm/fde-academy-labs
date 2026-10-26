# Self-study guide: Profile a messy sales extract with pandas

The operations lead wants two answers for tomorrow's stand-up: which region earns the most and which products sell best. sales.csv has one row per order line with order_id, date, region, product, qty and unit_price. It is typical client data: one order appears twice, a region is written with stray spaces and lower case, one row has no quantity and one row has text where the date should be.

## Revise first (in the course)

- reading CSV files and checking what you loaded
- deduplicating and cleaning messy records
- the pathologies of real enterprise data

## Questions to ask the client first

- **Is a repeated order id always a duplicate, or can one order have several lines?** Dropping real order lines would understate revenue; the rule must come from the client.
- **Should rows without a quantity be fixed at the source or ignored in reports?** If they are real sales, ignoring them hides revenue the team expects to see.
- **Are prices in one currency and before or after tax?** Mixing taxed and untaxed prices makes regions impossible to compare.

## Ideas you will use

- **Profiling first:** Before answering, look at the data: print it, look at the types pandas guessed, count missing values. A column of prices read as text, or a date column with one bad value, changes every number that follows.
- **Duplicates:** drop_duplicates removes rows that are identical in every column. Real duplicates are often exact copies from a re-sent export; near-duplicates need a business rule, which this lab does not need.
- **Coercing dates:** pd.to_datetime with errors='coerce' turns anything that is not a real date into NaT, a missing date you can find with isna(). It is how you separate bad rows from good ones without crashing.
- **Group and sort:** groupby('region')['revenue'].sum() adds revenue per region; sort_values(ascending=False) puts the largest first, and the index of the result is the ranking.

## Steps, check by check

1. **Two bad rows are dropped (no quantity, no real date):** Remove the exact duplicate, tidy the region names, turn the dates into real dates, then count the rows with no quantity or no real date and store that count in bad_rows.
2. **Seven clean rows remain after removing the duplicate and the bad rows:** Keep the remaining rows in clean: seven rows once the duplicate and the two bad rows are gone.
3. **Regions are tidy: North, South, East or West:** Make sure every region is one of North, South, East or West after stripping spaces and fixing the case.
4. **Revenue per region is right:** Add a revenue column (quantity times unit price) to the clean rows and add it up per region, rounded to two decimals, into by_region.
5. **Products are ranked by revenue:** Add revenue up per product and list the products from highest to lowest revenue in top_products.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

Each check names the variable it reads. If the count of bad rows is wrong, print the rows you dropped and look at why each one was dropped. If regional revenue is off, print clean and look for a region that still has spaces, or prices still stored as text.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| Five regions instead of four | ' North' and 'south' were left as they were. | Strip spaces and fix the case before grouping. |
| bad_rows is 3 | The duplicate was counted as a bad row. | Remove duplicates first, then count only missing quantities and bad dates. |
| Revenue for West is wrong | A price stored as text was multiplied as text. | Convert unit_price to a number before multiplying. |
| by_region has numpy numbers that print oddly | The pandas result was used directly. | Convert each value to a float and round it. |

## What the result means for the client

West earns the most, and Gadget is the top product by revenue, but the answer is only half the message. Tell the operations lead what you removed (one duplicate order, one row without a quantity, one with no real date) so they can fix the export, and so nobody is surprised when their own spreadsheet gives a different total.

## What to send the client

A short message to the operations lead: revenue by region and the product ranking in a small table, then one line per problem found in the extract (the duplicate order, the row without a quantity, the row without a real date) and a request to fix them at the source.

## Stretch goal

Count revenue by region and month, and add a small table of the problems found (duplicates, bad dates, missing quantities) to send back to the team that produces the extract, so next month's file arrives cleaner.
