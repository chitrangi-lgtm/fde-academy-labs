import json
import re

DOCS = json.load(open("policies.json"))


def chunk(doc):
    return [{"tenant": doc["tenant"], "doc_id": doc["doc_id"], "n": 1, "text": doc["text"]}]


def search(chunks, query, tenant, k=1):
    return []


def cite(chunk):
    return ""


CHUNKS = [c for d in DOCS for c in chunk(d)]
print(len(CHUNKS), "chunks")
