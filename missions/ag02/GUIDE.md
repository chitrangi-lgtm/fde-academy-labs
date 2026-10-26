# Self-study guide: Validate and gate tool calls before they run

Once agents can call tools that move money, every call needs the same checks a payments team would demand from any other client: is the request well formed, is it allowed, and does a person need to approve it? Precise validation errors also make the agent better, because the model can fix its own call instead of guessing.

## Revise first (in the course)

- validating tool arguments before execution
- side effects, idempotency and approval
- a validator turning a bad call into a quick fix

## Read the email like an FDE

The payments owner sets an order of operations and a subset of JSON Schema. 'Before any call reaches payments' means validation and approval both come before the tool runs. 'Errors precise enough for the agent to fix its call' means one message per field, naming the problem. 'Refunds above 100 dollars must wait for a human' is an approval rule. The list of schema keywords tells you exactly what to support, and the criteria add the trap: a boolean is neither a number nor an integer.

## Questions to ask the client first

- **Should the agent ever see the approval rule, or only the 'approval required' answer?** Revealing thresholds can encourage splitting a refund into smaller ones.
- **Who approves, and how does an approval reach this layer?** The approval needs an identity and a record for audit.
- **What stops the same refund from being sent twice?** Validation does not prevent duplicates; an idempotency key does.

## How each criterion is checked

1. **A good call validates:** A correct refund request must validate with no errors.
2. **Every problem is named by field:** A request with four different problems must produce one error per field, each naming its problem, sorted.
3. **Missing fields and wrong types are caught; a boolean is not a number:** A request with a boolean amount and a missing currency must report a wrong type and a required field.
4. **Unknown tools and invalid calls never run:** An unknown tool and an invalid call must both be refused without running anything.
5. **A large refund waits for a human:** A refund above the approval limit must be refused with 'approval required', and no refund must be recorded.
6. **Approved or small refunds run once:** An approved large refund and a small refund must each run once.

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
| True passes as an amount | bool is a subclass of int in Python. | Exclude booleans from number and integer. |
| A wrong type also reports below minimum | Checks went on after a type error. | Skip the remaining checks for a field once its type is wrong. |
| The pattern accepts '104233-ORD-000001' | A search was used instead of a full match. | Match the whole value against the pattern. |
| A large refund is recorded before approval | The tool ran before the approval check. | Check approval before calling the tool. |

## Test yourself before you check

- Write five bad calls, each with one problem, and check each gives exactly one error.
- Try an extra field with and without additionalProperties false.
- Check the refunds list after each execute call.
- Read your error messages as the model would: could it fix the call from them?

## What a senior reviewer also looks for

A reviewer would check the order validate, authorise, act in execute, that error messages never include sensitive values, and that every refused call is logged with its reason. They would also look for the approval rule to live with the tool's definition, where the payments team can see and change it.

## Stretch goal

Add an idempotency key to the refund tool so a repeated identical request returns the first result instead of refunding twice.
