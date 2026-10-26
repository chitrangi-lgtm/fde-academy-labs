# Nudges (open only if stuck)

1. Replace the endless while with `for step in range(1, max_steps + 1)` and return max_steps after it.

2. Remember the previous (tool, args) and count repeats; wrap the tool call in try/except and turn errors into observations.
