# Lab 02: The same tenant-filtered search in Qdrant and pgvector

**Time:** 75 minutes · **Level:** Intermediate · **Builds on:** Professional Practice P1, FDE Module 14 (retrieval-augmented generation), Agentic Module 5 (retrieval agents)

## The problem

A platform serves three clients from one assistant: CrestFin (lending), Albion (health insurance) and Lakeshore
(hospital robots). Their policy documents sit in one vector store. A CrestFin user must never receive an Albion
document, even if it happens to be the closest match. The architecture review wants to know which vector database to
use, and whether it enforces the tenant filter properly.

You'll load the same six documents into **Qdrant**, a dedicated vector database, and **PostgreSQL with pgvector**, a
vector extension for a database most clients already run. Then you'll run the same filtered search in both and write an
architecture decision record (ADR).

## What you'll learn

- How to create a collection or table with a vector size and a distance measure (cosine).
- How to filter by tenant in each database: a payload filter in Qdrant, a `WHERE` clause in SQL.
- Why the filter must be part of the search, not applied to results afterwards.
- How to compare two options on results, latency and the operational work, and record the decision.

## Before you start

1. From `realtools/`: `docker compose up -d --build`. This starts Qdrant on port 6333 and PostgreSQL with pgvector on 5432.
2. Run `docker compose exec labs python 02_vector_databases.py`.
3. Without Docker you need both servers running locally; set `QDRANT_URL` and `PG_DSN` to point at them.

The embeddings come from `common.embed`, a toy 64-dimension embedding based on word hashing, so nothing is downloaded.
It's good enough to show the mechanics; a real project would use an embedding model.

## Key ideas

**Cosine similarity compares direction.** Both stores use cosine. Qdrant reports a similarity score (higher is closer).
pgvector's `<=>` operator returns cosine *distance*, so the query prints `1 - distance` to show the same similarity.

**The tenant filter belongs inside the query.** Qdrant's `query_filter` with a `FieldCondition` on `tenant`, and SQL's
`WHERE tenant = %s`, restrict the search itself. If you searched everything and filtered afterwards, a query could
return fewer results than asked for, or a mistake in the filtering code could leak another tenant's text.

**Index the filter field.** `create_payload_index` on `tenant` lets Qdrant filter efficiently during the vector search.
In PostgreSQL, the `hnsw` index speeds up the vector part; on a large table, an ordinary index on `tenant` or a
partition per tenant helps the filter.

**Operations matter as much as speed.** Qdrant is another service to run, secure, back up and monitor. pgvector lives
in a database the client already backs up and audits, with transactions and joins. At the scale of most enterprise
pilots (thousands to a few million chunks), both are fast enough, so the decision is usually about operations.

## Steps

1. **Run the lab.** Expected output (latencies vary on your machine):
   `Qdrant      4.2 ms  [('POL-7.1', 0.624), ('POL-4.2', 0.126)]` and
   `pgvector    1.8 ms  [('POL-7.1', 0.624), ('POL-4.2', 0.126)]`. Both return the gold-loan policy POL-7.1 first,
   with the same scores, and only CrestFin documents.

2. **Check the filter works.** Change `TENANT` to `"albion"` and run again. Both should return only AMH-CL-3 and
   AMH-CL-8, even though they're poor matches for a gold-loan question. That is correct: an unrelated document from the
   right tenant is better than a relevant one from the wrong tenant.

3. **Remove the filter.** Comment out `query_filter=...` in Qdrant and the `WHERE tenant = %s` in SQL (adjust the
   parameters). Change `TENANT` back and ask an insurance question, such as `"physiotherapy pre-authorisation"`. See an
   Albion document returned for a CrestFin user. Put the filters back.

4. **Look inside each store.** Open the Qdrant dashboard at <http://localhost:6333/dashboard> and inspect the `policies`
   collection. Then connect to PostgreSQL (`docker compose exec postgres psql -U fde`) and run
   `SELECT id, tenant FROM chunks;`.

5. **Compare latency honestly.** Run the lab five times and note the range. With six documents the numbers mostly show
   network and connection overhead, not search speed. Write down what you would need to measure properly (realistic
   data volume, concurrent queries, p95 latency).

6. **Write the ADR.** In half a page: the context (multi-tenant, CrestFin's existing PostgreSQL estate), the options,
   your decision, and the consequences, including who runs and backs up the store.

## Check yourself

<details><summary>Why are the scores identical in both databases?</summary>
Both store the same vectors and compute the same cosine similarity. The databases differ in how they index and filter,
not in the maths, so on a small exact search the results match.
</details>

<details><summary>What is wrong with filtering by tenant after the search?</summary>
The top results might all belong to other tenants, leaving you with fewer than K results or none. Worse, other tenants'
text has already been read by your service, and a bug in the filtering code would leak it.
</details>

<details><summary>When would you pick Qdrant over pgvector?</summary>
When vector search is the main workload at large scale (tens of millions of vectors or more), when you need features such
as advanced filtering, quantization or hybrid search tuned for vectors, and the client is willing to run another service.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `Connection refused` on 6333 or 5432 | The services aren't running | `docker compose up -d` and check `docker compose ps` |
| `type "vector" does not exist` | The extension isn't enabled | The lab runs `CREATE EXTENSION IF NOT EXISTS vector`; make sure you use the `pgvector/pgvector` image |
| `expected 64 dimensions, not ...` | Vectors of a different size from the column or collection | Keep one embedding model and dimension per collection |
| Results include another tenant | The filter was removed or applied to results afterwards | Put the tenant condition inside the search query |

## Take it further

- Add a `created_at` field and filter to documents from the last year as well as the tenant.
- Load 50,000 synthetic chunks and measure p95 latency for both, with and without the HNSW index.
- Use PostgreSQL row-level security so the tenant filter is enforced by the database for each connection's user.

## In a real client project

- Take the tenant from the user's verified identity token, never from the request body.
- Back up the vector store with the same schedule and retention as the source documents.
- Re-embed everything when you change the embedding model; mixing models in one collection gives meaningless scores.
