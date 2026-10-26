# Self-study guide: Score the agent runs the way the board will ask

Boards and risk committees fund agents that are dependable, not agents that succeed once in a while. A single success rate hides the difference between a task the agent can do sometimes and a task it does every time. Reporting both, with tool accuracy and the cost of each success, is how agent programmes get approved or stopped.

## Revise first (in the course)

- statistics for agent evaluations
- success rate versus reliability over many runs
- reliability statistics

## Read the email like an FDE

The head of automation lists the board's questions, and the criteria define each one. Success rate is over all runs. 'At least once in three tries' is pass at k: any success for a task. 'Reliably every time' is pass hat k: all runs of a task succeed. Tool accuracy counts correct calls over all calls, not an average of per-run rates. Cost per success divides the cost of every run, including failures, by the number of successes. Everything is rounded to three places.

## Questions to ask the client first

- **Are the eight tasks representative of real work, and who chose them?** A small or easy task set flatters any agent.
- **What success rate would the business accept for each task type?** A board decision needs a target, not only a measurement.
- **Should failed runs that cost nothing be treated differently?** Some failures stop early and cheaply; others fail after many expensive steps.

## How each criterion is checked

1. **Success rate over all runs:** success_rate must be successful runs over all runs, rounded.
2. **pass@3: tasks done at least once:** pass_at_k must be the share of tasks with at least one success.
3. **pass^3: tasks done every time:** pass_hat_k must be the share of tasks where every run succeeded.
4. **Steps, tool accuracy and cost per success:** avg_steps, tool_accuracy and cost_per_success must match the definitions in the criteria.
5. **Unreliable tasks are named:** unreliable must name the tasks that succeeded sometimes but not every time, sorted.

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
| Cost per success is too low | Only successful runs' costs were added. | Failures cost money too: add the cost of every run. |
| Tool accuracy differs slightly | Per-run accuracies were averaged. | Divide total correct calls by total calls. |
| pass_hat_k equals pass_at_k | Any and all were mixed up. | pass at k asks 'any success', pass hat k asks 'all successes'. |
| Values are not rounded | The dictionary was returned with raw values. | Round each value to three places. |

## Test yourself before you check

- Make a table of tasks by runs with ticks and crosses, and work out each metric by hand.
- Change one failed run to a success and predict which metrics move.
- Check that pass hat k is never above success rate and never above pass at k.
- Read the unreliable list and think about what the team should investigate.

## What a senior reviewer also looks for

A reviewer would want the number of tasks and runs shown next to every percentage, because three runs per task is a small sample. They would check that definitions are written down with the numbers, so the board compares like with like next quarter, and that the unreliable tasks come with their failing runs for the team to read.

## Stretch goal

Add a confidence interval for the success rate, and report pass hat k per task type so the board sees where reliability is good enough to scale.
