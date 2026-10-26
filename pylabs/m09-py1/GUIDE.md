# Self-study guide: Validate model output with pydantic

An invoice-extraction prompt returns JSON most of the time. model_outputs.json holds five model replies: two good invoices (one wrapped in chatty text and a code fence), one whose total does not match its lines, one with a lower-case currency and one with a zero quantity. You write a pydantic schema that catches every problem and a parser that rescues the wrapped answer.

## Revise first (in the course)

- runtime data validation with pydantic
- constrained decoding versus validation and correction
- recovering JSON from a chatty model reply

## Questions to ask the client first

- **What should happen to an invoice the schema rejects: retry the model, or send it to a person?** The answer decides whether you need a retry loop or a review queue.
- **How close must the total be to the sum of the lines?** Rounding on paper invoices can differ by a cent; finance must set the tolerance.
- **Which currencies can appear on your invoices?** An allowed list that is too short will reject real invoices.

## Ideas you will use

- **Field constraints:** Field(gt=0) rejects zero and negatives; Field(ge=0) allows zero. pattern checks text against a regular expression. Constraints live with the field, so they cannot be forgotten.
- **Literal types:** Literal['USD', 'EUR', 'GBP'] accepts only those exact values, so 'usd' fails. It documents the allowed values at the same time.
- **Model validators:** @model_validator(mode='after') runs once all fields are valid and can compare fields with each other, such as the total against the sum of the lines.
- **Rescuing JSON:** A regular expression can take the text from the first opening brace to the last closing brace, dropping chatty text and code fences, before pydantic parses it.

## Steps, check by check

1. **The two good invoices pass, including the one wrapped in a code fence:** Parse every model output; collect the invoice numbers of the good ones, including the wrapped one, in valid.
2. **Three outputs are rejected:** Record the index and error message of every rejected output in errors.
3. **A total that does not match the lines is rejected:** Add a model validator that rejects a total that does not match the lines.
4. **A lower-case currency is rejected:** Restrict the currency to the allowed upper-case codes.
5. **A zero quantity is rejected:** Reject a line whose quantity is zero.
6. **A good invoice still validates:** Make sure a good invoice still validates and keeps its total.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If valid is missing the wrapped invoice, print what your parser extracts from it before validation. If a bad invoice passes, validate it on its own and read pydantic's error list. Each check that builds an invoice directly tells you which rule is missing, because it changes one field of a good invoice and expects an error.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| The wrapped invoice fails | The raw text was validated directly. | Extract the JSON between the outer braces first. |
| A total off by 0.001 is rejected | The comparison demanded exact equality. | Allow a small tolerance, such as one cent. |
| The cross-field rule never runs | It was written as a normal method. | Use a model validator in after mode. |
| errors stores exceptions, not messages | The exception object was saved. | Store the first error's message as text. |

## What the result means for the client

Two of five replies were usable, and the other three would have reached finance as silently wrong data. With the schema, each failure is caught with a reason that can drive a retry or a review queue. Tell finance which rules the schema enforces, so they can add the next one they find.

## What to send the client

The schema as code, a list of the rules it enforces in plain words, and the three rejected outputs with their reasons, so finance can see what would have reached them without it.

## Stretch goal

Write a retry message for each rejected output that lists its errors and asks the model for JSON only, ready to send back in a correction loop. Limit the loop to two retries, and send anything still failing to a review queue with its last error, so no invoice is lost or guessed.
