# Self-study guide: Plan an agent's work as a graph with NetworkX

A planning agent produced seven tasks with durations in days and dependencies for a document-search launch. plan.json holds the tasks and, for each task, the tasks it depends on. Before anyone commits to a date, you check the plan as a graph: which tasks can run in parallel, which chain sets the launch date, how long it takes, and whether a proposed change would create a cycle.

## Revise first (in the course)

- decomposition and dependency graphs
- validating plans and replanning
- validating a plan before executing it

## Questions to ask the client first

- **Are durations in working days, and who estimated them?** An agent's estimates need a person's review before they become a date.
- **Can tasks in the same wave really run at the same time?** Parallel on paper needs people and access in practice.
- **What happens if a dependency is added later?** A cycle check before accepting changes keeps the plan possible.

## Ideas you will use

- **Directed graph:** Each dependency is an edge from the prerequisite to the task. nx.DiGraph holds the tasks as nodes and the dependencies as edges.
- **Topological generations:** nx.topological_generations groups tasks into waves: each wave holds the tasks whose prerequisites are all in earlier waves, so a wave's tasks can run together.
- **Longest path:** dag_longest_path finds the chain with the largest total edge weight. Durations belong to tasks, so weight each edge by its target task's duration and add the first task's own duration.
- **Cycle check:** A copy of the graph with the proposed edges added either is still acyclic or is not. is_directed_acyclic_graph answers it without changing the real plan.

## Steps, check by check

1. **Tasks are grouped into parallel waves:** Build the graph and group the tasks into waves, each sorted by name.
2. **The critical path runs through the data work:** Find the critical path, the chain through the data work.
3. **The plan takes 11 days:** Add up the durations of the tasks on the critical path: 11 days.
4. **Making collect wait for launch is a cycle:** Check that making the first task wait for the launch creates a cycle.
5. **A harmless extra dependency is not:** Check that a harmless extra dependency does not.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If the waves are wrong, print the graph's edges and check their direction: prerequisite to task. If the critical path is wrong, print each edge's weight. If the duration is wrong, check the first task's duration is counted once. If a cycle check gives the wrong answer, print the edges of the copied graph after adding the proposed ones, and follow them by hand from the first task.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| Waves come out reversed | Edges point from task to prerequisite. | Add edges from prerequisite to task. |
| The critical path ignores durations | Edges had no weights. | Weight each edge by its target task's duration. |
| has_cycle changes the real plan | Edges were added to G itself. | Copy the graph before adding edges. |
| The duration is too short | Only edge weights were added. | Add up the task durations along the path. |
| A task with no dependencies is missing from the waves | Only tasks with edges were added to the graph. | Add every task as a node first, then the edges. |

## What the result means for the client

The launch is set by the data work (collect, clean, embed, index, launch), 11 days, while the policy review has slack. Tell the delivery manager that staffing the data chain decides the date, and that any new dependency should go through the cycle check before it is accepted. If the agent replans later, run the same three checks on the new plan before anyone updates the launch date, because a plan that looks similar can have a different critical path.

## What to send the client

The waves as a staffing plan, the critical path with its duration, and the list of tasks with slack, sent to the delivery manager before the date is committed.

## Stretch goal

Compute each task's slack (how many days it can slip without moving the launch) and highlight the tasks with none. Then add the proposed review dependency from the second cycle check and see whether the launch date moves.
