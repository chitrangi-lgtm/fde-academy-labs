# Self-study guide: Stop the instruction hidden in an email

Prompt injection is not solved by better prompts: an agent that reads email, documents or web pages will eventually read an instruction written by an attacker. The defence is policy enforced in code: track where each instruction came from, refuse side effects that untrusted content asked for, and put a human in the loop for risky actions. Security teams test this first in any agent review.

## Revise first (in the course)

- prompt injection and the lethal trifecta
- excessive agency and human oversight
- risk tiers for agent actions

## Read the email like an FDE

The CISO describes the red-team result and the policy that would have stopped it. The deciding fact is provenance: who asked for the action. Anything with side effects is blocked when the instruction came from content the agent read rather than from the employee. When the employee did ask, three cases still need a human: mail leaving the company's domain, payments over the limit, and any delete. Reading is always fine. Every decision needs a reason a person can read.

## Questions to ask the client first

- **How does the agent know which instruction came from the employee?** Provenance has to be tracked by the system, never claimed by the text.
- **Who approves, and how quickly must approvals happen?** Slow approvals push people to work around the gate.
- **Should blocked attempts alert the security team?** A blocked injection is evidence of an attack in progress.

## How each criterion is checked

1. **The injected forward is blocked:** Forwarding mail because of an instruction found in an email must be blocked.
2. **Side effects from tool output are blocked too:** A payment requested by tool output must be blocked too.
3. **Reading is always allowed:** Reading the inbox must be allowed whoever asked.
4. **Mail leaving the company needs approval, internal mail does not:** Mail from the employee to an outside recipient must need approval, while mail only to colleagues is allowed.
5. **Large payments and any delete need approval:** A payment above the limit and any delete must need approval, while a small payment is allowed.
6. **Every decision comes with a reason:** Every decision must come with a readable reason.

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
| The injected forward needs approval instead of being blocked | Arguments were checked before provenance. | Decide on provenance first. |
| An address like 'x@ashgrove.example.evil.com' counts as internal | A substring test was used. | Check that the address ends with '@' plus the internal domain. |
| A payment exactly at the limit needs approval | The comparison included equality. | Only payments above the limit need approval. |
| Reasons are empty | Only the decision was returned. | Return a short reason with every decision. |

## Test yourself before you check

- Make a table of tools against provenances and fill in the decisions by hand.
- Try a recipient list with one internal and one external address.
- Try an unknown tool name and decide what the policy should say.
- Read the reasons out loud: would an employee understand why they were stopped?

## What a senior reviewer also looks for

A reviewer would check that the guard denies by default for tools it does not know, that provenance comes from the system and not from the model's text, and that every block and approval is logged for the security team. They would also ask for the policy values to live in configuration the CISO's team can change.

## Stretch goal

Make unknown tools blocked by default with their own reason, and add a log of every decision with the tool, provenance and reason, ready for the security team's dashboard.
