"""Lab 01 — LangGraph underwriting workflow with a persistent checkpoint and a human approval interrupt.

Run:   docker compose exec labs python 01_langgraph_agent.py start t-101      (runs until the approval step and stops)
       docker compose restart labs        (the process and container are gone; the checkpoint is not)
       docker compose exec labs python 01_langgraph_agent.py resume t-101 APPROVE "credit officer K. Rossi"
Try:   stop after `start`, delete the Python process (or restart the container), then `resume`: the state survives in
       checkpoints.sqlite. Then remove interrupt_before and watch the graph decide with no human — a CISO finding.
"""

from __future__ import annotations

import sys
from typing import List, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from common import DOCS


class State(TypedDict, total=False):
    application: dict
    chunks: List[str]
    dscr: float
    proposal: str
    decision: str
    decided_by: str


def retrieve(state: State) -> State:
    words = {w for w in state["application"]["purpose"].lower().split() if len(w) > 3}
    chunks = [d["text"] for d in DOCS if d["tenant"] == "crestfin" and words & set(d["text"].lower().split())]
    return {"chunks": chunks}


def assess(state: State) -> State:
    app = state["application"]
    dscr = round(app["ebitda"] / app["debt_service"], 2)
    return {"dscr": dscr, "proposal": "APPROVE" if dscr >= 1.25 and state["chunks"] else "REFER"}


def human_approval(state: State) -> State:
    # The graph is interrupted *before* this node; by the time it runs, `decision` was supplied by a person.
    return {"decision": state.get("decision", "REFER"), "decided_by": state.get("decided_by", "unknown")}


def build(saver):
    g = StateGraph(State)
    g.add_node("retrieve", retrieve)
    g.add_node("assess", assess)
    g.add_node("human_approval", human_approval)
    g.add_edge(START, "retrieve")
    g.add_edge("retrieve", "assess")
    g.add_edge("assess", "human_approval")
    g.add_edge("human_approval", END)
    return g.compile(checkpointer=saver, interrupt_before=["human_approval"])


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        return
    action, thread = sys.argv[1], sys.argv[2]
    config = {"configurable": {"thread_id": thread}}
    with SqliteSaver.from_conn_string("checkpoints.sqlite") as saver:
        app = build(saver)
        if action == "start":
            app.invoke({"application": {"id": "BHF-001", "purpose": "gold loan for working capital", "ebitda": 1_500_000,
                                        "debt_service": 1_100_000}}, config)
            snap = app.get_state(config)
            print("paused before:", snap.next, "| proposal:", snap.values.get("proposal"), "| DSCR:", snap.values.get("dscr"))
        elif action == "resume":
            decision, officer = sys.argv[3], sys.argv[4]
            app.update_state(config, {"decision": decision, "decided_by": officer})
            final = app.invoke(None, config)
            print("final:", final["decision"], "by", final["decided_by"], "| AI proposed", final["proposal"])


if __name__ == "__main__":
    main()
