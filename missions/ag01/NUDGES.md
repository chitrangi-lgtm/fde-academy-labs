# Nudges (open only if stuck)

1. Replace the endless while with `for step in range(1, max_steps + 1)` and return max_steps after it.

2. Remember the previous (tool, args) and count repeats; wrap the tool call in try/except and turn errors into observations.

## The approach, in plain English (open last)

1. Start the history with the user's task.
2. Loop over a fixed number of steps instead of an endless while. In each step call the model once and append its action to the history.
3. If the action is final, return the answer with stopped 'final'.
4. Otherwise compare the requested tool and arguments with the previous request and count repeats; on the third identical request in a row, stop with 'loop' before running it.
5. Run the tool inside a try/except. An unknown tool or an exception becomes an observation starting 'error:'. Append the observation. If the loop ends, return 'max_steps' with no answer.
