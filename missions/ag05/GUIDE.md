# Self-study guide: Retrieve until you have enough, then stop

Retrieval agents fail in two opposite ways: they search once and give up, or they search without limit and burn the budget. A written policy (what to try next, and when to stop) makes the agent predictable, cheap and easy to evaluate. It also handles the most common problem in enterprise search: users' words do not match the documents' words.

## Revise first (in the course)

- query planning: rewriting and broadening
- retrieval as a tool
- evaluating and securing retrieval

## Read the email like an FDE

The search lead writes the strategy as an ordered list. First the question's keywords, without stopwords. Then, if nothing came back, the same keywords with synonyms swapped in, but only if that changes the query. Then broaden by dropping the last keyword, then the last two, and so on. Stop at the first search with results, and never run more searches than the budget. The searches run must be returned in order, so the client can see what the agent did.

## Questions to ask the client first

- **Who maintains the synonym list, and how is it reviewed?** A bad synonym silently changes what lawyers find.
- **Is it better to return a broad result or to say nothing was found?** In legal research a loosely related document can mislead.
- **Should the agent tell the lawyer which query found the documents?** Showing the final query helps lawyers judge the result.

## How each criterion is checked

1. **Keywords drop stopwords and punctuation:** keywords must drop stopwords and punctuation and keep the order of the remaining words.
2. **A direct hit stops after one search:** A question that matches directly must stop after one search with the right citations.
3. **Synonyms rescue the lawyer's own words:** A question in the lawyer's own words must succeed on the second search, with synonyms swapped in.
4. **Broadening drops the last keyword:** A question with too many keywords must succeed after dropping the last one.
5. **Nothing found within the budget:** A question with no matches must return found False after the three searches the budget allows.
6. **The budget is never exceeded:** With a budget of one, exactly one search must be run.

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
| The synonym query repeats the original | It was added even when no word changed. | Add the synonym query only if it differs. |
| Broadening drops the first words | Words were removed from the front. | Keep the first words and drop from the end. |
| Four searches run with a budget of three | The budget was checked after running a query. | Check the budget before each search. |
| Citations come back unsorted | They were returned in search order. | Sort the citation ids. |

## Test yourself before you check

- Write down the candidate queries for each test question before running your code.
- Print each query as it runs and the number of results.
- Try a one-word question: how many candidate queries are there?
- Change the budget from 1 to 5 and watch the searches list.

## What a senior reviewer also looks for

A reviewer would check that the strategy is visible as one ordered list of steps, that the budget guard cannot be skipped, and that the result always shows the queries run. They would also ask for an evaluation set of lawyers' questions so changes to the synonyms can be measured.

## Stretch goal

Add a decomposition step for questions with 'and' (search each part separately and merge the citations) while keeping the same overall budget.
