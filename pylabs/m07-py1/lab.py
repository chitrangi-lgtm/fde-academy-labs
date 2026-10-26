import json
import numpy as np

data = json.load(open("embeddings.json"))
docs, queries = data["docs"], data["queries"]
for d in docs:
    print(d["id"], d["text"], "length", round(float(np.linalg.norm(d["vec"])), 2))

def cosine(a, b):
    """Cosine similarity of two vectors."""
    return 0.0

def top_k(query_vec, k=3):
    """The ids of the k documents most similar to query_vec by cosine, best first."""
    return []

dot_winner = ""   # the id that wins for the 'refund' query if you rank by the plain dot product instead
