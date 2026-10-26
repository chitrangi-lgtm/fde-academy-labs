# Nudges (open only if stuck)

1. Split on blank lines; a block whose lines all start with '|' and whose second line is only dashes, pipes and colons is a table.

2. For a table, emit header line + one data row per chunk (skip the separator line).

## The approach, in plain English (open last)

1. Split each document's text on blank lines into blocks.
2. Decide whether a block is a table: every line starts with a pipe and the second line holds only dashes, pipes, colons and spaces.
3. For a table, emit one chunk per data row: the header line, a newline, then the row. Skip the separator line. Other blocks become one chunk each.
4. Number the chunks from 1 within each document and attach the tenant and document id.
5. In search, keep the asking tenant's chunks first, then score each by distinct query words found and sort with the tie-breaks from the criteria.
