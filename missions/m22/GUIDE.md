# Self-study guide: Check the partner feed against its data contract

Integration is where engagements fail: a partner renames a field, starts sending text where a number was, or stops sending updates, and the assistant quietly gives wrong answers. A data contract checked before anything loads turns those silent changes into a failed check that names the row and the field. It is the conversation you want to have with a partner, with evidence in hand.

## Revise first (in the course)

- data contracts: making interfaces explicit
- contract tests and a test strategy
- validating records against a data contract

## Read the email like an FDE

The integration lead lists what the contract covers: types, required fields, allowed values, nullability and freshness. Two words are easy to confuse and the criteria separate them: a nullable field may hold None, while a field that is not required may be absent altogether. The problems have fixed names, and the order of checks matters, because a missing field cannot also have a wrong type. 'Before anything loads' means the check runs on the whole batch and reports everything, not just the first problem.

## Questions to ask the client first

- **Should a batch with violations be held entirely, or should good rows load?** Partial loads can leave the assistant with a mix of new and stale claims.
- **Who at the partner receives the violation report?** A contract only works when both sides act on breaches.
- **Which time zone are the updated_at timestamps in?** Freshness compared across time zones can be wrong by hours.

## How each criterion is checked

1. **Every violation is listed by row and field:** violations on the sample batch must list exactly six problems by row index, field and problem name, sorted.
2. **A nullable amount may be None and an optional field may be absent:** A record with a nullable field set to None and an optional field absent must have no violations.
3. **An integer is a number, a boolean is not:** An integer must be accepted as a number, and a boolean must be rejected as a number.
4. **Fresh within two hours:** is_fresh must be True when the newest update is within the contract's freshness window.
5. **Stale after two hours:** is_fresh must be False once that window has passed.

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
| True passes as an integer | bool is a subclass of int in Python. | Check for bool before checking for int. |
| An optional absent field is reported as missing | Required was not checked. | Report missing only for required fields. |
| A missing field also reports a wrong type | Checks went on after finding it missing. | Stop checking a field once it is missing or null. |
| Unexpected fields are never reported | Only the contract's fields were walked. | Also walk the record's own fields. |

## Test yourself before you check

- Go through the sample batch by hand and list every violation first.
- Build one perfect record and confirm it has no violations, then break it one field at a time.
- Print the newest timestamp and the cut-off time for both freshness cases.
- Try an empty batch and decide what is_fresh should say.

## What a senior reviewer also looks for

A reviewer would check that problem names are stable (other systems will count them), that the contract is read from the agreed file rather than restated in code, and that the report is sorted so two runs can be compared. They would also ask what the check does when the contract itself is malformed.

## Stretch goal

Group the violations by field with counts, so the partner sees 'status: 40 rows not allowed' instead of a long list, and include one example row for each.
