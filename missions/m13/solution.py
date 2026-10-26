import json

DATA = json.load(open("models.json"))
MODELS, TRAFFIC = DATA["models"], DATA["traffic"]


def request_cost(model, traffic, cache_hit_rate=0.0):
    return 0.0


def monthly_cost(model, traffic, cache_hit_rate=0.0):
    return 0.0


def cheapest(models, traffic, slo_ms, cache_hit_rate=0.0):
    return None


for m in MODELS:
    print(m["name"], monthly_cost(m, TRAFFIC), monthly_cost(m, TRAFFIC, 0.9))
