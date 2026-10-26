# Nudges (open only if stuck)

1. Handle the failure modes first, in order: unparseable text, an invalid request, a notification; then dispatch on the method.

2. Tool problems the model can act on (claim not found) are results with isError; malformed calls are JSON-RPC errors.
