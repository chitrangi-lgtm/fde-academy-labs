# Validate tool-call arguments with JSON Schema

**Libraries:** jsonschema · **Level:** Intermediate · about 30 minutes

An agent can call create_refund. Before any call reaches the payments system, the platform team wants every argument checked against the tool's JSON Schema, with a clear field name in each rejection so the agent can correct itself. Six calls from last night's logs are waiting.

Write your code in `lab.py`, then run `python tools/fde_check.py ag02-py1` from the kit's folder.

<details><summary>Hints</summary>

1. `errors = list(Draft202012Validator(schema).iter_errors(args))`; an empty list means valid.
2. For most errors the field is `error.path[0]`. A missing property has an empty path: the name is in `error.message` ("'reason' is a required property").
3. An extra property is reported by additionalProperties: its message ends with "('approve' was unexpected)". `re.findall(r"'([^']+)'", error.message)` gets the quoted names.
</details>

## Why it matters

Validate every tool call against its schema before it touches a real system, and return the field name: that one detail lets the agent repair its own call instead of looping or giving up.
