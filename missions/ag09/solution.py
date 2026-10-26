from provided import *  # the client's code (the checker runs provided.py first)

def guard(action, provenance):
    return "allow", "no checks yet"


print(guard({"tool": "forward_email", "args": {"to": ["payments-update@quickmail.example"]}}, "retrieved"))
