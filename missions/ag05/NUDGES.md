# Nudges (open only if stuck)

1. Write a generator of candidate queries in the agreed order, then loop over it with the budget as a guard.

2. Only add the synonym query if it differs from the original; broadening keeps the first words and drops from the end.

## The approach, in plain English (open last)

1. Write keywords: lower-case words of letters and digits, without stopwords, in order.
2. Write a generator of candidate queries in the agreed order: the keywords, the synonym version if it differs, then the keywords with one, two and more words dropped from the end.
3. In answer, loop over the candidates, stopping when the budget is used up.
4. Run each query, record it, and return at the first one with results, with the citations sorted.
5. If nothing was found, return found False with the searches run.
