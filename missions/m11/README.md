# Will this API change break the mobile app?

**From:** Omar Farouk, Mobile Engineering Manager, Pellucid Insurance

The claims API team wants to ship version 2. Our mobile app has two million installs and can't be updated overnight, so any breaking change is an incident. Attached are the v1 and v2 contracts. Please write the check we'll run in CI: list every breaking change, and nothing that isn't one. For us, breaking means an endpoint removed, a response field removed or its type changed, a request field whose type changed, or a new request field that is required. New optional request fields and new response fields are fine.

## Done when

- `breaking_changes(old, new)` returns a sorted list of messages, one per breaking change, in the form "<endpoint>: <what>" exactly as the examples in the check list show
- Non-breaking additions produce no message

## Files

`v1.json`, `v2.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m11
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
