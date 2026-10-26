# Nudges (open only if stuck)

1. Load the state from the file at the start of every call (or start a new one), act only on the current step, and save after each change.

2. Make each step conditional on the saved step: a 'sent' workflow ignores 'approve', so re-running is safe.

## The approach, in plain English (open last)

1. Write a loader that reads the state file, or returns a fresh state with step 'new' and zero counts when the file does not exist.
2. Write a saver that writes the state as JSON.
3. In run, load the state and act only on its current step: a new workflow drafts and moves to waiting.
4. While waiting, an approve moves to sending, saves, sends once, moves to sent and saves; a reject moves to rejected and saves.
5. Every other combination of step and event changes nothing. Return the step.
