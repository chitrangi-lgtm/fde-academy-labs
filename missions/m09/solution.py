import re

LABELS = ["billing", "delivery", "technical", "other"]


def build_messages(ticket, examples):
    """examples: [(ticket_text, label)]. Returns a list of {"role": ..., "content": ...}."""
    return [{"role": "user", "content": ticket}]


def parse_label(reply):
    return reply


print(build_messages("I was charged twice", [("Parcel is late", "delivery")]))
