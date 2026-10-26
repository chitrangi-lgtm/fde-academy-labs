"""Lab 12 — Microsoft AutoGen: a writer and a compliance reviewer agree a customer letter in a round-robin team.

Run:   docker compose exec labs python 12_autogen_team.py
With a real model (any OpenAI-compatible endpoint):
       docker compose exec -e FDE_LLM_BASE_URL=http://host.docker.internal:11434/v1 -e FDE_LLM_MODEL=qwen2.5:7b labs python 12_autogen_team.py
Guide: guides/12_autogen_team.md

Agentic Module 7 (multi-agent coordination) with a framework. Two AssistantAgents take turns in a RoundRobinGroupChat:
the writer drafts, the reviewer checks the draft with a wording tool and either asks for changes or says APPROVED. The
team stops on the word APPROVED or after eight messages, whichever comes first, which is the budget guard from the
module. Offline, ReplayChatCompletionClient plays both models from a fixed script, so you can see the protocol exactly.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import FunctionCall
from autogen_core.models import CreateResult, RequestUsage
from autogen_ext.models.replay import ReplayChatCompletionClient

BANNED = ["guarantee", "definitely", "100%", "no questions asked"]


def check_wording(letter: str) -> str:
    """Check a customer letter against the insurer's banned-phrase list (Insurance-regulator fair-treatment rules)."""
    found = [p for p in BANNED if p in letter.lower()]
    return json.dumps({"ok": not found, "banned_phrases": found})


DRAFT_1 = ("Dear Mrs Rossi, your claim C-881 is delayed because the hospital bill is missing. We guarantee it will be paid "
           "within 2 days of receiving the bill.")
DRAFT_2 = ("Dear Mrs Rossi, your claim C-881 is waiting for the hospital's final bill. Once we receive it, we aim to decide "
           "within 2 working days, and we will email you the outcome.")


def tool_call(letter: str) -> CreateResult:
    call = FunctionCall(id="check-1", name="check_wording", arguments=json.dumps({"letter": letter}))
    return CreateResult(finish_reason="function_calls", content=[call], usage=RequestUsage(prompt_tokens=0, completion_tokens=0), cached=False)


INFO = {"vision": False, "function_calling": True, "json_output": False, "family": "unknown", "structured_output": False}


def clients():
    base, model = os.getenv("FDE_LLM_BASE_URL"), os.getenv("FDE_LLM_MODEL")
    if base and model:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        info = INFO
        real = OpenAIChatCompletionClient(model=model, base_url=base, api_key=os.getenv("FDE_LLM_API_KEY", "not-needed"), model_info=info)
        return real, real
    writer = ReplayChatCompletionClient([DRAFT_1, DRAFT_2], model_info=INFO)
    reviewer = ReplayChatCompletionClient([
        tool_call(DRAFT_1), "CHANGES REQUESTED: remove 'guarantee'; promise a decision time, not a payment.",
        tool_call(DRAFT_2), "APPROVED: no banned phrases, and it states what happens next.",
    ], model_info=INFO)
    return writer, reviewer


async def main() -> None:
    logging.getLogger("autogen_core").setLevel(logging.ERROR)     # the replay client warns about token counts on every turn
    writer_model, reviewer_model = clients()
    writer = AssistantAgent("writer", model_client=writer_model,
                            system_message="You write short, plain customer letters for Albion Mutual. Revise when the reviewer asks.")
    reviewer = AssistantAgent("reviewer", model_client=reviewer_model, tools=[check_wording], reflect_on_tool_use=True,
                              system_message=("You review letters. Always run check_wording on the latest draft. Reply "
                                              "'CHANGES REQUESTED: …' or 'APPROVED: …'."))
    team = RoundRobinGroupChat([writer, reviewer], termination_condition=TextMentionTermination("APPROVED") | MaxMessageTermination(8))
    result = await team.run(task="Write to Mrs Rossi about claim C-881, delayed because the hospital's final bill is missing.")
    for msg in result.messages:
        text = msg.to_text() if hasattr(msg, "to_text") else str(getattr(msg, "content", msg))
        print(f"[{msg.source} · {type(msg).__name__}] {text[:220]}")
    print("\nstopped because:", result.stop_reason)


if __name__ == "__main__":
    asyncio.run(main())
