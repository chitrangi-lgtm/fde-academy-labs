# Lab 01: Pause and resume an underwriting workflow with LangGraph

**Time:** 60 minutes · **Level:** Intermediate · **Builds on:** Professional Practice P1, Agentic Module 1 (the agent loop), FDE Module 15 (agents in production)

## The problem

CrestFin's small-business lending team wants an assistant that reads a loan application, finds the credit policies that apply,
computes the debt-service coverage ratio (DSCR) and proposes approve or refer. The CISO has one condition: no loan is
decided by software alone. A credit officer must approve every decision, and that may happen hours later, after the
server has restarted or been redeployed.

So the workflow has to stop before the decision, keep its state somewhere durable, and carry on later from exactly where
it stopped, with the officer's name recorded. This lab builds that with **LangGraph**, a library for agent workflows as
graphs of steps, and its SQLite checkpointer.

## What you'll learn

- How a LangGraph `StateGraph` describes a workflow as nodes (functions) and edges, sharing a typed state.
- How a checkpointer saves the state after every step, keyed by a `thread_id`, so a run survives a restart.
- How `interrupt_before` pauses the graph before a node, and how `update_state` plus `invoke(None, ...)` resumes it.
- Why the human decision is recorded separately from the AI's proposal, and what an auditor will ask for.

## Before you start

1. Start the labs from `realtools/`: `docker compose up -d --build` (the first build takes a few minutes).
2. Run `docker compose exec labs python 01_langgraph_agent.py` with no arguments to see the usage.
3. Without Docker: create a virtual environment, `pip install -r requirements.txt`, then `cd labs`.

No model or API key is needed: the nodes are plain Python, which keeps the focus on the workflow.

## Key ideas

**State is a typed dictionary.** `State` lists everything the workflow knows: the application, the retrieved policy
chunks, the DSCR, the proposal, and the final decision and who made it. Each node returns only the keys it changes, and
LangGraph merges them into the state.

**The checkpointer is the memory between runs.** `SqliteSaver` writes the state to `checkpoints.sqlite` after every
node. The `thread_id` (here `t-101`) is the key: one thread per application. Restart the process and the next call with
the same thread finds the saved state.

**An interrupt is a planned stop.** `interrupt_before=["human_approval"]` makes the graph stop just before that node.
`get_state(config).next` tells you which node is waiting. Nothing about the decision happens until a person supplies it.

**Resuming means adding input, then continuing.** `update_state` writes the officer's decision and name into the saved
state; `invoke(None, config)` continues from the checkpoint instead of starting again.

**The AI proposes; a person decides.** The final output keeps both `proposal` (the AI's suggestion) and `decision` with
`decided_by`. When they differ, that's useful evidence of the officer's judgement and of where the model needs work.

## Steps

1. **Start a run.** `docker compose exec labs python 01_langgraph_agent.py start t-101`. Expected output:
   `paused before: ('human_approval',) | proposal: APPROVE | DSCR: 1.36`. The DSCR is 1,500,000 / 1,100,000 = 1.36,
   above the 1.25 threshold, and the gold-loan policy was retrieved, so the proposal is APPROVE.

2. **Restart everything.** `docker compose restart labs`. The Python process and the container are gone. The file
   `labs/checkpoints.sqlite` is still on your disk, because the folder is mounted from your machine.

3. **Resume as the officer.** `docker compose exec labs python 01_langgraph_agent.py resume t-101 APPROVE "credit officer K. Rossi"`.
   Expected output: `final: APPROVE by credit officer K. Rossi | AI proposed APPROVE`. The run continued from the
   checkpoint; it didn't retrieve or assess again.

4. **Disagree with the AI.** Start thread `t-102`, then resume it with `REFER "credit officer S. Weber"`. The output shows
   `final: REFER ... | AI proposed APPROVE`. Think about where you'd store this disagreement for the monthly model review.

5. **Change the numbers.** Edit `debt_service` to `1_300_000` and start thread `t-103`. The DSCR becomes 1.15 and the
   proposal becomes REFER. Then change the purpose to `"machinery purchase"`: no policy matches any word longer than
   three letters, `chunks` is empty and the proposal is REFER even with a good DSCR. Decide whether that's the right
   behaviour.

6. **Remove the human (and see the finding).** Delete `interrupt_before=["human_approval"]` and start thread `t-104`.
   The output shows `paused before: ()`: nothing waited for a person, and the saved state now holds a decision of
   REFER made by `unknown` (print `snap.values` to see it). That is exactly what a CISO would raise as a finding. Put
   the interrupt back.

7. **Inspect the checkpoints.** Open `checkpoints.sqlite` with any SQLite tool, or call `app.get_state_history(config)`,
   and list the saved steps for `t-101`. Each node left a checkpoint; that history is your audit trail.

## Check yourself

<details><summary>Why use a thread_id per application rather than one per officer?</summary>
The saved state belongs to the application's workflow. One officer handles many applications, and an application may be
picked up by a different officer. Keying by application keeps each workflow's history separate and easy to audit.
</details>

<details><summary>What would happen without the checkpointer?</summary>
The state lives only in memory. After the restart in step 2, `resume` would find nothing to continue, and the
application would have to be processed again, possibly with different retrieved policies.
</details>

<details><summary>Why keep both the proposal and the decision?</summary>
Auditors and model owners need to see what the AI suggested and what the person decided. Disagreements show where the
model or the policy retrieval needs work, and prove that a person really made the decision.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `resume` fails with a `KeyError` | A different `thread_id` from the one you started with, so there is no saved state to continue | Use exactly the same thread id for `start` and `resume` |
| The graph never pauses | `interrupt_before` was removed or names the wrong node | The list must contain the node name exactly as added: `"human_approval"` |
| `final:` shows `unknown` as the decider | The state was not updated before resuming | Call `update_state` with `decision` and `decided_by` before `invoke(None, config)` |
| `database is locked` | Two processes writing the same SQLite file | Run one command at a time, or use the PostgreSQL checkpointer for real deployments |

## Take it further

- Add a `notify` node after `assess` that prints a message for the officer's queue, so they know an application is waiting.
- Add a timeout rule: if no decision arrives within 48 hours, a separate job marks the thread as escalated.
- Swap `SqliteSaver` for the PostgreSQL checkpointer and run two containers against one database.

## In a real client project

- Use a durable, backed-up checkpoint store (PostgreSQL), not a local SQLite file.
- Authenticate the officer and take `decided_by` from their verified identity, never from a typed argument.
- Keep the full checkpoint history for the retention period your client's regulator requires.
