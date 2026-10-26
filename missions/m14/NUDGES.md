# Nudges (open only if stuck)

1. Split on blank lines; a block whose lines all start with '|' and whose second line is only dashes, pipes and colons is a table.

2. For a table, emit header line + one data row per chunk (skip the separator line).
