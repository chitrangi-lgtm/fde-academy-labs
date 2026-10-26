# Structured output with a validate-and-retry loop

**Libraries:** pydantic · **Level:** Intermediate · about 30 minutes

A support agent turns customer emails into tickets. The first answer from the model is chatty and uses a priority the system does not know; the second, after a corrective message, is clean. Build the loop a production team would: extract the JSON, validate it, and if it fails, write a retry message that names each field and the allowed values.

Write your code in `lab.py`, then run `python tools/fde_check.py ag03-py1` from the kit's folder. `GUIDE.md` has the ideas, the steps check by check and the common mistakes.

<details><summary>Hints</summary>

1. Restrict fields with `Literal['low', 'medium', 'high']` and `Literal['payments', 'account', 'delivery', 'other']`; `Field(pattern=r'^TCK-\d+$')` for the id.
2. `exc.errors()` lists each problem with its `loc` (the field) and `msg`; for a Literal the message already lists the allowed values.
3. Loop over `attempts`, count each one, stop at the first that validates.
</details>

## Why it matters

Structured output is a loop, not a single call: extract, validate, and on failure tell the model exactly which fields were wrong and what is allowed. Cap the retries and log every failure.
