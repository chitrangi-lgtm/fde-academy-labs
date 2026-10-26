# Table-aware chunking with tenant-safe retrieval

**From:** Noor Rahman, Knowledge Manager, Harbor Group Travel Desk

Our policy assistant answers per diem questions wrongly because our chunker cuts tables apart: a row like "Tier 2 | 70" ends up in a chunk without its header, so the model can't tell it's a nightly rate. And once it quoted another company's policy, because both companies share the index. Please chunk our policy documents so every table row carries its header, search only the asking company's chunks, and return the best chunk with a citation we can show (document id and chunk number).

## Done when

- `chunk(doc)` splits a document's text into paragraphs (blank-line separated); a Markdown table becomes one chunk per data row, each starting with the table's header line
- Every chunk is a dict {"tenant", "doc_id", "n" (1-based within the document), "text"}
- `search(chunks, query, tenant, k=1)` scores chunks of that tenant only, by how many distinct query words (lower case, letters and digits) they contain, ties by doc_id then n, and returns the top k
- `cite(chunk)` returns "[doc_id#n]"

## Files

`policies.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m14
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
