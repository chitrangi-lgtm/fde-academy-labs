# Nudges (open only if stuck)

1. Normalise the SKU first (`.strip().upper()`), then group rows by SKU and, inside that, by effective date.

2. ISO dates (2026-03-01) sort correctly as strings, so `max()` of the dates gives the latest; collect all rows on that date before choosing a price.
