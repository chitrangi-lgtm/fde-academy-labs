# Validate and gate tool calls before they run

**From:** Tobias Brandt, Payments Platform Owner, CrestFin Lending Operations

Agents now request refunds through our tool layer. Before any call reaches payments, it must be checked against the tool's schema, with errors precise enough for the agent to fix its call, and refunds above 100 dollars must wait for a human. Our library has no JSON Schema package, so write the subset we use: type, required, enum, minimum, maximum, pattern and additionalProperties false.

## Done when

- `validate(args, schema)` returns a sorted list of errors "<field>: <problem>" with problems "required", "wrong type", "not one of ..." (the allowed values), "below minimum", "above maximum", "does not match pattern", "not allowed" (extra field); types string, number, integer, boolean (bool is neither number nor integer)
- `execute(call, registry, approved=False)` returns {"ok": True, "result": ...} or {"ok": False, "error": ...}: unknown tool -> "unknown tool"; schema errors -> the error list; needs_approval(args) true and not approved -> "approval required"; the tool runs only when everything passes

## Files

none

`provided.py` holds code the client gives you; the checker runs it before your code.

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag02
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
