# Nudges (open only if stuck)

1. Write a generator of candidate queries in the agreed order, then loop over it with the budget as a guard.

2. Only add the synonym query if it differs from the original; broadening keeps the first words and drops from the end.
