# Nudges (open only if stuck)

1. Check required fields first, then each provided field: unknown field, type, then enum, bounds and pattern.

2. In execute, the order matters: unknown tool, validation, approval, and only then call the function.

## The approach, in plain English (open last)

1. Keep a small table of type checks, with booleans handled separately from numbers.
2. In validate, first report each required field that is missing.
3. Then walk the provided fields: an unknown field is 'not allowed' when extra fields are forbidden; otherwise check the type, and only if the type is right, check allowed values, bounds and pattern.
4. Return the errors sorted.
5. In execute, check in this order: the tool exists, the arguments validate, approval is satisfied; only then call the tool and return its result.
