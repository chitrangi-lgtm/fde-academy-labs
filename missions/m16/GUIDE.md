# Self-study guide: Pre-retrieval access control and redaction

Security teams block go-live for two reasons more than any other: an assistant that can retrieve documents the user may not see, and personal data shown where it should be masked. Access control has to happen before retrieval, because a model cannot be trusted to keep a secret it has already read. Redaction has to be precise, or users switch it off.

## Revise first (in the course)

- why access control in the prompt is a vulnerability
- a deny-by-default policy engine with explanations
- a personal-data redactor

## Read the email like an FDE

The CISO states the access rules in a fixed order. Same company first: no rule ever crosses tenants. Then clearance: the document's level must not be higher than the user's, using the order public, internal, confidential, restricted. Then department, but only for confidential and restricted documents, with auditors as the one exception. For redaction, three kinds of data are masked, and the last sentence is the trap: order numbers are long digit strings too, so only numbers that pass the Luhn check are cards.

## Questions to ask the client first

- **Should a denied document be invisible, or shown as 'you do not have access'?** Revealing that a document exists can itself leak information.
- **Which phone formats do your staff and customers use?** Phone patterns differ by country; a pattern that misses one format leaks numbers.
- **Should every access decision be logged for audit?** Regulated clients often must show who could see what, and when.

## How each criterion is checked

1. **A claims agent sees claims documents up to their clearance:** visible for a claims agent must return the claims documents up to their clearance, sorted.
2. **An auditor sees across departments, within clearance:** visible for an auditor must include confidential documents from other departments, within clearance.
3. **An intern sees nothing above internal:** visible for an intern must return only public and internal documents.
4. **Another company's documents are never visible:** No user may ever see the other company's document.
5. **Emails and phones are masked:** redact must mask an email address and two differently formatted phone numbers in one sentence, leaving the rest unchanged.
6. **Real card numbers are masked, order numbers are not:** redact must mask two real card numbers written with spaces and with dashes, and leave an order number that fails the Luhn check alone.

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
| The intern sees a confidential document | Clearance was compared alphabetically. | Compare the positions of the levels in the ordered list. |
| The auditor still cannot see other departments | The auditor exception was checked before the department rule applied, or not at all. | Apply the exception inside the department rule for confidential and restricted. |
| The order number is masked | Every long digit string was treated as a card. | Mask only runs that pass the Luhn check. |
| Card digits are masked as phone numbers | Phones were replaced before cards. | Replace cards before phones. |

## Test yourself before you check

- Make a table of every user against every document and fill it in by hand before running visible.
- Run Luhn on the test card number and on the order number and print both results.
- Redact a sentence with an email next to a card number and read the result.
- Try a document from another company with every clearance level.

## What a senior reviewer also looks for

A reviewer would check that the policy denies by default: a missing field or unknown level must mean no access, never access. They would look for the access rule in one function that returns a reason, so audit questions can be answered, and for redaction that runs on everything the assistant shows, including citations.

## Stretch goal

Make the access function return the reason for each decision ('different company', 'above clearance', 'other department'), and write the decisions to an audit log.
