# Nudges (open only if stuck)

1. For each record, walk the contract's fields (missing, null, type, enum in that order), then look for fields the contract doesn't know.

2. Check bool before int: in Python, True is an instance of int.
