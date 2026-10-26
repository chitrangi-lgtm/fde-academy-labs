# Nudges (open only if stuck)

1. Take the text from the first '{' to the last '}', then remove a comma that comes right before '}' or ']' with a regular expression.

2. Collect every field error before returning, so one retry can fix them all.

## The approach, in plain English (open last)

1. In extract, take the text from the first opening brace to the last closing brace, and raise ValueError when there is none.
2. Remove a comma that comes right before a closing brace or bracket, then parse the JSON, turning a parse failure into ValueError.
3. In parse_ticket, extract the data, then check each field rule and collect every error before returning.
4. Return the ticket with default tags when there are no errors, otherwise None and the sorted errors.
5. In retry_prompt, write one line asking for the JSON object only, then each error on its own line.
