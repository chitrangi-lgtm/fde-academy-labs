import csv

with open("scores.csv", newline="") as f:
    ROWS = [(float(r["score"]), int(r["fraud"])) for r in csv.DictReader(f)]
print(len(ROWS), "payments,", sum(f for _, f in ROWS), "fraud")


def confusion(threshold):
    return {"tp": 0, "fp": 0, "fn": 0, "tn": 0}


def precision_recall(threshold):
    return 0.0, 0.0


def alerts_per_day(threshold, daily_volume=10000):
    return 0


def best_threshold(min_precision=0.8):
    return 1.0
