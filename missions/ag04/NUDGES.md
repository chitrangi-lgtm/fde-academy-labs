# Nudges (open only if stuck)

1. Keep a flag per message (pinned or not) and a count of removed messages; build the summary line in context().

2. After each add, loop while over budget: remove the first message that is not pinned and is not the last one.
