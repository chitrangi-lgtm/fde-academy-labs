import json

BACKLOG = json.load(open("backlog.json"))
for item in BACKLOG:
    print(item["id"], item["title"])


def wsjf(item):
    return 0.0


def plan(backlog, capacity):
    return []
