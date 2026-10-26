import json

RULES = json.load(open("rules.json"))
BASELINE = {"requests": 20000, "errors": 100, "p95_ms": 1200, "eval_score": 0.91}


def canary_decision(baseline, canary, rules):
    return "promote", []


def next_stage(pct):
    return 100
