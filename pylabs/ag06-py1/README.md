# Plan an agent's work as a graph with NetworkX

**Libraries:** NetworkX · **Level:** Intermediate · about 30 minutes

A planning agent produced seven tasks with durations (in days) and dependencies for a document-search launch. Before anyone commits to a date, check the plan: which tasks can run in parallel, which chain sets the launch date, how long it takes, and whether a proposed change would create a cycle.

Write your code in `lab.py`, then run `python tools/fde_check.py ag06-py1` from the kit's folder.

<details><summary>Hints</summary>

1. `nx.topological_generations(G)` yields the parallel waves.
2. dag_longest_path uses edge weights, but durations belong to tasks: weight each edge by its target task's duration and add the first task's duration yourself.
3. For has_cycle, copy the graph (`G.copy()`), add the edges and use `nx.is_directed_acyclic_graph`.
</details>

## Why it matters

Plans from agents (and people) are graphs. Check them as graphs: parallel waves for staffing, the critical path for the date, and a cycle check before accepting any new dependency.
