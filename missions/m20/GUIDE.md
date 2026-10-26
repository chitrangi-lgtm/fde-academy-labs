# Self-study guide: Answer the security questionnaire from evidence

No enterprise signs until its vendor-risk team is satisfied, and their questionnaire can stall a deal for weeks. Teams that answer from memory overclaim, and overclaims become contract problems later. Answering from an evidence register is faster, honest, and turns every gap into a dated plan the client can track. The same register answers the next client's questionnaire in an afternoon.

## Revise first (in the course)

- passing the CISO's security review
- commercial structures and pilots
- secrets, encryption, residency and audit

## Read the email like an FDE

The vendor risk manager sets the rules of honesty. Answers come from the register, never from memory, and each carries its evidence ids. A question can need several controls, and the criteria define the verdict exactly: Yes only when every control is implemented, Partial when at least one is implemented or partial but not all are implemented, No when none is. A control missing from the register counts as missing. 'The list of gaps you'll close before go-live' is every question not answered Yes.

## Questions to ask the client first

- **Do you need the evidence documents themselves, or only their ids at this stage?** Sharing evidence often needs an NDA and a secure channel.
- **Will a Partial answer with a dated plan be accepted for go-live?** Some risk teams accept compensating controls; others require Yes.
- **How often must the answers be refreshed?** Annual re-assessment is common; the register makes it cheap if kept current.

## How each criterion is checked

1. **Fully implemented controls are answered Yes with all evidence:** A question whose controls are all implemented must be answered Yes with all their evidence, sorted.
2. **A partly implemented control is Partial:** A question whose one control is only partly in place must be answered Partial with that control's evidence.
3. **One of two controls in place is Partial:** A question with one of two controls in place must be answered Partial with the evidence of the one in place.
4. **Missing or planned controls are No:** A question whose controls are missing or only planned must be answered No with no evidence.
5. **The gap list is what must close before go-live:** gaps must list the questions answered Partial or No, sorted.

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
| A KeyError on a control | A control missing from the register was looked up directly. | Look it up with a default status of missing. |
| Planned controls add evidence | Evidence was collected from every control. | Only implemented or partial controls contribute evidence. |
| A question with one partial control is No | Partial was not counted as 'something in place'. | Partial controls make the answer Partial. |
| Evidence ids are in register order | The list was not sorted. | Sort the evidence ids. |

## Test yourself before you check

- Answer the four questions by hand from the register first.
- Add a control with status 'planned' to a question and see the answer change.
- Remove a control from the register and check the question degrades, not crashes.
- Print the gaps and imagine presenting them with dates.

## What a senior reviewer also looks for

A reviewer would check that the answer logic is conservative: anything unknown makes the answer worse, never better. They would ask for each Partial and No to carry an owner and a date in the go-live plan, and for the register to be the single source used by sales, security and delivery alike.

## Stretch goal

Produce the gap list as a table with the missing controls for each question, ready for owners and dates to be filled in.
