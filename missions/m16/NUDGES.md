# Nudges (open only if stuck)

1. Check the rules in order: tenant, clearance (compare positions in the levels list), then department for confidential and restricted, unless auditor.

2. Find candidate digit runs (digits with optional spaces or dashes), strip separators, and mask only those whose length is 13 to 19 and pass Luhn. Do cards before phones.

## The approach, in plain English (open last)

1. Keep the levels in one ordered list and compare positions.
2. Write one function that decides a single user and document by the rules in the email's order, and use it for every document.
3. For redaction, mask emails first.
4. Then find runs of digits with optional spaces or dashes, strip the separators, and replace a run with [CARD] only if its length is 13 to 19 and it passes Luhn.
5. Then mask phone numbers in the formats shown.
