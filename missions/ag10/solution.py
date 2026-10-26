import json

RUNS = json.load(open("runs.json"))
print(len(RUNS), "runs")


def evaluate(runs):
    return {}


def unreliable(runs):
    return []
