import json

OLD, NEW = json.load(open("v1.json")), json.load(open("v2.json"))


def breaking_changes(old, new):
    return []


for line in breaking_changes(OLD, NEW):
    print(line)
