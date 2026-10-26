# Nudges (open only if stuck)

1. Split the input into the cached part of the prefix (prefix x hit rate) and everything else, then price each part.

2. Filter models by p95 first; then take the minimum monthly cost, or None if the list is empty.
