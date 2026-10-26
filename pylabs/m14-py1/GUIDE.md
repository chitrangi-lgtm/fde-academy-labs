# Self-study guide: Hybrid retrieval: TF-IDF plus vectors, fused with RRF

Harbor Group's policy assistant must answer 'per diem for overnight travel' from its own policies only. policies.json holds policies from two companies, each with an id, a tenant, its text and a short vector, plus the query as text and as a vector. Keyword search misses paraphrases and vector search misses exact table terms, so you build both, fuse them with reciprocal rank fusion, and filter by tenant before ranking.

## Revise first (in the course)

- hybrid retrieval and reciprocal rank fusion
- reciprocal rank fusion
- access control before retrieval

## Questions to ask the client first

- **Where does the tenant come from: the signed-in user, or the question?** The tenant must come from identity; a filter set from text can be talked around.
- **Which matters more for your users: exact terms or paraphrases?** Weights between keyword and vector results should reflect real questions.
- **How many policies will each tenant have next year?** Fitting TF-IDF per query is fine for dozens of documents, not for millions.

## Ideas you will use

- **TF-IDF:** Scores how important each word is in a document compared with all documents. TfidfVectorizer turns texts into vectors of those scores; the query's TF-IDF vector times each document's gives a keyword score.
- **Dense vectors:** Embedding vectors capture meaning, so 'overnight travel allowance' can match 'per diem' without sharing a word. Cosine similarity ranks them by direction.
- **Reciprocal rank fusion:** Each ranking adds 1 / (k + rank) to every id it contains, with rank starting at 1 and k usually 60. It uses positions, not scores, so keyword and vector scores on different scales can be combined without tuning.
- **Filter before ranking:** Removing other tenants' policies before any scoring means they can never appear, whatever k you ask for. Filtering after taking the top results can leak or come back short.

## Steps, check by check

1. **RRF rewards ids that rank well in both lists:** Write rrf: add 1 / (k + rank) for every id in every ranking and return the ids by total, best first.
2. **The two per diem policies come first:** In hybrid, keep the tenant's policies, rank them by TF-IDF and by vector cosine, fuse the two rankings and return the top ids: the two per diem policies come first.
3. **Another tenant's policy never appears:** Make sure the other company's policies never appear, even when asking for six results.
4. **The other tenant gets its own per diem policy:** Check that the other company's own per diem policy comes first for its tenant.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If the per diem policies are not first, print both rankings before fusing and see which one misplaces them. If another tenant appears, look at where the filter happens. If rrf gives the wrong order on the small example, compute its scores by hand: rank starts at 1, not 0. With k at 60 the differences between scores are small, so print them with several decimals before deciding they are equal.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| The other tenant appears with k=6 | The filter ran after ranking. | Filter by tenant before any scoring. |
| rrf order is wrong on the example | Ranks started at 0. | Count ranks from 1. |
| TF-IDF gives every document zero | The vectorizer was fitted on the query only. | Fit on the tenant's policy texts, then transform the query. |
| Vector scores favour long vectors | The plain dot product was used. | Use cosine similarity. |

## What the result means for the client

Hybrid retrieval finds both per diem policies, the one with the exact table term and the paraphrased one, and the tenant filter guarantees another company's policy can never reach the answer. Tell the client both properties together: better answers and a hard isolation guarantee, which their security team will ask about.

## What to send the client

The top results for the per diem question for both tenants, a sentence on why hybrid retrieval found the paraphrased policy, and a statement that the tenant filter runs before any ranking.

## Stretch goal

Add a weight to each ranking in rrf (for example 2 for keywords and 1 for vectors) and show how the top three change, then write one sentence on how you would choose the weights with real questions.
