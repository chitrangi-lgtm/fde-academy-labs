import json
import re


def extract(raw):
    return json.loads(raw)


def parse_ticket(raw):
    return extract(raw), []


def retry_prompt(errors):
    return ""


print(parse_ticket('{"ticket_id": "TCK-1", "priority": "high", "summary": "Card declined"}'))
