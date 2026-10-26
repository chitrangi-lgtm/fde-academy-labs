import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

data = json.load(open("policies.json"))
policies, query = data["policies"], data["query"]

def rrf(rankings, k=60):
    """Reciprocal rank fusion: each list adds 1 / (k + rank) to an id's score (rank starts at 1). Ids, best first."""
    return []

def hybrid(query, tenant, top=3):
    """Filter to the tenant, rank by TF-IDF and by cosine of the vectors, fuse with rrf, return the top ids."""
    return []

print(hybrid(query, "harbor"))
