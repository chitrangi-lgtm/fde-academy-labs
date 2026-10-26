"""Lab 09 — A Hugging Face smolagents ToolCallingAgent that checks a supplier invoice for sales tax (scripted model offline).

Run:   docker compose exec labs python 09_smolagents_agent.py
With a real model (any OpenAI-compatible endpoint):
       docker compose exec -e FDE_LLM_BASE_URL=http://host.docker.internal:11434/v1 -e FDE_LLM_MODEL=qwen2.5:7b labs python 09_smolagents_agent.py
Guide: guides/09_smolagents_agent.md (the problem, the concepts, step-by-step tasks, expected output and common mistakes)

The same tool-calling loop you built from scratch in Agentic Module 1, now with a framework: smolagents turns typed,
documented Python functions into tools, asks the model which to call, runs them, feeds the results back, and stops when
the model calls the built-in final_answer tool or max_steps is reached.
"""

from __future__ import annotations

import json
import os
from typing import Any, List, Optional

from smolagents import ChatMessage, Model, OpenAIServerModel, ToolCallingAgent, tool
from smolagents.models import ChatMessageToolCall, ChatMessageToolCallFunction, MessageRole

# A tiny stand-in for the sales tax registry and the tariff schedule. In a client project these are API calls with timeouts.
TAX_ID_REGISTRY = {
    "TX272082027": {"name": "Summit Agro Foods", "region": "West", "status": "Active"},
    "TX297674749": {"name": "Harbor Spice Traders", "region": "South", "status": "Cancelled"},
}
HS_RATES = {"0904": 5.0, "2008": 12.0, "8471": 18.0}


@tool
def lookup_tax_id(tax_id: str) -> dict:
    """Look up a sales tax registration number in the registry.

    Args:
        tax_id: The tax ID printed on the invoice (TX followed by 9 digits).
    """
    record = TAX_ID_REGISTRY.get(tax_id.strip().upper())
    return record or {"error": f"Tax ID {tax_id} is not in the registry"}


@tool
def hs_rate(hs_code: str) -> dict:
    """Return the tax rate (percent) for a Harmonized System (HS) code.

    Args:
        hs_code: The 4-digit HS code of the goods.
    """
    code = hs_code.strip()[:4]
    return {"hs_code": code, "rate_percent": HS_RATES[code]} if code in HS_RATES else {"error": f"unknown HS code {hs_code}"}


class ScriptedModel(Model):
    """Plays the model's part so the lab runs offline: it asks for each check once, then gives a final answer."""

    def __init__(self) -> None:
        super().__init__(model_id="scripted")

    def generate(self, messages: List[ChatMessage], stop_sequences: Optional[List[str]] = None, response_format: Any = None,
                 tools_to_call_from: Any = None, **kwargs: Any) -> ChatMessage:
        transcript = " ".join(str(m.content) if not isinstance(m, dict) else str(m.get("content")) for m in messages)
        if "Harbor Spice Traders" not in transcript and "not in the registry" not in transcript:
            return self._call("lookup_tax_id", {"tax_id": "TX297674749"})
        if "rate_percent" not in transcript:
            return self._call("hs_rate", {"hs_code": "0904"})
        verdict = ("Hold the invoice: the supplier's tax ID TX297674749 (Harbor Spice Traders) is Cancelled, so input tax "
                   "credit can't be claimed. The 5% rate on HS code 0904 (pepper) matches the invoice.")
        return self._call("final_answer", {"answer": verdict})

    @staticmethod
    def _call(name: str, args: dict) -> ChatMessage:
        call = ChatMessageToolCall(id=f"call_{name}", type="function", function=ChatMessageToolCallFunction(name=name, arguments=args))
        return ChatMessage(role=MessageRole.ASSISTANT, content="", tool_calls=[call])


def make_model() -> Model:
    base, model = os.getenv("FDE_LLM_BASE_URL"), os.getenv("FDE_LLM_MODEL")
    if base and model:
        return OpenAIServerModel(model_id=model, api_base=base, api_key=os.getenv("FDE_LLM_API_KEY", "not-needed"))
    return ScriptedModel()


if __name__ == "__main__":
    agent = ToolCallingAgent(tools=[lookup_tax_id, hs_rate], model=make_model(), max_steps=5, verbosity_level=1)
    task = ("Invoice INV-2207 from tax ID TX297674749 charges 5% sales tax on 200 kg of black pepper (HS code 0904). "
            "Check the supplier's registration and the rate, then say whether accounts can pay it and claim the credit.")
    answer = agent.run(task)
    print("\nFINAL ANSWER:", answer)
    steps = [s for s in agent.memory.steps if getattr(s, "tool_calls", None)]
    print("tool calls:", json.dumps([c.name for s in steps for c in s.tool_calls]))
