DOCS = {
    "L1": "termination of employment contract notice period",
    "L2": "notice period for residential tenancy termination",
    "L3": "data breach notification deadline regulator",
    "L4": "employee dismissal procedure and appeal rights",
}
STOPWORDS = {"what", "is", "the", "for", "a", "an", "of", "in", "on", "to", "how", "do", "i", "my"}
SYNONYMS = {"firing": "dismissal", "staff": "employee", "lease": "tenancy", "leak": "breach"}


def search(query):
    """Ids of documents containing every word of the query."""
    words = query.split()
    return [d for d, text in DOCS.items() if all(w in text.split() for w in words)]
