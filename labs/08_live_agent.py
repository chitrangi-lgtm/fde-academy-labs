"""Lab 08 — A LangGraph agent loop against a real language model (or a scripted one when you have none).

Run:   docker compose exec labs python 08_live_agent.py
With a real model (any OpenAI-compatible endpoint: OpenAI, Azure OpenAI, a local vLLM or Ollama server):
       docker compose exec -e FDE_LLM_BASE_URL=http://host.docker.internal:11434/v1 -e FDE_LLM_MODEL=qwen2.5:7b labs python 08_live_agent.py
       (add -e FDE_LLM_API_KEY=... for hosted providers; the key is read from the environment, never written to code)
Try:   ask a question that needs both tools; remove the step limit and watch a confused model loop; add a node that refuses
       any tool the plan didn't mention.

This is the Module 1 agent loop (and the ag01 client project) as a LangGraph graph: a model node, a tools node, and a
conditional edge that decides whether to run a tool or stop.
"""

from __future__ import annotations

import json
import os
import urllib.request
from typing import List, TypedDict

from langgraph.graph import END, START, StateGraph

MAX_STEPS = 5
TOOLS = {
    "order_status": lambda order_id="": {"order_id": order_id, "status": "shipped", "eta_days": 2},
    "refund_policy": lambda: {"days": 7, "condition": "unused, in the original packaging"},
}
SYSTEM = ("You are a support agent. Tools: order_status(order_id), refund_policy(). "
          'To use a tool, reply ONLY with JSON like {"tool": "order_status", "args": {"order_id": "A12"}}. '
          'When you can answer, reply ONLY with JSON like {"answer": "..."}.')


class State(TypedDict):
    messages: List[dict]
    steps: int


def chat(messages: List[dict]) -> str:
    """The configured OpenAI-compatible model, or a scripted stand-in so the lab runs offline."""
    base, model = os.getenv("FDE_LLM_BASE_URL"), os.getenv("FDE_LLM_MODEL")
    if not (base and model):
        if not any(m["content"].startswith("Tool result") for m in messages):
            return '{"tool": "order_status", "args": {"order_id": "A12"}}'
        if sum(m["content"].startswith("Tool result") for m in messages) == 1:
            return '{"tool": "refund_policy", "args": {}}'
        return '{"answer": "Order A12 has shipped and arrives in 2 days; you can return it within 7 days if unused."}'
    headers = {"Content-Type": "application/json"}
    if os.getenv("FDE_LLM_API_KEY"):
        headers["Authorization"] = "Bearer " + os.environ["FDE_LLM_API_KEY"]
    body = json.dumps({"model": model, "messages": messages, "temperature": 0.2, "max_tokens": 200}).encode()
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"]


def first_json(text: str) -> dict:
    start, end = text.find("{"), text.rfind("}")
    try:
        return json.loads(text[start:end + 1]) if start >= 0 else {"answer": text}
    except json.JSONDecodeError:
        return {"answer": text}


def model_node(state: State) -> State:
    reply = chat(state["messages"])
    print(f"model (step {state['steps'] + 1}): {reply.strip()}")
    return {"messages": state["messages"] + [{"role": "assistant", "content": reply}], "steps": state["steps"] + 1}


def tools_node(state: State) -> State:
    call = first_json(state["messages"][-1]["content"])
    tool = TOOLS.get(call.get("tool"))
    try:
        result = tool(**call.get("args", {})) if tool else {"error": f"unknown tool {call.get('tool')}"}
    except TypeError as exc:
        result = {"error": str(exc)}
    print(f"tool {call.get('tool')}: {result}")
    return {"messages": state["messages"] + [{"role": "user", "content": "Tool result: " + json.dumps(result)}], "steps": state["steps"]}


def route(state: State) -> str:
    decision = first_json(state["messages"][-1]["content"])
    return "tools" if "tool" in decision and state["steps"] < MAX_STEPS else END


def build():
    g = StateGraph(State)
    g.add_node("model", model_node)
    g.add_node("tools", tools_node)
    g.add_edge(START, "model")
    g.add_conditional_edges("model", route, {"tools": "tools", END: END})
    g.add_edge("tools", "model")
    return g.compile()


if __name__ == "__main__":
    goal = "Where is order A12, and can I still return it if I don't like it?"
    final = build().invoke({"messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": goal}], "steps": 0})
    answer = first_json(final["messages"][-1]["content"]).get("answer", final["messages"][-1]["content"])
    print(f"\nanswer after {final['steps']} model calls: {answer}")
