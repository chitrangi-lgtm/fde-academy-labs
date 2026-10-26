# Nudges (open only if stuck)

1. Waves: repeatedly take every remaining task whose dependencies are all done; if none is ready but tasks remain, there is a cycle.

2. Critical path: process tasks wave by wave and keep, for each task, the longest chain that ends with it.

## The approach, in plain English (open last)

1. For waves, keep a set of done tasks; repeatedly take every remaining task whose dependencies are all done, sorted, as the next wave.
2. If no task is ready but some remain, the dependencies contain a cycle.
3. has_cycle can reuse the waves logic.
4. For the critical path, go through the tasks wave by wave and remember, for each task, the longest chain ending with it: the best chain among its dependencies plus itself.
5. The critical path is the longest of those chains.
