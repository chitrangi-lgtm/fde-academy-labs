# Nudges (open only if stuck)

1. Keep a set of agents that already handled the ticket and a count of hand-offs.

2. Before following a hand-off, check both stop conditions; otherwise move to the next agent and loop.

## The approach, in plain English (open last)

1. Write route: walk the routes in order and return the first agent with a matching keyword, or 'human'.
2. In supervise, send an unmatched ticket straight to a human.
3. Otherwise keep the transcript, the set of agents that handled the ticket and the hand-off count.
4. Call the current agent, record its reply, and finish if it does not hand off.
5. Before following a hand-off, count it and check both stop rules; escalate if either applies, otherwise move to the next agent.
