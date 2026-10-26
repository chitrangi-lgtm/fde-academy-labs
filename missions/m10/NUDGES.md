# Nudges (open only if stuck)

1. Loop: build the list of items that are not picked, fit the remaining capacity and have every dependency picked.

2. From that list take the highest WSJF (ties by id), subtract its effort, repeat until the list is empty.
