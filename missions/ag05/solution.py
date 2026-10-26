from provided import *  # the client's code (the checker runs provided.py first)

import re


def keywords(question):
    return question.lower().split()


def answer(question, search, max_searches=3):
    results = search(" ".join(keywords(question)))
    return {"found": bool(results), "citations": results, "searches": []}


print(answer("What is the notice period for termination?", search))
