# Stop the runaway agent loop

**From:** Mira Castellanos, Head of Automation, CrestFin Lending Operations

Our order-status agent ran up a large bill overnight: the model kept asking for the same lookup and the loop never ended. Another time a typo in a tool name crashed the whole service. I want the agent loop rewritten so it can't do either: tool errors go back to the model as observations, a repeated identical request is stopped, and there's a hard cap on steps. Stand-in models and our two tools are provided so you can test.

## Done when

- `run_agent(task, model, tools, max_steps=6)` returns {"answer", "steps", "stopped", "history"}
- Each step calls model(history) once. The model returns {"final": text} or {"tool": name, "args": {...}}
- History starts with {"role": "user", "content": task}; each step appends {"role": "assistant", "content": action} and, for tool calls, {"role": "tool", "content": observation as text}
- An unknown tool or a tool that raises becomes an observation starting "error:" and the loop continues
- The third identical request in a row is not executed: stopped = "loop". No final within max_steps: stopped = "max_steps" and answer None. A final answer: stopped = "final"

## Files

none

`provided.py` holds code the client gives you; the checker runs it before your code.

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag01
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
