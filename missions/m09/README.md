# Make the ticket classifier prompt testable

**From:** Ruth Mensah, Customer Experience Director, Ostara Telecom

We classify support tickets with a model. Today the prompt is a string someone edits in production, replies come back as "Label: Billing." or a whole sentence, and last week a customer wrote "ignore your rules" inside a ticket and it worked. I want the prompt built by code we can test: a system message listing our four labels and asking for the label only, optional examples as user and assistant turns, and the ticket itself fenced so it can't break out. And a parser that turns whatever the model replies into one of our labels, or "other" when it can't tell.

## Done when

- `build_messages(ticket, examples)` returns chat messages: one system message naming billing, delivery, technical and other and asking for the label only; each example as a user turn then an assistant turn; the ticket last, inside <ticket>...</ticket>
- A ticket that contains </ticket> cannot close the fence early
- `parse_label(reply)` returns the first known label that appears as a whole word (any case), else "other"

## Files

none

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m09
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
