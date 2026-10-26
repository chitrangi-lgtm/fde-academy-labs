# Self-study guide: Structured output with a validate-and-retry loop

A support agent turns customer emails into tickets. ticket_attempts.json holds the model's two answers in order: the first is wrapped in chatty text, uses a priority the system does not know and has no category; the second, after your corrective message, is clean. You build the loop a production team would: extract the JSON, validate it, and if it fails, write a retry message naming each field and the allowed values.

## Revise first (in the course)

- validate, then repair: bounded correction loops
- extracting JSON robustly from model replies
- a bounded repair loop

## Questions to ask the client first

- **How many retries may the agent make before a person takes over?** Each retry costs time and money; the limit should be agreed.
- **Which categories and priorities does the ticketing system really accept?** The schema must match the system of record exactly.
- **Should failed attempts be kept for analysis?** Logged failures show which fields the prompt explains badly.

## Ideas you will use

- **Literal fields:** Literal['low', 'medium', 'high'] accepts only those values. When validation fails, pydantic's message lists the allowed values, which is exactly what the retry message needs.
- **Extracting JSON:** A regular expression takes the text from the first opening brace to the last closing brace, so chatty text around the JSON is dropped before validation.
- **Reading validation errors:** exc.errors() returns one entry per problem, each with loc (the field) and msg (what was wrong). Turning each into a line gives a precise retry message.
- **A bounded loop:** Try each answer in order, count the attempts, and stop at the first that validates. A real loop would also stop after a fixed number of retries.

## Steps, check by check

1. **JSON is pulled out of chatty text:** Write extract_json so it pulls the JSON object out of chatty text.
2. **The ticket validates on the second answer:** Loop over the answers, validating each, and stop at the first valid ticket: the second answer, with category payments.
3. **Unknown priorities are rejected:** Restrict priority with a Literal so 'urgent' is rejected.
4. **The retry message names both failing fields:** Write retry_message so it names every failing field, including the missing category.
5. **The retry message gives the allowed priorities:** Make sure the retry message includes the allowed priorities.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If the first check fails, print what extract_json returns for a short chatty string. If the loop stops at the wrong answer, print each validation error. If the retry message misses a field, print exc.errors() and check you turned every entry into a line. The checks build their own invalid ticket to test the retry message, so it must work from any validation error, not only the one in the file.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| The first answer validates | Priority and category were left as plain strings. | Use Literal types with the allowed values. |
| The retry message names only priority | Only the first error was used. | Include every error. |
| attempts_used is 1 | The counter was not increased for the failed attempt. | Count every answer you try. |
| Extraction fails on multi-line JSON | The regular expression did not cross line breaks. | Let the pattern match across lines. |
| The loop would retry forever on a stubborn model | Nothing limited the attempts. | Stop when the answers run out here, and after a fixed number of retries in production. |

## What the result means for the client

The first answer would have created a ticket the system cannot route; the retry message fixed both problems in one round. Tell the support platform team that a precise message usually costs one extra call, and that capping retries keeps the cost predictable.

## What to send the client

The schema, the retry message the loop produced, and a note recommending a two-retry limit with failures sent to a person, ready for the support platform team's review.

## Stretch goal

Count how often each field fails across many attempts and print the most common one, which tells the team which part of the prompt to improve first.
