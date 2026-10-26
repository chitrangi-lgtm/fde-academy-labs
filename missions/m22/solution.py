import json
from datetime import datetime, timedelta

CONTRACT = json.load(open("contract.json"))
BATCH = json.load(open("batch.json"))


def violations(contract, records):
    return []


def is_fresh(contract, records, now):
    return True


for v in violations(CONTRACT, BATCH):
    print(v)
