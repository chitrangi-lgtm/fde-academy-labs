"""Lab 11 — Google's Agent Development Kit (ADK): a loan pre-check agent with function tools, a session and events.

Run:   docker compose exec labs python 11_google_adk_agent.py
With a real model: ADK talks to Gemini natively (set GOOGLE_API_KEY and ADK_MODEL=gemini-…), or to any LiteLLM-supported
       provider after `pip install "google-adk[extensions]"` (set ADK_MODEL=openai/<model>, OPENAI_API_BASE and OPENAI_API_KEY).
Guide: guides/11_google_adk_agent.md

The idea is the agent loop from Agentic Module 1 again, in Google's framework: plain Python functions become tools (ADK
reads their type hints and docstrings), an LlmAgent decides which to call, and a Runner executes the turn inside a
session, emitting an event for every model reply, tool call and tool result. That event stream is what you log, trace and
audit in production. Offline, a scripted model stands in so you can study the events without a key.
"""

from __future__ import annotations

import asyncio
import os
from typing import AsyncGenerator

from google.adk.agents import LlmAgent
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import InMemoryRunner
from google.genai import types

CREDIT_BANDS = {"TP28746677": {"band": "A", "score": 781}, "TP39977518": {"band": "C", "score": 612}}


def get_credit_band(taxpayer_id: str) -> dict:
    """Return the applicant's credit band and score from the bureau.

    Args:
        taxpayer_id: The applicant's taxpayer ID (TP followed by 8 digits).
    """
    return CREDIT_BANDS.get(taxpayer_id.upper(), {"error": f"no bureau record for {taxpayer_id}"})


def monthly_instalment(principal_usd: float, annual_rate_percent: float, months: int) -> dict:
    """Calculate the fixed monthly instalment (amortising payment) for a loan.

    Args:
        principal_usd: The loan amount in dollars.
        annual_rate_percent: The yearly interest rate, for example 11.5.
        months: The loan tenure in months.
    """
    r = annual_rate_percent / 1200
    instalment = principal_usd * r * (1 + r) ** months / ((1 + r) ** months - 1) if r else principal_usd / months
    return {"instalment_usd": round(instalment), "total_interest_usd": round(instalment * months - principal_usd)}


class ScriptedLlm(BaseLlm):
    """Stands in for Gemini offline: calls the bureau, then the monthly instalment tool, then answers from both results."""

    async def generate_content_async(self, llm_request: LlmRequest, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:
        done = {p.function_response.name: p.function_response.response for c in llm_request.contents for p in (c.parts or [])
                if p.function_response}
        if "get_credit_band" not in done:
            part = types.Part(function_call=types.FunctionCall(name="get_credit_band", args={"taxpayer_id": "TP28746677"}))
        elif "monthly_instalment" not in done:
            part = types.Part(function_call=types.FunctionCall(name="monthly_instalment", args={"principal_usd": 25000, "annual_rate_percent": 11.5, "months": 36}))
        else:
            band, instalment = done["get_credit_band"], done["monthly_instalment"]
            text = (f"Pre-check passed: credit band {band.get('band')} (score {band.get('score')}). A $25,000 loan over 36 months "
                    f"at 11.5% costs ${instalment.get('instalment_usd'):,} a month. Final approval needs income proof and a credit officer.")
            part = types.Part(text=text)
        usage = types.GenerateContentResponseUsageMetadata(prompt_token_count=0, candidates_token_count=0, total_token_count=0)
        yield LlmResponse(content=types.Content(role="model", parts=[part]), usage_metadata=usage)


def make_model():
    name = os.getenv("ADK_MODEL")
    if not name:
        return ScriptedLlm(model="scripted")
    if name.startswith("gemini"):
        return name                                   # ADK's native Gemini client reads GOOGLE_API_KEY
    from google.adk.models.lite_llm import LiteLlm   # needs google-adk[extensions]
    return LiteLlm(model=name)


agent = LlmAgent(
    name="loan_precheck",
    model=make_model(),
    instruction=("You pre-check personal-loan enquiries for CrestFin. Always call get_credit_band before quoting, then "
                 "monthly_instalment. Never promise approval: a credit officer decides."),
    tools=[get_credit_band, monthly_instalment],
    output_key="precheck_summary",
)


async def main() -> None:
    runner = InMemoryRunner(agent=agent, app_name="crestfin_precheck")
    session = await runner.session_service.create_session(app_name="crestfin_precheck", user_id="branch-riverton-07")
    question = types.Content(role="user", parts=[types.Part(text="Taxpayer ID TP28746677 wants $25,000 over 3 years at 11.5%. Pre-check it.")])
    async for event in runner.run_async(user_id="branch-riverton-07", session_id=session.id, new_message=question):
        for part in (event.content.parts if event.content else []):
            if part.function_call:
                print(f"[{event.author}] calls {part.function_call.name}({dict(part.function_call.args)})")
            elif part.function_response:
                print(f"[{event.author}] result {part.function_response.name}: {dict(part.function_response.response)}")
            elif part.text:
                print(f"[{event.author}] says: {part.text}")
    saved = await runner.session_service.get_session(app_name="crestfin_precheck", user_id="branch-riverton-07", session_id=session.id)
    print("\nsession state saved by output_key:", saved.state.get("precheck_summary", "")[:80], "…")
    print("events in the session:", len(saved.events))


if __name__ == "__main__":
    asyncio.run(main())
