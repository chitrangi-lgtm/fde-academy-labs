# Nudges (open only if stuck)

1. For each record, walk the contract's fields (missing, null, type, enum in that order), then look for fields the contract doesn't know.

2. Check bool before int: in Python, True is an instance of int.

## The approach, in plain English (open last)

1. For each record, walk the contract's fields in order.
2. For a field that is absent, report 'missing' only if it is required, then move on.
3. For a field set to None, report 'null' only if it is not nullable.
4. Otherwise check the type (treating booleans separately from numbers), then the allowed values.
5. After the contract's fields, report any field in the record the contract does not know. For freshness, compare the newest timestamp with now minus the window.
