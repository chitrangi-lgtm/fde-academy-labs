# A supervisor that routes, follows hand-offs and knows when to stop

**From:** Lars Eriksen, Contact Centre Platform Lead, Ostara Telecom

We run specialist agents for billing, technical and delivery questions. Some tickets bounce between agents forever: billing hands to technical, technical hands back to billing. I need a supervisor that routes each ticket to the right specialist, follows hand-offs, and escalates to a human the moment a ticket would go back to an agent that already had it, or after two hand-offs. The agents and routing keywords are provided.

## Done when

- `route(ticket)` returns the first agent (in ROUTES order) with a keyword in the ticket, else "human"
- `supervise(ticket, agents, max_handoffs=2)` returns {"handled_by", "transcript" [(agent, reply)], "escalated"}
- Follow each agent's handoff; escalate (handled_by "human", escalated True) when the next agent already handled the ticket or the hand-off count would exceed max_handoffs
- A ticket no agent matches goes straight to a human with an empty transcript

## Files

none

`provided.py` holds code the client gives you; the checker runs it before your code.

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag07
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module ag07) records your score.
