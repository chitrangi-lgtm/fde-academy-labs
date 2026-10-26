# Self-study guide: Parse what the model actually sends back

Models are asked for JSON and send back JSON wrapped in prose, code fences, trailing commas or wrong values. A parser that rescues what it safely can, validates the rest and tells the model exactly what to fix turns a one-in-ten failure into a self-correcting loop. Structured output is how agents hand work to ordinary software.

## Revise first (in the course)

- extracting JSON robustly from model replies
- validate, then repair: bounded correction loops
- five broken replies, one robust extractor

## Read the email like an FDE

The director lists the ways replies arrive broken: wrapped in a code fence, wrapped in a sentence, or with a trailing comma. Those are syntax problems you may repair. 'When it is clean, sometimes a field is wrong' is a validation problem you must report, not repair. 'Gives us the exact message to send back to the model' asks for a retry prompt that lists every error at once. The criteria fix the field rules and say that tags are optional with a default of an empty list.

## Questions to ask the client first

- **How many retries should the agent get before a person takes over?** Retries cost money and time; a bounded loop needs a clear limit.
- **Should a ticket with an invalid optional field be saved without it?** Dropping bad optional data is sometimes acceptable and sometimes not.
- **Can the model's provider enforce a JSON schema directly?** Strict output modes reduce, but do not remove, the need for validation.

## How each criterion is checked

1. **A fenced, chatty answer is rescued:** extract must find the JSON object inside a chatty reply with a code fence.
2. **Trailing commas are repaired:** extract must repair trailing commas before closing brackets and braces, including nested ones.
3. **No JSON at all is a clear error:** A reply with no JSON object must raise ValueError.
4. **A valid ticket gets default tags:** A valid ticket must come back with tags defaulting to an empty list and no errors.
5. **Every invalid field is reported:** A ticket with several invalid fields must come back as None with one error per field, sorted.
6. **The retry message lists each error and asks for JSON only:** retry_prompt must put each error on its own line starting with '- ' and ask for JSON only.

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
| Only the first error is reported | The function returned at the first failed rule. | Collect all errors, then return them together. |
| A comma inside a string is removed | The repair removed every comma before a bracket. | Remove only commas followed by optional spaces and a closing bracket or brace. |
| '881' passes as a ticket id | The pattern was searched, not fully matched. | Match the whole id against the pattern. |
| Missing tags cause an error | Tags were treated as required. | Default to an empty list when absent. |

## Test yourself before you check

- Feed extract five broken replies you write yourself, including nested trailing commas.
- Break one ticket field at a time and check each gives exactly one error.
- Print the retry prompt and read it as the model would.
- Try a reply with two JSON objects and decide what should happen.

## What a senior reviewer also looks for

A reviewer would check that repairs are limited to syntax and never change values, that every error names its field, and that the retry loop has a fixed limit. They would also ask for the number of rescued, repaired and failed replies to be counted, so the team can see whether a model change makes things better or worse.

## Stretch goal

Add a bounded repair loop that calls a stand-in model with the retry prompt up to two times and returns the first valid ticket, or the last errors.
