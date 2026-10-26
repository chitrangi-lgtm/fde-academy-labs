import json

MERGES = [tuple(m) for m in json.load(open("merges.json"))]
print(MERGES)


def bpe(word, merges):
    return list(word)


def count_tokens(text, merges):
    return 0


def pack(chunks, budget, merges):
    return []
