# Lab 10: Tenant-safe retrieval with citations in LlamaIndex

**Time:** 60 minutes · **Level:** Intermediate · **Builds on:** FDE Module 14 (enterprise RAG), Agentic Module 5 (agentic retrieval), P1.2 (vector databases)

## The problem

FDE Academy's simulated companies share one policy assistant. CrestFin (a lender) and Albion Mutual (a health insurer)
each have their own policies in the same index. Two failures would end the engagement:

- An answer to a CrestFin user quoting Albion's policy, which is a data leak between clients.
- A confident answer with no source, so a compliance reviewer can't check it.

The client asks for answers that cite numbered sources. Retrieval must be filtered by tenant before the model sees
anything, and when the tenant's documents don't cover a question, the assistant must say so rather than guess.

## What you'll learn

- LlamaIndex's building blocks: `Document`, nodes, embeddings, `VectorStoreIndex`, retrievers and query engines.
- How metadata filters restrict retrieval to one tenant, and why the filter belongs in the retriever, not the prompt.
- How `CitationQueryEngine` numbers the sources and asks the model to cite them.
- How to plug in your own embedding and model classes, so the same code runs offline and with a real provider.

## Before you start

Run `docker compose exec labs python 10_llamaindex_rag.py` from `realtools/`, or run it in a local virtual environment
with `requirements.txt` installed. Nothing is downloaded: the embedding is the deterministic toy embedding from
`common.py`, and the model is a scripted reader that answers from the best-matching source. Set `FDE_LLM_BASE_URL` and
`FDE_LLM_MODEL` to use a real model.

## Key ideas

**Documents, nodes and metadata.** Each policy becomes a `Document` with metadata (`policy_id`, `tenant`). LlamaIndex
splits documents into nodes, which are the units it embeds and retrieves, and copies the metadata onto every node. That
copy is what makes filtering possible.

**Embeddings decide what is "close".** `ToyEmbedding` hashes words into 64 numbers. It is good enough to show the
mechanics, and bad at synonyms: "LTV" and "loan-to-value" look unrelated to it. In client work you swap in a real
embedding model, and you keep one embedding model per index.

**Filter in the retriever.** `MetadataFilters(filters=[ExactMatchFilter(key="tenant", value=tenant)])` is applied when
the vector store searches, so other tenants' nodes are never candidates. A prompt instruction like "only use CrestFin
documents" is not a control, because the model has already seen the text.

**Citations are a contract.** `CitationQueryEngine` labels each retrieved chunk "Source 1", "Source 2" and so on, and
its prompt asks for answers that cite those numbers. Your application can then show the policy ID behind each number.
It can also reject an answer that cites nothing.

**Refuse when the sources don't cover the question.** The second question in the lab asks CrestFin's index about
oncology claims. The top-ranked CrestFin sources score near zero and are unrelated, so the reader answers "the sources
provided don't cover this". The assertion at the end of `ask()` checks that no node from another tenant came back.

## Steps

1. **Run the lab.** Expect three answers:
   - the gold-loan LTV rule with `[1]`, citing POL-7.1;
   - a refusal for CrestFin's oncology question;
   - the clinical-review rule for Albion, citing AMH-CL-8.

   Every source line shows the tenant and a similarity score.

2. **Read the scores.** Note the gap between the first and second source in each answer. Add `similarity_top_k=4` and
   watch weaker sources appear. Decide on a score threshold below which you'd rather refuse. LlamaIndex's
   `SimilarityPostprocessor(similarity_cutoff=...)` applies one.

3. **Break the tenant filter on purpose.** Remove `filters=` from `as_retriever` and ask CrestFin's oncology question
   again. The assertion fails because Albion's policy leaks in. Restore the filter. This is the regression test you'd
   keep in CI.

4. **Add a document.** Append a CrestFin policy to `DOCS` in `common.py`, for example: "Gold loans are renewable once,
   for a further 12 months, after re-appraisal." Ask "Can a gold loan be renewed?". Check that the new policy is cited.

5. **Try a synonym.** Ask "What's the maximum LTV on gold loans?". The toy embedding may miss, because "LTV" doesn't
   share words with the policy. Write down what a real embedding model would fix, and what a query-rewrite step or
   hybrid keyword search would fix. FDE Module 14 covers both.

6. **Use a real model (optional).** Set the `FDE_LLM_*` variables and compare the answers. Check that each answer still
   cites a source number. If the model answers without one, add a post-check that rejects uncited answers.

## Check yourself

<details><summary>Why is the tenant filter applied in the retriever rather than written into the prompt?</summary>
Anything in the prompt has already been shown to the model, so an instruction can't un-leak it, and prompt injection can
override instructions. Filtering at retrieval means other tenants' text never reaches the model.
</details>

<details><summary>What does a citation number prove, and what doesn't it prove?</summary>
It proves which retrieved chunk the model claims to rely on, so a reviewer can check it. It doesn't prove the chunk
actually supports the sentence. For high-stakes answers, add a faithfulness check (P8 and FDE Module 18).
</details>

<details><summary>When should the assistant refuse instead of answering?</summary>
When no retrieved source is relevant enough, or the top sources contradict each other. Then it should explain why and,
in client workflows, route the question to a person.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| Answers cite a source from another client | No metadata filter, or the filter key doesn't match the metadata | Filter in the retriever and test with a cross-tenant question |
| Every answer cites `[1]`, even when wrong | Only one source retrieved, or a weak embedding | Raise `similarity_top_k`, add a score cut-off, use a real embedding model |
| `ValueError` about dimensions after changing the embedding | The index was built with a different embedding size | Rebuild the index when you change embedding models |
| Long policies get cut mid-sentence | Chunk size too small | Tune `citation_chunk_size` and the node parser's chunk size and overlap |

## Take it further

- Persist the index with `index.storage_context.persist("./storage")` and reload it, as you would between deploys.
- Replace the in-memory store with Qdrant from lab 02 (`llama-index-vector-stores-qdrant`) and keep the same filter.
- Add access control by role: a branch officer sees branch policies, a credit officer also sees credit policies.

## In a real client project

- Store `tenant` and access labels on every node, and test the filter in CI with deliberate cross-tenant questions.
- Log the policy IDs behind every answer, so an auditor can reconstruct what the user was shown.
- Re-index when policies change. Version the index so you can say which policy text an old answer used.
