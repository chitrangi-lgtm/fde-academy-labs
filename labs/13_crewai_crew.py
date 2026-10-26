"""Lab 13 — CrewAI: a two-agent crew (policy researcher, then briefing writer) that prepares a client steering note.

Run:   docker compose exec labs python 13_crewai_crew.py
With a real model (any OpenAI-compatible endpoint):
       docker compose exec -e FDE_LLM_BASE_URL=http://host.docker.internal:11434/v1 -e FDE_LLM_MODEL=qwen2.5:7b labs python 13_crewai_crew.py
Guide: guides/13_crewai_crew.md

CrewAI describes work as Agents (a role, a goal, a backstory, tools) and Tasks (a description and an expected output),
run by a Crew in a Process. Here the process is sequential: the researcher searches CrestFin's policies with a tool and
reports the rules that apply; the writer turns that into a five-line steering note, receiving the researcher's output as
context. That hand-off (one task's output becoming the next task's context) is the core idea. Offline, a scripted model
answers in CrewAI's Thought / Action / Final Answer format so you can watch the loop without a key.
"""

from __future__ import annotations

import os

os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")   # keep the lab offline
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

from typing import Any  # noqa: E402

from crewai import LLM, Agent, BaseLLM, Crew, Process, Task  # noqa: E402
from crewai.tools import tool  # noqa: E402

from common import DOCS  # noqa: E402


@tool("search_policies")
def search_policies(query: str) -> str:
    """Search CrestFin's lending policies and return the matching policy lines with their IDs."""
    words = {w for w in query.lower().split() if len(w) > 3}
    hits = [f"{d['id']}: {d['text']}" for d in DOCS if d["tenant"] == "crestfin" and words & set(d["text"].lower().split())]
    print(f"[tool] search_policies({query!r}) -> {len(hits)} policy lines")
    return "\n".join(hits) or "No matching policy."


class ScriptedLLM(BaseLLM):
    """Plays both agents offline, in the text format CrewAI parses: an Action first, then a Final Answer."""

    def call(self, messages: Any, tools: Any = None, callbacks: Any = None, available_functions: Any = None,
             from_task: Any = None, from_agent: Any = None, response_model: Any = None) -> str:
        text = messages if isinstance(messages, str) else "\n".join(str(m.get("content", "")) for m in messages)
        if "Policy researcher" in text and "POL-2.9:" not in text:   # no tool result yet (the prompt itself mentions "Observation")
            return ('Thought: I should look up the small-business lending rules first.\nAction: search_policies\n'
                    'Action Input: {"query": "Small-business loans approval late payment"}')
        if "Policy researcher" in text:
            return ("Thought: I now know the final answer\nFinal Answer: POL-2.9 requires two credit officers to approve small-business loans "
                    "above 5 million. POL-4.2 sets late-payment interest at 2% a month on overdue small-business instalments.")
        return ("Thought: I now know the final answer\nFinal Answer: Steering note: small-business pilot\n"
                "1. Decision: keep two-officer approval for loans above $5 million (POL-2.9) inside the new workflow.\n"
                "2. Risk: the assistant must quote the 2% monthly late-payment rate exactly (POL-4.2).\n"
                "3. Ask: credit to name the two approvers for the pilot branches by Friday.\n"
                "4. Measure: approval turnaround and the share of quotes that cite a policy ID.\n"
                "5. Next review: after 200 pilot applications.")


def make_llm():
    base, model = os.getenv("FDE_LLM_BASE_URL"), os.getenv("FDE_LLM_MODEL")
    if base and model:
        return LLM(model=f"openai/{model}", base_url=base, api_key=os.getenv("FDE_LLM_API_KEY", "not-needed"))
    return ScriptedLLM(model="scripted")


def build_crew() -> Crew:
    llm = make_llm()
    researcher = Agent(role="Policy researcher", goal="Find the CrestFin lending rules that apply to the small-business pilot",
                       backstory="You read policy manuals carefully and always quote the policy ID.", tools=[search_policies],
                       llm=llm, allow_delegation=False, max_iter=4, verbose=False)
    writer = Agent(role="Briefing writer", goal="Write a five-line steering note the client's sponsor can act on",
                   backstory="You write for busy executives: decisions, risks, asks, measures.", llm=llm,
                   allow_delegation=False, max_iter=2, verbose=False)
    research = Task(description="Find every policy that constrains small-business loan approvals and late payments.",
                    expected_output="Each relevant rule in one sentence with its policy ID.", agent=researcher)
    brief = Task(description="Write the steering note for the small-business pilot from the research.",
                 expected_output="Exactly five numbered lines: decision, risk, ask, measure, next review.", agent=writer,
                 context=[research])
    return Crew(agents=[researcher, writer], tasks=[research, brief], process=Process.sequential, verbose=False)


if __name__ == "__main__":
    result = build_crew().kickoff()
    for task_output in result.tasks_output:
        print(f"\n--- {task_output.agent} ---\n{task_output.raw}")
