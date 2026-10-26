# Nudges (open only if stuck)

1. Take the text from the first '{' to the last '}', then remove a comma that comes right before '}' or ']' with a regular expression.

2. Collect every field error before returning, so one retry can fix them all.
