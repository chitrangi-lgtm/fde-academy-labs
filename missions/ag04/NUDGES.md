# Nudges (open only if stuck)

1. Keep a flag per message (pinned or not) and a count of removed messages; build the summary line in context().

2. After each add, loop while over budget: remove the first message that is not pinned and is not the last one.

## The approach, in plain English (open last)

1. Store each message with its role, its masked text and a pinned flag, and keep a count of removed messages.
2. Mask emails first, then runs of seven or more digits with optional spaces or dashes.
3. After each add, while the total words are over budget, remove the oldest message that is neither pinned nor the newest, and count it. Stop if nothing can be removed.
4. In context, return the messages in order, with the summary line first when anything was removed.
