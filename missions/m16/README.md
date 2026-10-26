# Pre-retrieval access control and redaction

**From:** Beatriz Santos, Chief Information Security Officer, Ashgrove Mutual

Before our staff assistant goes live, two controls must be in place. First, a person may only ever retrieve documents they're entitled to: same company, classification no higher than their clearance, and for confidential or restricted documents, their own department, unless they are an auditor. Second, anything the assistant shows must have email addresses, phone numbers and real card numbers masked. Our order numbers are long digit strings too; don't mask those (real cards pass the Luhn check).

## Done when

- `visible(user, docs)` returns the sorted ids of documents the user may retrieve under the rules above (levels: public < internal < confidential < restricted)
- `redact(text)` replaces emails with [EMAIL], phone numbers with [PHONE] and 13 to 19 digit card numbers that pass the Luhn check (spaces or dashes allowed) with [CARD], leaving other digit strings alone

## Files

`docs.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m16
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
