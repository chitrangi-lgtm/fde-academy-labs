import json
from datetime import datetime
from decimal import Decimal, InvalidOperation


def normalize(record):
    raise ValueError("not written yet")


def load(path):
    good, quarantine = [], []
    return good, quarantine


good, quarantine = load("feed.jsonl")
print(len(good), "good,", len(quarantine), "quarantined")
