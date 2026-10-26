# Check the partner feed against its data contract

**From:** Rhys Morgan, Data Integration Lead, Albion Claims (capstone client)

The claims-status assistant depends on the partner's hourly claims feed. We agreed a data contract with them: field types, required fields, allowed values, nullability and freshness. Every hour, before anything loads, I want a check that lists each violation by row and field, and tells me whether the feed is fresh. The contract and a sample batch are attached.

## Done when

- `violations(contract, records)` returns a sorted list of (row index, field, problem) with problems: "missing", "null", "wrong type", "not allowed" (value outside the enum), "unexpected field"
- Types: string, integer (bool is not an integer), number (integer or float, not bool), boolean
- A nullable field may be None; a field that is not required may be absent
- `is_fresh(contract, records, now)` is True when the newest updated_at is within freshness_hours of now (ISO timestamps)

## Files

`contract.json`, `batch.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m22
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
