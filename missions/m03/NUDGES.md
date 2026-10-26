# Nudges (open only if stuck)

1. `conn.executescript(text)` runs a file with several statements; `conn.execute` runs one.

2. Never build SQL with f-strings from user input: pass values as parameters, `conn.execute(sql, (name,))`.
