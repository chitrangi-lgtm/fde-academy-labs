# Semantic search with embeddings in NumPy

**Libraries:** NumPy · **Level:** Beginner · about 30 minutes

A help-centre search returns the same long FAQ page for every question. The team ranks documents by the dot product of embedding vectors. Show them why the FAQ page always wins, and rank by cosine similarity instead.

Write your code in `lab.py`, then run `python tools/fde_check.py m07-py1` from the kit's folder. `GUIDE.md` has the ideas, the steps check by check and the common mistakes.

<details><summary>Hints</summary>

1. Cosine is the dot product divided by both lengths: `np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))`.
2. Score every document, then `sorted(docs, key=..., reverse=True)` and keep the first k ids.
3. For dot_winner, rank by `np.dot(query, d['vec'])` alone: the longest vector wins, which is the bug.
</details>

## Why it matters

Dot products reward long vectors, so a page that mentions everything wins everything. Cosine (or normalising embeddings once, at indexing time) ranks by direction, which is meaning.
