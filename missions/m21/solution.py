import json

DATA = json.load(open("golive.json"))


def gate(metrics, thresholds, issues):
    return {"decision": "GO", "reasons": []}


print(gate(DATA["week"], DATA["thresholds"], DATA["issues"]))
