# Self-study guide: Validate tool-call arguments with JSON Schema

An agent can call create_refund. Before any call reaches payments, the platform team wants every argument checked against the tool's JSON Schema, with the field at fault named so the agent can correct itself. tool_calls.json holds the schema (order id pattern, amount limits, allowed currencies, a minimum reason length, no extra fields) and six calls from last night's logs.

## Revise first (in the course)

- validating tool arguments before execution
- the anatomy of a tool definition
- validating tool arguments against a schema

## Questions to ask the client first

- **Should the agent see the full error message or only the field name?** Error text can reveal limits the agent might try to work around.
- **Who is alerted when an agent keeps sending invalid calls?** Repeated failures often mean a prompt or tool description needs fixing.
- **Is the schema versioned with the tool?** A schema change without a version can break agents silently.

## Ideas you will use

- **JSON Schema:** A standard way to describe what valid JSON looks like: types, required fields, patterns, limits, allowed values and whether extra fields are allowed. Tool definitions use it to tell models what arguments to send.
- **iter_errors:** Draft202012Validator(schema).iter_errors(args) yields every problem instead of stopping at the first. An empty list means the call is valid.
- **Finding the field:** Most errors carry the field in error.path. A missing required field and an unexpected field have an empty path; their names are in the error message, in quotes.
- **Validate before executing:** Only calls with no errors may reach the payments system. The rest go back to the agent with the field name so it can repair the call.

## Steps, check by check

1. **Only the first call is valid:** Validate every call and record whether it is valid: only the first one is.
2. **Amount over the limit names 'amount':** For the amount over the limit, report the field 'amount'.
3. **A bad order id names 'order_id':** For the badly formed order id, report 'order_id'.
4. **A missing reason names 'reason':** For the missing reason, report 'reason', taken from the error message because the path is empty.
5. **An unexpected argument names 'approve':** For the unexpected argument, report 'approve', also taken from the message.
6. **Only valid calls are executed:** List the indexes of the valid calls as the only ones safe to execute.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If a field name is wrong, print every error for that call with its path and message. If the missing reason gives an empty field, you read the path instead of the message. If more calls look valid than expected, check that the validator was built from the schema in the file.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| Every call is valid | check_call was left returning True. | Build the validator and use its errors. |
| The missing field's name is empty | error.path was used for a required-field error. | Take the quoted name from the message when the path is empty. |
| Different runs report different fields | Errors were taken in an unstable order. | Sort the errors before taking the first. |
| Invalid calls are in safe_to_execute | The list was built from all calls. | Include only valid ones. |
| A reason of five words is rejected | minLength was read as words. | JSON Schema's minLength counts characters, not words. |

## What the result means for the client

Five of six calls from last night would have reached payments with bad arguments, including one that tried to add its own approval flag. Validation stops all five and tells the agent which field to fix. Tell the platform team the gate costs microseconds and closes a whole class of incidents.

## What to send the client

A short report for the platform team: each call with its verdict and field, the one call that would run, and a recommendation to log every rejected call with the agent's prompt for review.

## Stretch goal

Return every failing field for a call, not just the first, and write the message you would send back to the agent so it can fix them all at once. Keep the message free of the limits' exact values if the platform team prefers not to reveal them.
