# Beat a rules baseline with logistic regression

**Libraries:** scikit-learn, pandas · **Level:** Intermediate · about 40 minutes

Harbor Payments flags a card payment as fraud when the amount is over 900 dollars. Their fraud team says the rule misses most real fraud, which happens at night on new devices. Train a model on the first 60 payments, test it on the last 20, and show the team, with the same metric for both, whether the model beats the rule.

Write your code in `lab.py`, then run `python tools/fde_check.py m06-py1` from the kit's folder. `GUIDE.md` has the ideas, the steps check by check and the common mistakes.

<details><summary>Hints</summary>

1. Amount is in hundreds and hour in units: put a `StandardScaler` in front of the model with `make_pipeline(StandardScaler(), LogisticRegression())`.
2. Fit on `train[features]` and `train['fraud']`; predict on `test[features]`.
3. Read the confusion matrix as [[true negatives, false positives], [false negatives, true positives]]: the team cares most about the bottom-left number.
</details>

## Why it matters

Always compare a model with the client's current rule on the same held-out data and the same metric. Scaling features matters for linear models, and the confusion matrix is what the business reads.
