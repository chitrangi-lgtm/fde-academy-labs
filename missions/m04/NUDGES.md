# Nudges (open only if stuck)

1. Build the group key from the method and `path.strip('/').split('/')[0]`.

2. A replay with the same idempotency key is safe by design; duplicates come from creates without a key.
