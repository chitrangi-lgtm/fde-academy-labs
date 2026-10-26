# Nudges (open only if stuck)

1. Handle the failure modes first, in order: unparseable text, an invalid request, a notification; then dispatch on the method.

2. Tool problems the model can act on (claim not found) are results with isError; malformed calls are JSON-RPC errors.

## The approach, in plain English (open last)

1. Parse the text first; a failure is a parse error with a null id.
2. Check it is a JSON-RPC 2.0 request with a method; otherwise it is an invalid request.
3. A message without an id is a notification: return None.
4. Dispatch on the method: initialize, tools/list and tools/call; anything else is method not found.
5. In tools/call, an unknown tool or missing claim id is invalid params; an unknown claim is a result with isError true; a known claim is text content.
