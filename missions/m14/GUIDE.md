# Self-study guide: Table-aware chunking with tenant-safe retrieval

Most wrong answers from enterprise assistants come from retrieval, not the model: the right fact was cut away from its meaning, or the wrong customer's document was searched. A table row without its header is a number without a meaning, and a shared index without a tenant filter is a data leak. Citations are what let the client check every answer.

## Revise first (in the course)

- layout-aware parsing and table chunking
- naive chunking versus keeping table headers
- filtering by permission before retrieval

## Read the email like an FDE

The knowledge manager describes two incidents and three requirements. The wrong per diem came from a row separated from its header, so each table row must become its own chunk that starts with the header line. The other company's policy appeared because both share one index, so search must only look at the asking company's chunks, filtering before ranking rather than after. The citation format is fixed: document id and chunk number. The acceptance criteria also define the scoring: distinct query words found, with ties broken by document id and then chunk number.

## Questions to ask the client first

- **Do your documents ever contain tables without a header row, or with merged cells?** A chunker built for clean Markdown tables needs a rule for the messy ones.
- **Where does the tenant of the person asking come from: the login, or the question?** The tenant must come from identity, never from text the user can type.
- **Should the assistant answer at all when no chunk matches well?** Returning the best weak match invites a confident wrong answer.

## How each criterion is checked

1. **Paragraphs and table rows become separate chunks:** chunk on the first document must produce five chunks numbered from 1, and the second document two chunks.
2. **Every table row carries the header:** Every chunk that contains a tier row must start with the table's header line.
3. **A row chunk keeps its own values:** One row chunk must still contain its own values for tier 2.
4. **Search finds the right row for its tenant:** search for the tier 2 nightly per diem for the first company must return its tier 2 row, by document and chunk number.
5. **Another tenant's chunks never appear:** With k=10, search must return only that company's chunks.
6. **The other tenant gets its own rate:** The same query for the other company must return its own, different rate.
7. **Citations name the document and chunk:** cite on the best chunk must return the document id and chunk number in brackets.

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
| Row chunks lack the header | The table was split by lines like any paragraph. | Detect tables and prepend the header line to each row. |
| The separator line becomes a chunk | All lines after the header were treated as rows. | Start rows from the third line of the table. |
| The other company's rate appears | Results were filtered after taking the top k. | Filter by tenant before ranking. |
| Ties come back in a different order | Sorting used only the score. | Sort by score, then document id, then chunk number. |

## Test yourself before you check

- Print every chunk of the first document and read each as the model would see it.
- Search with a query for a word that only the other company uses and confirm nothing leaks.
- Try a query with repeated words: each distinct word should count once.
- Check that chunk numbers restart at 1 for each document.

## What a senior reviewer also looks for

A reviewer would check that the tenant filter happens in one place, before any ranking, and cannot be bypassed by an argument left empty. They would also look for the table detection to be a small, named function with tests, and for citations on every answer the assistant gives.

## Stretch goal

Keep the heading path of each paragraph (the section titles above it) in the chunk, and include it in the citation, so the client can see where in the policy the answer came from.
