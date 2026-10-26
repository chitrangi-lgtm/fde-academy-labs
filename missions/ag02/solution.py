from provided import *  # the client's code (the checker runs provided.py first)

import re


def validate(args, schema):
    return []


def execute(call, registry, approved=False):
    tool = registry[call["tool"]]
    return {"ok": True, "result": tool["fn"](**call["args"])}


print(execute({"tool": "create_refund", "args": {"order_id": "ORD-104233", "amount": 42.5, "currency": "USD"}}, REGISTRY))
