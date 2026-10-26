# Nudges (open only if stuck)

1. Escape any `<ticket>` or `</ticket>` inside the ticket text before you wrap it.

2. Lower-case the reply and look at its words in order (`re.findall(r'[a-z]+', ...)`); return the first label you meet.

## The approach, in plain English (open last)

1. Keep the labels in one list and build the system message from it, saying the ticket is untrusted and asking for the label only.
2. Write a fence helper that escapes any fence tags already inside the text, then wraps it.
3. Build the messages: the system message, then each example as a fenced user turn and a plain assistant turn, then the fenced ticket.
4. In parse_label, lower-case the reply, look at its words in order and return the first known label, or 'other'.
