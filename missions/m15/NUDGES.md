# Nudges (open only if stuck)

1. Load the state from the file at the start of every call (or start a new one), act only on the current step, and save after each change.

2. Make each step conditional on the saved step: a 'sent' workflow ignores 'approve', so re-running is safe.
