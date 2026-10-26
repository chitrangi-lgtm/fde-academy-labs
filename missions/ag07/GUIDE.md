# Self-study guide: A supervisor that routes, follows hand-offs and knows when to stop

Multi-agent systems fail in a way single agents do not: work bounces between specialists forever while the customer waits. Contact centres that use specialist agents need a supervisor with explicit stop rules and a human fallback. The same rules apply to any team of agents handing work to each other.

## Revise first (in the course)

- orchestration patterns
- coordination failures and how to prevent them
- catching delegation ping-pong

## Read the email like an FDE

The platform lead describes the failure (billing hands to technical, technical hands back) and the rules that stop it. Route each ticket to the first specialist whose keywords match, in the order given. Follow hand-offs. Escalate to a human the moment a ticket would go back to an agent that already had it, or after the hand-off budget is used. 'The moment' means before the agent is called again. A ticket no agent matches goes straight to a human.

## Questions to ask the client first

- **Should a human receive the transcript of what the agents already tried?** Escalating without the history makes the customer repeat themselves.
- **Is keyword routing a first step, with a classifier later?** Keyword order decides ties, and that order should be agreed.
- **Can an agent hand off to a human directly?** Some specialists know earlier than the supervisor that a person is needed.

## How each criterion is checked

1. **Routing by keyword, in order:** route must pick the first specialist in the given order whose keyword appears, or 'human'.
2. **A simple ticket is handled by one agent:** A simple refund ticket must be handled by billing alone, with one transcript line.
3. **A hand-off is followed:** A ticket that technical hands to delivery must end with delivery, after two transcript lines.
4. **Ping-pong is escalated before it starts:** A ticket that would bounce back to billing must be escalated before billing is called a second time.
5. **Too many hand-offs are escalated:** With a budget of one hand-off, a ticket needing two must be escalated.
6. **Unmatched tickets go to a human:** A ticket no agent matches must go to a human with an empty transcript.

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
| Ping-pong shows three transcript lines | The revisit was detected after calling the agent again. | Check whether the next agent already handled the ticket before calling it. |
| Routing picks delivery for a refund about a parcel | Routes were checked in a different order. | Check the routes in the order given. |
| max_handoffs is off by one | The hand-off was counted after the check. | Count the hand-off, then compare with the budget. |
| An unmatched ticket crashes | The agents dictionary was indexed with 'human'. | Handle 'human' before looking up an agent. |

## Test yourself before you check

- Trace the ping-pong ticket on paper: which agent, which reply, which hand-off.
- Change max_handoffs to 0 and see what happens to a ticket with one hand-off.
- Write a ticket with keywords for two specialists and predict the route.
- Print the transcript for every test ticket.

## What a senior reviewer also looks for

A reviewer would check that the stop rules are visible in one place, that escalation always includes the transcript, and that every escalation is logged with its reason (revisit or budget). They would also ask how the routes are maintained, because keyword lists drift as products change.

## Stretch goal

Return the escalation reason ('revisit' or 'budget') and the agent the ticket would have gone to next, so the contact-centre team can find the specialist pairs that bounce most.
