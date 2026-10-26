# Nudges (open only if stuck)

1. Normalise the SKU first (`.strip().upper()`), then group rows by SKU and, inside that, by effective date.

2. ISO dates (2026-03-01) sort correctly as strings, so `max()` of the dates gives the latest; collect all rows on that date before choosing a price.

## The approach, in plain English (open last)

1. Write one small helper that reads the file and yields clean rows: the SKU stripped and upper-cased, the price as a float, the date and the source. Skip a row as soon as its price is blank.
2. Group the clean rows by SKU and, inside each SKU, by effective date, keeping every row for that date.
3. For each SKU pick the latest date. ISO dates compare correctly as text, so the largest string is the latest.
4. For current_prices, use the catalog row on that date if there is one, otherwise the price that is there.
5. For conflicts, count the distinct prices on that date; more than one means the file disagrees with itself. Return the SKUs sorted.
6. Print both functions' results for both files before you press Check.
