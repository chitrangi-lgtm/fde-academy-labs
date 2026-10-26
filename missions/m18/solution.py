import json
import math

EVAL = json.load(open("eval.json"))
SPANS = json.load(open("spans.json"))


def hit_rate(results, k=3):
    return 0.0


def mrr(results):
    return 0.0


def p95(values):
    return 0


def p95_by_span(spans):
    return {}


def leaks(spans):
    return []
