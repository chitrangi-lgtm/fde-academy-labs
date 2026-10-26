# Nudges (open only if stuck)

1. Walk the old contract: for each endpoint and response field, ask whether it still exists in the new one with the same type.

2. Walk the new contract's request fields: a field the old contract didn't have is breaking only if it is required.
