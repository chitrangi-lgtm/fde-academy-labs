import json


def load(path):
    return []


def error_rates(records):
    return {}


def duplicate_creates(records):
    return []


def retryable(status):
    return False


def backoff(attempt, retry_after=None):
    return 0.0


records = load("api_log.jsonl")
print(len(records), "records")
