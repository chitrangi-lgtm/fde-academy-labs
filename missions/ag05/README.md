# Retrieve until you have enough, then stop

**From:** Sven Aaltonen, Search Lead, Quillon Legal Search

Our research agent either searches once and gives up, or searches twenty times and burns the budget. Our lawyers write questions in their own words, which don't always match the documents. I want a disciplined strategy: search the question's keywords; if nothing comes back, retry with our synonym list; if still nothing, broaden by dropping the last keyword, one at a time; stop at the first search that finds something, and never run more searches than the budget allows. The search function, stopwords and synonyms are provided.

## Done when

- `keywords(question)`: the lower-case words (letters and digits) not in STOPWORDS, in order
- `answer(question, search, max_searches=3)` returns {"found", "citations" (sorted ids), "searches" (the queries run, in order)}
- Query order: the keywords; then the keywords with synonyms swapped in (only if that changes the query); then the keywords with the last one dropped, then the last two, and so on
- Stop at the first query with results; never exceed max_searches; found is False if nothing was found

## Files

none

`provided.py` holds code the client gives you; the checker runs it before your code.

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag05
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module ag05) records your score.
