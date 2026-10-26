# Self-study guide: Choose the alert threshold the fraud team can live with

A fraud model is only switched on when the business accepts its threshold. The fraud team does not think in scores; it thinks in alerts a day and how many of them are false alarms. Turning a model's output into those terms, under a constraint the client sets, is the moment an AI project is accepted or rejected.

## Revise first (in the course)

- evaluating classifiers the way the business experiences them
- precision, recall and choosing a threshold
- a confusion matrix from scratch

## Read the email like an FDE

The head of fraud gives you a constraint and a goal. 'They lose trust when more than one in five alerts is a false alarm' is a precision floor of 0.8. 'Catches the most fraud' is recall, to be made as high as possible under that floor. 'Our volume of 10,000 payments' turns the share flagged into alerts a day, the unit the team plans staff with. 'For any threshold' means your functions take the threshold as an argument, and the rule 'score at or above the threshold is flagged' is in the acceptance criteria.

## Questions to ask the client first

- **How many alerts a day can the team really investigate?** An alert budget is a second constraint that may decide the threshold before precision does.
- **Does last month look like a normal month for fraud?** A threshold tuned on an unusual month will disappoint in the next one.
- **What does a missed fraud cost compared with an investigation?** With costs, the threshold becomes a business optimisation rather than a rule of thumb.

## How each criterion is checked

1. **The confusion matrix at 0.8:** confusion(0.8) must count true positives, false positives, false negatives and true negatives exactly.
2. **Precision and recall at 0.8:** precision_recall(0.8) must return both values rounded to three places.
3. **Precision and recall match at other thresholds:** precision_recall is compared at four more thresholds, including very high ones where nothing may be flagged, so the undefined case must return 0.0 instead of crashing.
4. **Alerts a day at the client's volume:** alerts_per_day must scale the share flagged to 10,000 payments and return a whole number, at two thresholds.
5. **The best threshold keeps precision at 0.8 or better:** best_threshold(0.8) must return the threshold, chosen from the scores in the file, with the highest recall that keeps precision at 0.8 or better.
6. **A stricter precision target moves the threshold up:** best_threshold(0.95) must move to a stricter threshold.

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
| Counts are off by one or two | Flagging used greater-than instead of greater-than-or-equal. | Follow the rule in the criteria: a score equal to the threshold is flagged. |
| ZeroDivisionError at a high threshold | Nothing was flagged, so precision has no denominator. | Return 0.0 when the denominator is zero. |
| best_threshold returns a value not in the file | Thresholds were stepped in fixed increments. | Use the distinct scores themselves as candidates. |
| The tie goes the wrong way | max() picked the first of two equal recalls. | Compare on recall first and the threshold second. |

## Test yourself before you check

- Check that tp + fp + fn + tn equals the number of rows at every threshold.
- Print precision and recall for all thresholds in a small table and find the best one by eye.
- Check that a higher threshold never produces more alerts a day.
- Try best_threshold with a floor of 1.0 and think about what the client should be told.

## What a senior reviewer also looks for

A reviewer would want the table of thresholds in the client's units (alerts a day, fraud caught, false alarms) because that is what the head of fraud will present. They would check that the data is read once, that rounding happens only at the reporting boundary, and that the code says clearly what happens when no threshold meets the floor.

## Stretch goal

Add the cost view: with an investigation cost per alert and an average loss per missed fraud, find the threshold with the lowest total cost, and compare it with the precision-floor choice.
