# Nudges (open only if stuck)

1. Escape any `<ticket>` or `</ticket>` inside the ticket text before you wrap it.

2. Lower-case the reply and look at its words in order (`re.findall(r'[a-z]+', ...)`); return the first label you meet.
