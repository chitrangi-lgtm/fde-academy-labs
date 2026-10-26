# Parse what the model actually sends back

**From:** Ruth Mensah, Customer Experience Director, Ostara Telecom

Our ticket-creation agent fails about one time in ten because the model's JSON isn't clean: it comes wrapped in a code fence or a sentence, or with a trailing comma. When it is clean, sometimes a field is wrong. I want a parser that rescues what can be rescued, validates the ticket, and when it fails, gives us the exact message to send back to the model so it can fix its answer.

## Done when

- `extract(raw)` returns the dict inside raw: it may be wrapped in a ```json fence or in prose and may have trailing commas before } or ]; raises ValueError when there is no JSON object
- `parse_ticket(raw)` returns (ticket, []) when valid, or (None, errors) with errors "<field>: <problem>"; rules: ticket_id like TCK-123, priority one of low, medium, high; summary a string of at least 5 characters; tags optional, a list of strings (default [])
- `retry_prompt(errors)` returns a message with each error on its own line starting "- " and asking for JSON only

## Files

none

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag03
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module ag03) records your score.
