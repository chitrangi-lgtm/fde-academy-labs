# Nudges (open only if stuck)

1. Split the input into the cached part of the prefix (prefix x hit rate) and everything else, then price each part.

2. Filter models by p95 first; then take the minimum monthly cost, or None if the list is empty.

## The approach, in plain English (open last)

1. Load the models and traffic once.
2. In request_cost, split the input tokens: the cached part of the prefix (prefix times hit rate) and everything else (the rest of the prefix plus the conversation).
3. Price the uncached input, the cached input and the output with their own per-million prices, and add them.
4. monthly_cost multiplies one request by requests a day and 30 days, rounded to cents.
5. cheapest keeps the models within the latency target and returns the name with the lowest monthly cost, or None.
