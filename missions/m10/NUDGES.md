# Nudges (open only if stuck)

1. Loop: build the list of items that are not picked, fit the remaining capacity and have every dependency picked.

2. From that list take the highest WSJF (ties by id), subtract its effort, repeat until the list is empty.

## The approach, in plain English (open last)

1. Load the backlog once.
2. Write wsjf from the formula and round to two places.
3. In plan, keep the picked ids and the remaining capacity.
4. In a loop, list the items not yet picked that fit the remaining capacity and whose dependencies are all picked.
5. If that list is empty, stop. Otherwise take the highest score (ties by id), add it and subtract its effort.
