# Hybrid retrieval: TF-IDF plus vectors, fused with RRF

**Libraries:** scikit-learn, NumPy · **Level:** Intermediate · about 40 minutes

Harbor Group's policy assistant must answer 'per diem for overnight travel' from its own policies only. Keyword search misses paraphrases and vector search misses exact table terms, so the team wants both, fused with reciprocal rank fusion, and a tenant filter applied before ranking so another company's policy can never appear.

Write your code in `lab.py`, then run `python tools/fde_check.py m14-py1` from the kit's folder.

<details><summary>Hints</summary>

1. RRF: for each list, `for rank, id in enumerate(lst, 1): score[id] += 1 / (k + rank)`; sort by score.
2. Filter first: `docs = [p for p in policies if p['tenant'] == tenant]`. Fit the TfidfVectorizer on those texts, then score the query with `(X @ q.T)`.
3. Vector ranking: cosine between `query['vec']` and each `p['vec']`; then `rrf([keyword_ids, vector_ids])[:top]`.
</details>

## Why it matters

Hybrid retrieval is the default for enterprise RAG: keywords catch exact terms, vectors catch paraphrases, and RRF fuses ranks without tuning score scales. Tenant filtering belongs before ranking, never after.
