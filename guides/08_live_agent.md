# Lab 08: The agent loop as a LangGraph graph against a real model

**Time:** 45 minutes · **Level:** Intermediate · **Builds on:** Professional Practice P7, Agentic Module 1 (the agent loop), Agentic Module 2 (tool design)

## The problem

An online retailer's support team wants an assistant that answers "where is my order?" and "can I return it?" by
checking the order system and the returns policy, rather than guessing. You built this loop by hand in Agentic Module 1
and in the sandbox's live lab. Here you build the same loop as a **LangGraph** graph and run it against a real language
model on your machine or a hosted one, so you can see how a real model behaves inside your loop.

## What you'll learn

- How to express the agent loop as a graph: a model node, a tools node and a conditional edge.
- How to keep a step budget in the graph's state and stop when it runs out.
- How to call any OpenAI-compatible endpoint (a local Ollama or vLLM server, or a hosted provider) with only the
  standard library.
- What real models do differently from a scripted one: skipping tools, inventing them or answering early.

## Before you start

1. From `realtools/`: `docker compose up -d --build`.
2. Run `docker compose exec labs python 08_live_agent.py`. With no model configured, a scripted stand-in plays the model.
3. To use a local model, install [Ollama](https://ollama.com), run `ollama pull qwen2.5:7b`, then:
   `docker compose exec -e FDE_LLM_BASE_URL=http://host.docker.internal:11434/v1 -e FDE_LLM_MODEL=qwen2.5:7b labs python 08_live_agent.py`.
4. For a hosted provider, also pass `-e FDE_LLM_API_KEY=...`. Keys are read from the environment, never written to files.

## Key ideas

**Nodes do the work; edges decide what's next.** `model_node` calls the model and appends its reply. `tools_node` runs
the tool the model asked for and appends the result. `route` reads the last reply: if it's a tool call and the budget
isn't spent, go to `tools`; otherwise end.

**State carries the conversation and the budget.** `messages` is the full conversation; `steps` counts model calls.
Because each node returns new state, LangGraph can checkpoint, stream or inspect every step.

**Tools are looked up, never executed by name.** `TOOLS.get(...)` only runs functions in a fixed dictionary. An
unknown tool name returns an error result, and a wrong argument returns the `TypeError` message, both of which the model
can read and correct.

**The protocol is plain JSON over HTTP.** `chat()` posts to `/chat/completions` with `urllib`. The same code works with
OpenAI, Azure OpenAI, vLLM and Ollama, because they share this API shape.

## Steps

1. **Run with the scripted model.** Expected output:
   `model (step 1): {"tool": "order_status", "args": {"order_id": "A12"}}`, then the tool result with status `shipped` and
   `eta_days` 2, `model (step 2): {"tool": "refund_policy", "args": {}}`, its result (7 days, unused and in the original
   packaging), `model (step 3): {"answer": ...}`, and finally
   `answer after 3 model calls: Order A12 has shipped and arrives in 2 days; you can return it within 7 days if unused.`

2. **Draw the graph.** Add `print(build().get_graph().draw_ascii())` (install `grandalf` if asked) or `draw_mermaid()`, and
   match each box and arrow to the code.

3. **Run with a real model.** Configure a model as in "Before you start" and run. Compare the trace with the scripted one.
   Did it call both tools? Did it add text around the JSON? Did the final answer use only the tool results?

4. **Lower the budget.** Set `MAX_STEPS = 2` and run. The graph stops after two model calls, and the last message is a
   tool request, not an answer. Change the ending so the user gets a clear message, such as "I couldn't finish; a person
   will follow up", whenever the budget runs out.

5. **Handle an invented tool.** Make the scripted model's second reply ask for `{"tool": "cancel_order", "args": {}}` and
   run. The tools node returns `unknown tool cancel_order`, and the model gets another chance. Decide whether an unknown
   tool should end the run in production.

6. **Add a guard node.** Add a node between `model` and `tools` that rejects any tool call not on an allow-list for the
   signed-in user's role, and returns an error result instead.

## Check yourself

<details><summary>Why is the step budget checked in route() rather than inside the model node?</summary>
The routing function decides whether the loop continues. Checking there means no tool runs and no further model call is
made once the budget is spent, and the decision is visible in one place.
</details>

<details><summary>What are the risks of treating a non-JSON reply as the final answer?</summary>
A model that adds prose around a tool call, or answers before checking, would end the run with an unverified answer.
Some teams instead reject non-JSON replies and ask again, within the budget.
</details>

<details><summary>Why does the same code work with Ollama and hosted providers?</summary>
They all implement the OpenAI-compatible `/chat/completions` API, so only the base URL, the model name and the key
change.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `Connection refused` to `localhost:11434` from Docker | Inside a container, localhost is the container | Use `http://host.docker.internal:11434/v1` |
| `HTTP Error 401` | Missing or wrong API key for a hosted provider | Pass `-e FDE_LLM_API_KEY=...` |
| The model answers in prose without calling tools | A small or non-instruction-tuned model | Try a larger instruction-tuned model, or add a worked example to the system prompt |
| The loop always stops at the budget | The model keeps calling tools, often because results don't answer the question | Check the tool results and make the stopping condition explicit in the system prompt |

## Take it further

- Add a SQLite checkpointer (see lab 01) so a conversation can be resumed later.
- Stream each node's output with `graph.stream(...)` and show progress to the user.
- Record each run's tool calls and compare a real model's trajectories over 20 runs: how often does it skip a tool?

## In a real client project

- Use the provider's native tool-calling API where available instead of parsing JSON from text.
- Enforce permissions in code before every tool call, based on the user's verified identity.
- Log the model, prompt version, tool calls and results of every run for support and audit.
