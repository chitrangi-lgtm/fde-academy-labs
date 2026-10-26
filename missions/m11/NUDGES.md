# Nudges (open only if stuck)

1. Walk the old contract: for each endpoint and response field, ask whether it still exists in the new one with the same type.

2. Walk the new contract's request fields: a field the old contract didn't have is breaking only if it is required.

## The approach, in plain English (open last)

1. Load both contracts.
2. Walk the old contract's endpoints: a missing endpoint is one message and nothing more for it.
3. For an endpoint that remains, walk the old response fields: missing, or a different type, is breaking.
4. Walk the new request fields: a field the old version did not have is breaking only if required; a field whose type changed is breaking.
5. Build each message in the exact format of the examples and return them sorted.
