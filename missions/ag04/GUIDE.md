# Self-study guide: Give the assistant a memory that fits its budget

Long conversations overflow the context window, and an assistant that remembers everything also remembers personal data it should never have kept. Memory needs a budget, a policy for what survives, and privacy at the moment of writing. Health, finance and support assistants are all reviewed on exactly these points.

## Revise first (in the course)

- managing conversation history
- summarisation and compaction
- memory risks: poisoning, leakage and retention

## Read the email like an FDE

The product director lists four rules. A word budget: when it overflows, the oldest messages go, folded into one summary line. Pinned facts, like an allergy, are never dropped. The newest message always stays. Contact details are masked before anything is stored, which means at write time, not when the context is read. The criteria make the details exact: what counts as a word, that the summary line does not count towards the budget, and the exact text of the summary line.

## Questions to ask the client first

- **How long may memory be kept, and can a patient ask for it to be deleted?** Retention and deletion rights apply to assistant memory as to any other record.
- **Who may pin a fact: the patient, the clinician, or the assistant?** Pinned facts are trusted for the whole conversation, so who sets them matters.
- **Which identifiers besides phones and emails must be masked?** Health services often have their own patient numbers.

## How each criterion is checked

1. **Contact details are masked before storing:** A message with a phone number and an email must be stored with both masked.
2. **Under budget, nothing changes:** Two short messages under budget must come back unchanged and in order.
3. **The budget is respected:** After many messages, the words in the context (excluding the summary line) must fit the budget.
4. **Pinned facts survive:** A pinned fact must still be in the context after older messages are removed.
5. **The newest message is kept:** The newest message must always be the last item in the context.
6. **Removed messages are counted in one summary line at the start:** One summary line at the start must count the removed messages exactly.

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
| The newest message is removed | The search for a message to remove included the last one. | Search every message except the last. |
| The loop never ends | Only pinned messages and the newest are left, and they are over budget. | Stop removing when there is nothing left that may be removed. |
| Contact details appear in the context | Masking happened when reading, or not at all. | Mask before storing. |
| The summary line pushes the memory over budget | It was counted as words. | Leave the summary line out of the size. |

## Test yourself before you check

- Add messages one at a time with a small budget and print the context after each.
- Pin a long fact and watch what is removed around it.
- Store a message with a date like 2026-03-01 and check it is not masked.
- Count the words yourself and compare with the budget.

## What a senior reviewer also looks for

A reviewer would check that masking happens in exactly one place on the way in, that the removal policy is easy to read, and that nothing outside the class can bypass the mask by changing the stored list. They would also ask how the memory is deleted when a conversation ends.

## Stretch goal

Replace the removed-message count with a short summary written by a stand-in model, and keep the same rules about budget, pinned facts and masking.
