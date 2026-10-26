# Self-study guide: Reconcile the supplier price list

Price files that disagree with themselves are among the first data problems an FDE meets at a retail or distribution client. Quoting, invoicing and margin reports all read the same file, so one duplicate code or same-day clash becomes two different prices quoted to two customers. Clients judge you on whether the numbers you hand back can be trusted and explained.

## Revise first (in the course)

- reading CSV files safely with csv.DictReader and with open
- grouping rows into dictionaries with setdefault and get
- cleaning and deduplicating messy records before deciding

## Read the email like an FDE

Underline the business rules hidden in the wording before you write any code. 'The same product appears several times, sometimes with spaces or lower-case codes' means the SKU must be cleaned before anything is grouped. 'When a supplier changes a price we just add a row' means the history is kept, so today's price is the row with the latest effective date, not the last row in the file. 'Treat the catalog as the source of truth when two rows clash on the same date' is a tie-break, and it only matters on that latest date. 'Skip rows with no price rather than inventing one' rules out defaulting to zero. 'Next quarter's will look the same, so don't hard-code anything' tells you a second file will be used to test you.

## Questions to ask the client first

- **If two rows clash on the same date and neither comes from the catalog, which one wins?** The email covers catalog-versus-supplier clashes only; an unstated tie-break is a future argument.
- **Should a future effective date count as today's price?** Price files often carry announced increases; quoting tomorrow's price today loses deals.
- **Who fixes the conflicts the report lists, and how often?** A report nobody owns is ignored; naming the owner shapes what it should contain.

## How each criterion is checked

1. **Today's prices are right for this quarter's file:** current_prices is called on prices.csv and the whole dictionary is compared with the expected one, so an extra SKU, a missing SKU or a SKU that still has spaces or lower case fails it.
2. **The catalog price wins a same-day clash:** One SKU has two rows on its latest date, from different sources with different prices. The check looks only at that SKU and expects the catalog's price.
3. **A row with no price is skipped:** One SKU appears only with an empty price cell. The check expects it to be absent from the result, not present with 0 or None.
4. **Prices are floats:** Every value in the returned dictionary must be a float. Returning the text from the CSV fails even when it prints the same.
5. **Same-day disagreements are listed, identical duplicates are not:** conflicts('prices.csv') must be exactly one SKU. The file also repeats a SKU on the same date with the same price: that is a duplicate, not a conflict.
6. **Nothing is hard-coded: next quarter's file works:** Both functions are called on prices_q2.csv, which has different SKUs and dates. Anything tied to this quarter's values fails here.

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
| A SKU appears twice in your result, once in lower case | The SKU was grouped before it was cleaned. | Strip and upper-case the SKU on the way in, before any grouping. |
| A SKU shows an old price | You kept the last row in the file instead of the latest effective date. | Choose by date, never by row order. |
| conflicts lists a SKU whose two rows have the same price | You counted rows instead of distinct prices. | Put the prices for the latest date in a set and look at its size. |
| ValueError: could not convert string to float | A blank price reached float(). | Check for an empty price after stripping, and skip that row first. |

## Test yourself before you check

- Print current_prices('prices.csv') and check each SKU against the file by hand: which date did you use, and why that price?
- Print the grouped rows for the clashing SKU to see both sources on the same date.
- Run both functions on prices_q2.csv: if any value from this quarter appears, something is hard-coded.
- Print the set of value types in your result; it should contain only float.

## What a senior reviewer also looks for

A reviewer at the client would ask where the 'catalog wins' rule lives: it should sit in one obvious, named place, so the pricing team can change it later. They would also look for the file being read with a context manager, no silent except blocks, and helper names that say what they do. A short docstring stating the three rules (latest date, catalog wins, blanks skipped) turns the code into documentation the pricing team can read.

## Stretch goal

Return, for each conflict, the competing prices and their sources so the pricing team can fix the file at the source, and add a report of SKUs whose latest price moved by more than 20 percent from the previous date.
