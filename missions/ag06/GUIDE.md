# Self-study guide: Check the planning agent's plan

Planning agents produce plans that look convincing and are sometimes impossible: a cycle in the dependencies, or a path longer than anyone noticed. Treating the plan as data and checking it like a project manager would is cheap and catches the mistakes models make. Delivery managers want the parallel waves for staffing and the critical path for the date, and the same checks work on plans written by people.

## Revise first (in the course)

- decomposition and dependency graphs
- validating plans and replanning
- ordering a plan into parallel levels

## Read the email like an FDE

The delivery manager asks for three checks a project manager would run. Which tasks can run in parallel: tasks whose dependencies are all done form a wave. Whether the dependencies contain a cycle: the agent produced one before, so this is a real risk. The critical path: the longest chain of tasks by total duration, which sets the earliest finish date. 'No graph library' means plain Python. The criteria ask for each wave sorted.

## Questions to ask the client first

- **Are the durations working days or calendar days?** The launch date depends on weekends and holidays.
- **Can two tasks in the same wave really be staffed at the same time?** Parallel on paper is not parallel if one person does both.
- **What should happen when the agent's plan contains a cycle?** Rejecting it, or asking the agent to replan, are different workflows.

## How each criterion is checked

1. **Parallel waves:** waves must return the tasks grouped wave by wave, each wave sorted.
2. **The plan has no cycle:** has_cycle must say False for the real plan.
3. **A cycle is detected:** has_cycle must say True when a dependency makes the first task depend on the last.
4. **The critical path and its length:** critical_path must return the longest chain and its total days.
5. **A longer review changes the critical path:** When one task gets longer, critical_path must move to a different chain.

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
| waves loops forever on a cycle | Nothing stopped the loop when no task was ready. | Detect the empty wave and stop. |
| The critical path ignores a dependency | Chains were built in the order tasks appear in the file. | Build chains wave by wave, so dependencies are always done first. |
| The path length is right but the chain is wrong | Only totals were kept. | Keep the chain alongside its total. |
| Waves come out in a different order inside | Tasks were not sorted. | Sort each wave. |

## Test yourself before you check

- Draw the plan as boxes and arrows and find the waves by hand.
- Add up the durations of a few chains and find the longest yourself.
- Create a two-task cycle and check has_cycle.
- Make a task with no dependencies and no dependants and see where it lands.

## What a senior reviewer also looks for

A reviewer would check that the plan is never modified while checking, that a cycle is reported with the tasks involved, and that the critical path comes with its tasks' durations so the manager can challenge them. They would also ask what happens when a dependency names a task that does not exist, because models invent task names too.

## Stretch goal

Report the slack of every task that is not on the critical path (how many days it can slip without moving the launch), and the tasks involved when a cycle is found.
