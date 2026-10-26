import json
import re

DATA = json.load(open("docs.json"))
DOCS, USERS = DATA["docs"], DATA["users"]


def visible(user, docs):
    return sorted(d["id"] for d in docs)


def redact(text):
    return text


print(visible(USERS["intern"], DOCS))
print(redact("Call +1 555 010 0199 or mail jo@ashgrove.example about card 4111 1111 1111 1111, order 1234567890123"))
