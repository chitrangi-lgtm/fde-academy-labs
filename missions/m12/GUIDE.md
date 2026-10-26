# Self-study guide: Load the drifting partner feed without losing a row

Partner feeds drift: fields get renamed, formats change, someone adds a currency symbol. Finance cannot accept silently dropped rows or guessed values, so enterprise loaders either load a record cleanly or quarantine it with a reason. The quarantine report is often the deliverable the client reads most.

## Revise first (in the course)

- auto-healing versus dead-letter quarantine
- healing schema drift with an alias map
- the five pathologies of real enterprise data

## Read the email like an FDE

The data platform lead lists every kind of drift you will meet, and the rule for all of them. Field names drift between amount, amt and total_amount. Dates arrive in three formats, and the slash format is month first. Amounts may carry a dollar sign or thousands separators, and a dollar sign implies USD unless a currency field says otherwise. 'Nothing silently dropped, nothing guessed' is the invariant: every line ends up loaded or quarantined, and anything you cannot read with certainty goes to quarantine. 'Money in Decimal, never floats' is a hard rule.

## Questions to ask the client first

- **Who reviews the quarantine, and how fast must records be fixed?** Quarantined payments still need paying; the process matters as much as the code.
- **Which time zone are the dates in?** A payment near midnight can land on the wrong day in finance's books.
- **Can the partner send a corrected record for a quarantined line?** Corrections need an id rule so they replace, not duplicate, the original.

## How each criterion is checked

1. **Clean records load with ISO dates and Decimal amounts:** load('feed.jsonl') must return the three clean records with ISO dates, Decimal amounts and the right currencies, in file order.
2. **Money is Decimal, never float:** Every amount in the clean records must be a Decimal.
3. **Every bad line is quarantined by line number:** The five bad lines must be quarantined with their line numbers, counting from 1.
4. **Each quarantined line has a reason:** Every quarantined line must carry a reason of at least a few characters.
5. **Nothing is lost:** Loaded plus quarantined must equal all eight lines.
6. **normalize refuses a record without an amount, and accepts a good one:** normalize must refuse a record with no amount and accept a good one.

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
| A record vanishes | An exception was caught and ignored instead of quarantined. | Every except branch must add the line to the quarantine. |
| 03/01/2026 becomes 3 January | The slash format was read day first. | Use month-first for the slash format, as the email says. |
| Amounts print as 1250.5 | The amount went through float on the way. | Convert the cleaned text straight to Decimal. |
| Line numbers are one too low | Counting started at 0. | Count lines from 1, as finance does. |

## Test yourself before you check

- Read the feed file yourself and decide, line by line, load or quarantine and why.
- Print the quarantine list and check each reason would make sense to someone in finance.
- Check that the counts add up to the number of lines.
- Try normalize on a record with both a dollar sign and a currency field of EUR.

## What a senior reviewer also looks for

A reviewer would check that the accepted formats and field aliases are listed as data at the top, that reasons are specific enough to act on ('unknown date format: 31/31/2026', not 'error'), and that the loader never raises on a bad line. They would also ask for the quarantine to be written somewhere finance can open it.

## Stretch goal

Write the quarantine to a CSV with the original line, and add a summary that counts reasons, so the partner can be told which drift happens most.
