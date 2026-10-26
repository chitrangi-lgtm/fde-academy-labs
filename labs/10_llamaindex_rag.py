"""Lab 10 — LlamaIndex: tenant-filtered retrieval with numbered citations, and a refusal when the sources don't cover it.

Run:   docker compose exec labs python 10_llamaindex_rag.py
With a real model (any OpenAI-compatible endpoint):
       docker compose exec -e FDE_LLM_BASE_URL=http://host.docker.internal:11434/v1 -e FDE_LLM_MODEL=qwen2.5:7b labs python 10_llamaindex_rag.py
Guide: guides/10_llamaindex_rag.md

FDE Module 14 and Agentic Module 5 with a framework. LlamaIndex splits documents into nodes, embeds them, retrieves the
closest ones for a question, and asks the model to answer only from numbered sources. Two things matter in client work:
the tenant filter (CrestFin must never see Albion's policies) and citations a reviewer can check. The embedding is the
toy one from common.py, so nothing is downloaded; the model is scripted unless you point the lab at a real one.
"""

from __future__ import annotations

import json
import os
import re
import urllib.request
from typing import Any, List

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.llms import CompletionResponse, CompletionResponseGen, CustomLLM, LLMMetadata
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters

from common import DOCS, embed

STOP = set("a an and are can do does for how i in is it of on the to what when which who will with".split())


class ToyEmbedding(BaseEmbedding):
    """The deterministic hashing embedding from common.py, wrapped for LlamaIndex."""

    def _get_query_embedding(self, query: str) -> List[float]:
        return embed(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        return embed(text)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return embed(query)


class CourseLLM(CustomLLM):
    """The configured OpenAI-compatible model; offline, a scripted reader that answers from the best-matching source."""

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(model_name=os.getenv("FDE_LLM_MODEL") or "scripted", context_window=8192, num_output=256)

    def complete(self, prompt: str, formatted: bool = False, **kwargs: Any) -> CompletionResponse:
        base, model = os.getenv("FDE_LLM_BASE_URL"), os.getenv("FDE_LLM_MODEL")
        if base and model:
            headers = {"Content-Type": "application/json"}
            if os.getenv("FDE_LLM_API_KEY"):
                headers["Authorization"] = "Bearer " + os.environ["FDE_LLM_API_KEY"]
            body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 256}).encode()
            req = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp:
                return CompletionResponse(text=json.loads(resp.read())["choices"][0]["message"]["content"])
        return CompletionResponse(text=self._scripted(prompt))

    def stream_complete(self, prompt: str, formatted: bool = False, **kwargs: Any) -> CompletionResponseGen:
        yield self.complete(prompt)

    @staticmethod
    def _scripted(prompt: str) -> str:
        query = prompt.rsplit("Query:", 1)[-1].split("Answer:")[0]
        sources = re.findall(r"Source (\d+):\n(.*?)(?=\n\n|\n------)", prompt, re.S)   # each source's text ends at a blank line
        words = {w for w in re.findall(r"[a-z0-9%]+", query.lower()) if w not in STOP}
        best = max(sources, key=lambda s: len(words & set(re.findall(r"[a-z0-9%]+", s[1].lower()))), default=None)
        if not best or len(words & set(re.findall(r"[a-z0-9%]+", best[1].lower()))) < 2:
            return "The sources provided don't cover this, so I can't answer it."
        return f"{best[1].strip()} [{best[0]}]"


def build_index() -> VectorStoreIndex:
    Settings.embed_model = ToyEmbedding()
    Settings.llm = CourseLLM()
    docs = [Document(text=d["text"], metadata={"policy_id": d["id"], "tenant": d["tenant"]}, doc_id=d["id"]) for d in DOCS]
    return VectorStoreIndex.from_documents(docs)


def ask(index: VectorStoreIndex, tenant: str, question: str) -> None:
    retriever = index.as_retriever(similarity_top_k=2, filters=MetadataFilters(filters=[ExactMatchFilter(key="tenant", value=tenant)]))
    engine = CitationQueryEngine.from_args(index, retriever=retriever, citation_chunk_size=256)
    response = engine.query(question)
    print(f"\n[{tenant}] Q: {question}\nA: {response}")
    for i, node in enumerate(response.source_nodes, 1):
        meta = node.node.metadata
        print(f"   source {i}: {meta['policy_id']} (tenant {meta['tenant']}, score {node.score:.2f})")
    assert all(n.node.metadata["tenant"] == tenant for n in response.source_nodes), "a source from another tenant leaked"


if __name__ == "__main__":
    index = build_index()
    ask(index, "crestfin", "What is the maximum loan-to-value for a gold loan?")
    ask(index, "crestfin", "Do oncology claims go to clinical review?")      # Albion's policy: must not be visible to CrestFin
    ask(index, "albion", "Do oncology claims go to clinical review?")
