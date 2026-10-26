# Self-study guide: Plan the first sprint within capacity

Every engagement starts with more ideas than capacity. An FDE who can turn a backlog into a sprint by a rule the client's portfolio office already uses keeps scope conversations about scores, not opinions. Respecting dependencies and capacity is what turns a ranking into a plan a team can commit to.

## Revise first (in the course)

- prioritising use cases and managing stakeholders
- ranking a backlog with RICE and dependencies
- why proofs of concept stall, and how scope causes it

## Read the email like an FDE

The programme director gives you the formula and the picking rule in plain words. WSJF is value plus time criticality plus risk reduction, divided by effort, and they want to see the scores. The sprint rule is greedy and repeated: each time, take the best-ranked item whose prerequisites are already in the sprint and that still fits the remaining capacity, and stop only when nothing else fits. 'Still fits' means a large item is skipped, not that planning stops.

## Questions to ask the client first

- **Who scored value, time criticality and risk reduction, and when?** Stale or one-person scores make a precise formula look more objective than it is.
- **Is capacity in story points the team agreed, after holidays and support duty?** A plan built on optimistic capacity fails in the first week.
- **May a large item be split so part of it fits this sprint?** Splitting is often better than skipping the most valuable work.

## How each criterion is checked

1. **WSJF scores are right:** wsjf is called for every backlog item and the rounded scores must match, in backlog order.
2. **A 13-point sprint is planned in pick order:** plan with 13 points must return the items in the order they are picked, not sorted by score afterwards.
3. **A dependency is never picked before its prerequisite:** plan with 21 points must include an item only after its prerequisite has been picked.
4. **Big items are skipped when they don't fit:** With 21 points the largest item must still be left out because it never fits.
5. **A tiny sprint takes what fits:** plan with 2 points must return an empty list because no item is that small.

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
| An item appears before its prerequisite | The backlog was sorted by score once and walked in that order. | Recompute which items are ready after every pick. |
| Planning stops early | The loop ended at the first item that did not fit. | Skip items that do not fit; stop only when no ready item fits. |
| Scores differ in the second decimal | Rounding happened before dividing, or not at all. | Divide first, round the result to two places. |
| Ties pick a different item | The tie-break was left to sort order. | Break ties by id explicitly. |

## Test yourself before you check

- Write the WSJF scores in a table by hand and rank them.
- Walk the 13-point sprint on paper: capacity left after each pick, and why each next item is ready.
- Remove a dependency from the data and see the plan change.
- Try a capacity of 100 and check that only the never-fitting items are missing.

## What a senior reviewer also looks for

A reviewer would ask for the plan to explain itself: for each skipped item, why (does not fit, prerequisite missing). They would also check that the backlog is not modified while planning and that the formula is written once, named, so the portfolio office can see it matches their rule.

## Stretch goal

Return, next to the plan, the items left out with the reason for each, and the capacity left unused, ready to paste into the sprint-planning notes.
