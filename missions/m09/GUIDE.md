# Self-study guide: Make the ticket classifier prompt testable

A prompt edited by hand in production is untested code. Enterprises need prompts built by functions with tests, model replies parsed into known values with a safe default, and untrusted text that cannot change the instructions. Prompt injection through customer text is a real incident class, and the defences here are the first ones a security review asks about.

## Revise first (in the course)

- message roles and delimiting untrusted text
- prompts as versioned, tested code
- assembling messages with fenced, untrusted input

## Read the email like an FDE

Each problem in the email becomes a requirement. 'A string someone edits in production' means the prompt is built by a function you can test. 'Label: Billing.' or a whole sentence means the parser must tolerate punctuation, case and extra words. 'Ignore your rules inside a ticket' is prompt injection: the ticket goes inside a fence, and the fence must survive a ticket that contains the closing tag. 'Optional examples as user and assistant turns' fixes the message order exactly. 'Other when it can't tell' is the safe default.

## Questions to ask the client first

- **Who may change the labels, and how is a change released?** Labels in code need an owner and a release process, or production drifts again.
- **What should happen to tickets classified as other?** If 'other' goes to a human queue, its volume is a staffing question.
- **Can a ticket belong to two labels at once?** Single-label classification forces a choice the business may not want.

## How each criterion is checked

1. **The system message lists all labels and asks for the label only:** The first message must be a system message that names all four labels and asks for the label only.
2. **Examples become user and assistant turns:** Two examples must become user, assistant, user, assistant turns between the system message and the ticket, with the assistant turn holding just the label.
3. **The ticket is fenced:** The last message must hold the ticket text inside exactly one opening fence.
4. **A ticket cannot close the fence early:** A ticket containing the closing tag must still produce exactly one closing tag in the message.
5. **Replies are normalised:** parse_label must turn replies with prefixes, punctuation, spaces and capital letters into the right label.
6. **An unclear reply becomes other:** A reply with no label, or an empty reply, must become 'other'.

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
| The injection test fails | The ticket was wrapped without escaping the tags inside it. | Escape or replace any fence tags in the text before wrapping. |
| 'Label: Billing.' becomes other | The reply was compared as a whole string. | Look at the words inside the reply. |
| 'technically' is read as technical | Substring matching was used. | Match whole words only. |
| The examples are in the system message | Examples were pasted into the instructions. | Send each example as its own user and assistant turn. |

## Test yourself before you check

- Print the messages for a ticket and two examples and read them as the model would.
- Try a ticket with both tags inside it and count the tags in the result.
- Feed parse_label ten strange replies, including an empty one and one in capitals.
- Change the labels list and check the system message follows.

## What a senior reviewer also looks for

A reviewer would check that the labels exist in one place only, that the system message says plainly that instructions inside the ticket must be ignored, and that the parser never raises. They would also ask for the prompt to carry a version number, so a change in classification can be traced to a prompt change.

## Stretch goal

Return a confidence flag from parse_label (exact label, label found in a sentence, or defaulted), and count the defaulted cases so the team can see when the prompt needs work.
