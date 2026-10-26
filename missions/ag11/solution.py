from provided import *  # the client's code (the checker runs provided.py first)

import json
import math

CALLS = json.load(open("calls.json"))


def cost(record):
    return 0.0


def report(records):
    return {}


print(report(CALLS))
