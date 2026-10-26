# Self-study guide: Beat a rules baseline with logistic regression

Harbor Payments flags a payment as fraud when the amount is over 900 dollars, and the fraud team says the rule misses most real fraud, which happens at night on new devices. fraud.csv has amount, hour of day, new_device (1 for a device never seen before) and fraud (the true outcome). You train on the first 60 payments and test on the last 20, comparing the model with the rule on the same metric.

## Revise first (in the course)

- evaluating classifiers the way the business sees them
- generalisation, overfitting and leakage
- precision, recall and choosing a threshold

## Questions to ask the client first

- **How many alerts a day can the fraud team investigate?** A model that catches more fraud may also raise more alerts than the team can handle.
- **Is the outcome column confirmed fraud or reported fraud?** Labels that are only complaints teach the model the wrong thing.
- **Will the hour be in the customer's time zone or the server's?** 'At night' means different hours for customers in different places.

## Ideas you will use

- **A held-out test set:** The model learns from the training rows and is judged only on rows it has never seen. Judging on training rows would flatter it; the client cares about tomorrow's payments, not last month's.
- **Scaling:** Amount is in hundreds and hour runs from 0 to 23. Logistic regression weighs features by size, so a StandardScaler in a pipeline puts them on the same scale before the model sees them.
- **F1 score:** F1 combines precision (how many flags were real fraud) and recall (how much fraud was flagged) into one number. Comparing the rule and the model on F1 is fair because both use the same test rows.
- **Confusion matrix:** A 2 by 2 table of true negatives, false positives, false negatives and true positives. The bottom-left number, fraud that was missed, is the one the fraud team asks about first.

## Steps, check by check

1. **There is one prediction per test row:** Predict a 0 or 1 for each of the 20 test rows with a model trained only on the first 60 rows.
2. **model_f1 is the F1 of your predictions:** Compute model_f1 from the true outcomes of the test rows and your predictions.
3. **The rule really is weak on this data (F1 under 0.2):** Leave the rule as it is: its F1 on the test rows is low, which is the point of the comparison.
4. **The model reaches F1 of at least 0.6:** Use a scaled logistic regression on all three features so the model reaches an F1 of at least 0.6.
5. **The confusion matrix covers the 20 test rows:** Build the confusion matrix from the test outcomes and your predictions.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If the model's F1 is low, print the predictions next to the true outcomes and look at which fraud it misses. If the F1 check says your number does not match, make sure model_f1 was computed from the same y_pred the checks see, after the final fit. If the confusion matrix check fails, print its shape and its sum: it must be two by two and count exactly the twenty test payments.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| The model flags nothing | Features were not scaled, so the amount dominates. | Put a StandardScaler in front of the logistic regression. |
| F1 looks perfect | The model was scored on the training rows. | Score only the last 20 rows. |
| y_pred has 80 rows | Predictions were made on the whole file. | Predict on the test rows only. |
| confusion_matrix has the wrong layout | The arguments were swapped. | Pass the true outcomes first and the predictions second. |

## What the result means for the client

The model catches far more fraud than the amount rule on payments it has never seen, because it uses the hour and the new-device flag the fraud team already suspected. Present the two confusion matrices side by side: missed fraud and false alarms are the numbers the team will plan around, not F1.

## What to send the client

A one-page comparison for the fraud team: the rule's and the model's confusion matrices side by side, the fraud each one missed, and a recommendation to trial the model in shadow mode before it blocks payments.

## Stretch goal

Print the model's probability for each test payment and find the threshold that keeps false alarms at or below two while catching the most fraud, then explain the trade-off in one sentence.
