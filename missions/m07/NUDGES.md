# Nudges (open only if stuck)

1. Give each merge rule its rank (position in the list); at each step, find the adjacent pair with the lowest rank.

2. Replace that pair with the joined token and repeat until no adjacent pair has a rule.

## The approach, in plain English (open last)

1. Load the merge rules and give each pair a rank equal to its position in the list.
2. In bpe, start from the list of characters.
3. Repeatedly look at every adjacent pair, find the one with the lowest rank that has a rule, and join it into one token. Stop when no adjacent pair has a rule.
4. count_tokens splits the text on whitespace and adds up each word's tokens.
5. pack walks the chunks in order with a running total, keeping a chunk only if it still fits.
