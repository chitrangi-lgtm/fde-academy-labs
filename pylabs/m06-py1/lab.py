import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score

df = pd.read_csv("fraud.csv")
train, test = df.iloc[:60], df.iloc[60:]
features = ["amount", "hour", "new_device"]

baseline_pred = (test["amount"] > 900).astype(int)
baseline_f1 = f1_score(test["fraud"], baseline_pred, zero_division=0)

# Train a model on `train`, predict on `test`, and fill these in:
y_pred = None       # the model's predictions for the 20 test rows (0 or 1)
model_f1 = 0.0      # the model's F1 score on the test rows
cm = None           # confusion_matrix(test["fraud"], y_pred)
