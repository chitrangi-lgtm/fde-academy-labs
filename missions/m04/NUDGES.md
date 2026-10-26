# Nudges (open only if stuck)

1. Build the group key from the method and `path.strip('/').split('/')[0]`.

2. A replay with the same idempotency key is safe by design; duplicates come from creates without a key.

## The approach, in plain English (open last)

1. Load the file by parsing each non-empty line as JSON.
2. Write a helper that turns a record into its kind of call: the method and the first segment of the path.
3. Count calls and 5xx responses per kind, then divide and round.
4. For duplicates, keep only successful creates that had no idempotency key, count them per order reference, and list the references seen more than once, sorted.
5. Keep the retryable statuses in one named set and test membership.
6. For backoff, return Retry-After when it is given, otherwise the capped exponential value.
