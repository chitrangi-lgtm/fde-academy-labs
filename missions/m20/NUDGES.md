# Nudges (open only if stuck)

1. Look up each required control's status in the register (a control that is not there is missing).

2. Decide Yes, Partial or No from the list of statuses, then gather evidence only from implemented or partial controls.

## The approach, in plain English (open last)

1. Load the questionnaire and the register.
2. For each question, look up each required control's status, treating a control that is not in the register as missing.
3. Decide the verdict from the list of statuses using the three rules in order.
4. Collect evidence only from controls that are implemented or partial, and sort it.
5. gaps keeps the question ids whose answer is not Yes, sorted.
