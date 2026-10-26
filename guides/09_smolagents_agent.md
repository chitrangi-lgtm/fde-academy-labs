# Lab 09: An invoice-checking agent with Hugging Face smolagents

**Time:** 45–60 minutes · **Level:** Intermediate · **Builds on:** Agentic Module 1 (the agent loop), Module 2 (tool design), FDE Module 15 (agents in production)

## The problem

Summit Agro Foods' accounts team pays about 900 supplier invoices a month. Before paying, a clerk checks two things by
hand: that the supplier's sales tax registration (its tax ID) is active, and that the tax rate on the invoice matches the goods'
Harmonized System (HS) code. If the registration has been cancelled, the company cannot reclaim the input tax, which on a $2,400
pepper invoice is $120 lost. The client wants an assistant that does both checks, explains its decision in one paragraph and never
pays anything itself.

You built this loop from scratch in Agentic Module 1. This lab rebuilds it with **smolagents**, Hugging Face's agent
library, so you can see what a framework gives you, what it hides, and what you still have to design yourself.

## What you'll learn

- How smolagents turns a typed, documented Python function into a tool the model can call.
- How a `ToolCallingAgent` runs the loop: ask the model, run the tool it chose, feed back the observation, repeat until
  the model calls `final_answer` or `max_steps` runs out.
- The difference between a `ToolCallingAgent` (the model emits structured tool calls) and a `CodeAgent` (the model writes
  Python that the framework executes), and why the second needs a sandbox.
- How to swap a scripted model for a real one without changing the agent.

## Before you start

1. Start the labs container from `realtools/`: `docker compose up -d --build` (first run takes a few minutes).
2. Run the lab: `docker compose exec labs python 09_smolagents_agent.py`.
3. Without Docker: `python -m venv .venv`, activate it, `pip install -r requirements.txt`, then `cd labs` and
   `python 09_smolagents_agent.py`.

No API key is needed: a scripted model plays the model's part. To use a real model, set `FDE_LLM_BASE_URL` and
`FDE_LLM_MODEL`, and `FDE_LLM_API_KEY` for hosted providers. Any OpenAI-compatible endpoint works, including a local
Ollama server.

## Key ideas

**Tools are functions with a contract.** The `@tool` decorator reads the function's type hints and its docstring
(including the `Args:` section) and builds the description the model sees. A vague docstring produces vague tool use. A
missing `Args:` entry makes smolagents refuse to build the tool. That refusal is deliberate: the model can only use a
parameter it has been told about.

**The loop is bounded.** `max_steps=5` is your budget guard. A confused model that keeps calling tools is stopped and
the run raises an error, instead of spending money for ever. In production, set the budget from the longest legitimate
path plus one or two steps.

**`final_answer` is a tool.** The agent ends the run by calling a built-in tool named `final_answer`, not by printing
text. So "finishing" is visible in the trace like any other action, and you can validate the answer's shape before it
reaches a user.

**Memory is a list of steps.** `agent.memory.steps` records every model call, tool call, observation and error. That is
your audit log. The lab prints the tool names from it at the end.

**ToolCallingAgent and CodeAgent.** A `CodeAgent` lets the model write Python that calls the tools. That is powerful for
data work, but it means running model-written code. smolagents offers local, Docker, E2B and other executors for it.
For a payments workflow, structured tool calls are easier to audit and to restrict.

## Steps

1. **Run the lab and read the trace.** You should see three steps: `lookup_tax_id` with `TX297674749`, then
   `hs_rate` with `0904`, then `final_answer`. The final line lists the tool calls in order:
   `["lookup_tax_id", "hs_rate", "final_answer"]`. The answer says to hold the invoice because the tax ID is cancelled.

2. **Read the tool descriptions the model sees.** Add `print(lookup_tax_id.description, lookup_tax_id.inputs)` before
   `agent.run`. Compare the output with the docstring. Then delete the `Args:` section from `hs_rate` and run again.
   Note the error and why smolagents insists on it. Put the section back.

3. **Make a tool fail safely.** Change the task to an HS code that isn't in `HS_RATES` (for example `9999`), and
   change the scripted model's second call to match. The tool returns `{"error": ...}` instead of raising. Decide what
   the final answer should say when a check can't be completed. The usual client rule is "hold and escalate", never
   "pay".

4. **Exceed the budget.** Set `max_steps=2` and run. The agent stops before it can answer. Read the exception and decide
   what your application should show the clerk when this happens.

5. **Use a real model (optional).** Point `FDE_LLM_BASE_URL` at a local Ollama server (`ollama run qwen2.5:7b`) and
   run again. Real models sometimes skip a check or call `final_answer` too early. Compare the trace with the scripted
   one. Then strengthen the instruction: add a system rule through `ToolCallingAgent(..., instructions=...)` that says
   both checks are mandatory.

6. **Add a guard the model can't skip.** Write a function that inspects `agent.memory.steps` after the run and refuses
   the answer unless both `lookup_tax_id` and `hs_rate` were called. That is the "verify the trajectory, not just the
   answer" idea from Agentic Module 10.

## Check yourself

<details><summary>Why return an error dictionary from a tool instead of raising an exception?</summary>
The model can read a returned error and react, for example by asking for a different input or explaining that a check
couldn't be done. An unhandled exception ends the step with a framework error the model may misread. Return errors as
data, and raise only for bugs.
</details>

<details><summary>The model called final_answer after only one check. Whose fault is that, and how do you prevent it?</summary>
It's a design gap, not just a model mistake. Prevent it two ways: make the instruction explicit ("call both tools
before answering"), and add a programmatic check of the trajectory (step 6) so an incomplete run never reaches a clerk.
</details>

<details><summary>When would you choose a CodeAgent over a ToolCallingAgent?</summary>
When the task is open-ended data manipulation, where writing a few lines of Python is much easier than chaining many tool
calls, and you can run the code in an isolated executor. For money movement or anything that needs a clear audit trail,
prefer structured tool calls.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `Tool ... has no description for argument` on start-up | The docstring's `Args:` section is missing or misnamed | Document every parameter under `Args:` with the exact parameter name |
| The agent loops until `max_steps` | The model never sees a result it trusts, or the task is ambiguous | Return clear observations, state the stopping condition in the task, keep `max_steps` low |
| Real model returns prose instead of a tool call | The model doesn't support tool calling well | Use a model trained for tool use, or try a `CodeAgent` |
| `Connection refused` with a local model | Docker can't reach your host's Ollama | Use `http://host.docker.internal:11434/v1` as the base URL |

## Take it further

- Add a third tool, `supplier_bank_change(tax_id)`, that flags a recently changed bank account, a common invoice-fraud
  signal. Make the agent hold any invoice with a recent change.
- Replace the dictionaries with an HTTP call to a mock registry, with a two-second timeout and one retry.
- Log each run's steps as JSON lines and write a test that replays a stored run.

## In a real client project

- Keep the agent read-only. It recommends; a person or a separate, audited service pays.
- Version the tool descriptions like code, because changing a docstring changes behaviour.
- Record the model name, tool versions and every step for each decision. Auditors will ask why an invoice was held.
