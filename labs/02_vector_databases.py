"""Lab 02 — the same tenant-filtered search in Qdrant and in PostgreSQL + pgvector.

Run:   docker compose exec labs python 02_vector_databases.py
Compare the results, the latency and the operational work. Then write a short architecture decision record: which would
you choose for CrestFin, and why?
"""

from __future__ import annotations

import os
import time

import psycopg
from qdrant_client import QdrantClient, models

from common import DIM, DOCS, embed

QUERY, TENANT, K = "what is the maximum loan to value for gold", "crestfin", 2


def qdrant_search() -> list:
    client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
    name = "policies"
    if client.collection_exists(name):
        client.delete_collection(name)
    client.create_collection(name, vectors_config=models.VectorParams(size=DIM, distance=models.Distance.COSINE))
    client.create_payload_index(name, field_name="tenant", field_schema=models.PayloadSchemaType.KEYWORD)
    client.upsert(name, points=[models.PointStruct(id=i, vector=embed(d["text"]), payload=d) for i, d in enumerate(DOCS)])
    t0 = time.perf_counter()
    res = client.query_points(name, query=embed(QUERY), limit=K, query_filter=models.Filter(
        must=[models.FieldCondition(key="tenant", match=models.MatchValue(value=TENANT))]))
    ms = (time.perf_counter() - t0) * 1000
    return [(p.payload["id"], round(p.score, 3)) for p in res.points], ms


def pgvector_search() -> list:
    with psycopg.connect(os.getenv("PG_DSN", "postgresql://fde:fde_local_only@localhost:5432/fde"), autocommit=True) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute("DROP TABLE IF EXISTS chunks")
        conn.execute(f"CREATE TABLE chunks (id text PRIMARY KEY, tenant text NOT NULL, content text, embedding vector({DIM}))")
        conn.execute("CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops)")
        for d in DOCS:
            conn.execute("INSERT INTO chunks VALUES (%s, %s, %s, %s::vector)", (d["id"], d["tenant"], d["text"], str(embed(d["text"]))))
        t0 = time.perf_counter()
        rows = conn.execute("SELECT id, round((1 - (embedding <=> %s::vector))::numeric, 3) FROM chunks WHERE tenant = %s "
                            "ORDER BY embedding <=> %s::vector LIMIT %s", (str(embed(QUERY)), TENANT, str(embed(QUERY)), K)).fetchall()
        ms = (time.perf_counter() - t0) * 1000
    return [(r[0], float(r[1])) for r in rows], ms


if __name__ == "__main__":
    for name, fn in (("Qdrant", qdrant_search), ("pgvector", pgvector_search)):
        hits, ms = fn()
        print(f"{name:9} {ms:6.1f} ms  {hits}")
