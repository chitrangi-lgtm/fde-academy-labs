# Self-study guide: Stop the runaway agent loop

Runaway agent loops are the first production incident most agent teams have: a model that keeps asking for the same lookup can spend a month's budget overnight, and one bad tool name can crash a service. Every serious agent framework ships the same three guards, and clients expect you to build them in from the first version, not after the first bill.

## Revise first (in the course)

- the agent loop in plain Python
- stop conditions and loop guards
- a runaway loop meeting its guards

## Read the email like an FDE

The head of automation describes two incidents, and each becomes a guard. The overnight bill came from a repeated identical request and a loop with no end, so you need repeat detection and a hard step cap. The crash came from a typo in a tool name, so tool errors must become observations the model can read, not exceptions. The acceptance criteria fix the details: exactly what goes into the history and in what order, that the third identical request in a row is not executed, and the three values of 'stopped'.

## Questions to ask the client first

- **What should the user see when the loop is stopped for repeating itself?** A clear fallback message is better than silence or a raw error.
- **Is the step cap the same for every task, or should some tasks get more?** A single cap is simple; per-task budgets fit real workloads better.
- **Do you also want a cost cap in tokens or dollars?** Steps limit loops, but long steps can still be expensive.

## How each criterion is checked

1. **A normal run ends with the final answer:** A normal run with one tool call and a final answer must return the answer, stop as 'final' after two steps, and record the tool's observation.
2. **An unknown tool becomes an error observation, not a crash:** A call to a misspelled tool must produce an observation starting 'error:' that says the tool is unknown, and the run must still finish.
3. **A tool that raises becomes an error observation:** A tool that raises because of missing arguments must produce an 'error:' observation, and the run must finish.
4. **A repeated request is stopped before the third call:** A model that repeats the same request must be stopped as 'loop', with the tool executed only twice.
5. **A model that never finishes hits the step cap:** A model that never gives a final answer must stop as 'max_steps' after six steps with no answer.

## How to work it

1. Read the email twice: once for the story, then with a pen, underlining every number, every rule and every 'must' or 'never'. Those words become the checks.
2. Turn the acceptance criteria into your own checklist, one line per criterion, and decide how you will see each one working before you build it.
3. Open the data files and the provided code before writing anything. Real files hold the awkward cases (blanks, duplicates, odd formats) the checks use.
4. Build the smallest piece that runs, print its result, and compare it with what you worked out by hand.
5. Add the next rule, run again, and keep each business rule in one obvious, named place.
6. Press Check only when your own prints agree with the criteria, then read each failing criterion's message before you change any code.
7. When it passes, read your code as the client's reviewer would, then compare it with the debrief.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| The repeated tool runs three times | Repeats were counted after the tool ran. | Count and stop before executing the third identical request. |
| A typo in a tool name crashes the run | The tool was looked up directly in the dictionary. | Look it up safely and turn a missing tool into an error observation. |
| Repeat detection misses identical calls | Arguments were compared as dictionaries in different orders, or not at all. | Compare the tool name and the arguments together in a stable form. |
| steps is one too many or too few | The counter started at 0 or was not returned. | Count steps from 1 and return the step number with each result. |

## Test yourself before you check

- Print the history after each run and read it as the model would see it.
- Use the scripted stand-in model with a misspelled tool name and confirm the run continues.
- Count how many times the tool function was actually called in the repeat case.
- Set max_steps to 1 and to 2 and check the results.

## What a senior reviewer also looks for

A reviewer would check that every exit returns the same shape, that the guards are named and easy to find, and that observations for errors are written for the model to understand. They would also ask for each stop to be logged with its reason, because 'stopped: loop' is exactly what the operations team will want to count.

## Stretch goal

Add a token or cost budget alongside the step cap, with each step reporting its cost, and stop with 'budget' when the total passes the limit.
