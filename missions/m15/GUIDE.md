# Self-study guide: Make the approval workflow survive a restart

Agents that wait for people (approvals, sign-offs, reviews) must survive restarts, deployments and crashes. If they keep their progress only in memory, a restart repeats side effects: duplicate orders, duplicate emails, duplicate payments. Checkpointed state machines are how durable workflows and agent frameworks solve it.

## Revise first (in the course)

- state graphs versus free-running agent loops
- a tiny state-graph engine with checkpoints
- idempotency: making repeats harmless

## Read the email like an FDE

The automation lead's incident tells you the failure mode: after a restart the workflow started again from the beginning. The requirements follow from it. Save the state to a file after every step, so a restart can resume. Pick up exactly where it left off, so a second call never drafts again. Wait for an approve or reject event, so the workflow pauses in a named state. 'Never send an order twice, no matter how often it's called' means repeated calls, including repeated approvals, must be harmless. Events in the wrong state are ignored.

## Questions to ask the client first

- **What should happen if the server stops in the middle of sending an order?** The supplier's side decides whether a resend is safe; an order reference may be needed.
- **Who may approve, and does an approval expire?** Approval rules and time limits are often audited.
- **Where will the state live in production: a file, a database or the workflow engine?** A file is fine for one server; several servers need shared, locked storage.

## How each criterion is checked

1. **A new workflow drafts once and waits:** A new workflow must draft once, save its state and return waiting_for_approval.
2. **Restarting does not draft again:** Calling run twice on the same file must not draft again.
3. **Approval sends exactly once, even if called again:** Approving must send exactly once, even if run is called again and approve arrives twice.
4. **Rejection ends without sending:** Rejecting must end the workflow without sending, and a later approve must be ignored.
5. **State is checkpointed with the agreed fields:** The saved state must contain the agreed fields, with the step set to waiting_for_approval.

## How to work it

1. Read the email twice: once for the story, then with a pen, underlining every number, every rule and every 'must' or 'never'. Those words become the checks.
2. Turn the acceptance criteria into your own checklist, one line per criterion, and decide how you will see each one working before you build it.
3. Open the data files and the provided code before writing anything. Real files hold the awkward cases (blanks, duplicates, odd formats) the checks use.
4. Build the smallest piece that runs, print its result, and compare it with what you worked out by hand.
5. Add the next rule, run again, and keep each business rule in one obvious, named place.
6. Press Check only when your own prints agree with the criteria, then read each failing criterion's message before you change any code.
7. When it passes, read your code as the client's reviewer would, then compare it with the debrief.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| A second call drafts again | The state was kept in a variable, not read from the file. | Load the state from the file at the start of every call. |
| Approving twice sends twice | The send happened whenever approve arrived. | Send only on the transition from waiting to sent. |
| A crash mid-send loses track | The state was saved only at the end. | Save before and after the side effect. |
| Reject then approve sends | Events were not checked against the current step. | Ignore events that do not fit the current step. |

## Test yourself before you check

- Call run several times on a fresh file and print the state after each call.
- Delete nothing between calls: each call should behave like a fresh process reading the file.
- Try approve before the first draft and see what happens.
- Open the JSON file and check you could explain it to the operations team.

## What a senior reviewer also looks for

A reviewer would look for the steps written as named states with explicit transitions, a single place where the order is sent, and saves around that side effect. They would ask how the workflow would be observed in production (which step, since when) and how a stuck workflow would be found.

## Stretch goal

Add an approval timeout: if no decision arrives within a set time on an injected clock, move to an 'expired' state and record why, without ever sending.
