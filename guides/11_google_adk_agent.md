# Lab 11: A loan pre-check agent with Google's Agent Development Kit (ADK)

**Time:** 45–60 minutes · **Level:** Intermediate · **Builds on:** Agentic Module 1 (agent loop), Module 4 (state and memory), Module 11 (observability), P7 (agent platforms)

## The problem

CrestFin's branch staff field about 300 personal-loan enquiries a day. For each one they look up the applicant's credit
band, work out the monthly instalment, and quote a figure, while being careful never to promise approval. That decision belongs to a
credit officer. The client wants an assistant for branch staff that does the two lookups in the right order and records
every step for audit.

**ADK** is Google's open-source agent framework, used with Gemini on Vertex AI and in Google Agentspace, and it works
with other providers through LiteLLM. Its central ideas are the ones you need for this client: tools from plain
functions, sessions that hold state, and an event stream you can log.

## What you'll learn

- How an `LlmAgent` is configured: model, instruction, tools and `output_key`.
- How ADK turns a typed function with a docstring into a tool.
- How a `Runner` executes a turn inside a session and yields **events**: model replies, function calls and function
  results.
- How session state (`output_key`) carries a result forward, and how a custom `BaseLlm` lets you test without a model.

## Before you start

Run `docker compose exec labs python 11_google_adk_agent.py`, or run it in a local virtual environment with
`requirements.txt` installed. The scripted model needs no key.

To use a real model:
- **Gemini:** set `GOOGLE_API_KEY` and `ADK_MODEL=gemini-…`.
- **Any provider LiteLLM supports:** install `google-adk[extensions]` and set `ADK_MODEL=openai/<model>`, plus
  `OPENAI_API_BASE` and `OPENAI_API_KEY`.

## Key ideas

**Instructions are policy.** The agent's instruction says to call `get_credit_band` before quoting and never to promise
approval. An instruction steers a real model but doesn't enforce anything, so step 5 adds a callback that does.

**Function tools.** ADK reads the parameter names, types and docstring of `get_credit_band(taxpayer_id: str)` and
`monthly_instalment(principal_usd, annual_rate_percent, months)` to build the tool declarations the model sees. Use clear
units in names (`principal_usd`, `annual_rate_percent`), because they prevent the classic "11.5 or 0.115?" bug.

**Sessions and events.** `InMemoryRunner` creates a session service, and every `run_async` call adds events to the
session. One user question here produces six events: the user message, a call and a result for each tool, and the final
reply. Those events are what you export to tracing (OpenTelemetry, from Agentic Module 11) and keep for audit.

**State.** `output_key="precheck_summary"` stores the agent's final text in session state, where later agents in a
workflow, or a later turn, can read it. In production, swap the in-memory session service for a database-backed one.

**A model you can script.** `ScriptedLlm` subclasses `BaseLlm` and implements `generate_content_async`. It reads the
function responses already in the request to decide what to do next. The same technique is how you write deterministic
tests for an agent, with no network and the same answers every time.

## Steps

1. **Run the lab.** You should see:
   - `calls get_credit_band({'taxpayer_id': 'TP28746677'})`, then its result (band A, score 781);
   - the instalment call and its result ($824 a month);
   - the final reply, then the saved session state and "events in the session: 6".

2. **Check the instalment maths yourself.** With r = 11.5/1200 and n = 36, instalment = P·r·(1+r)^n / ((1+r)^n − 1). Work it out for
   P = $25,000 and compare with the tool. Then change the tool so it raises an error if `annual_rate_percent` is below
   1 (someone passed 0.115). A quote that is 100 times too small is worse than no quote.

3. **Handle a missing bureau record.** Change the question and the scripted model to use taxpayer ID `TP00000000`. The tool
   returns an error dictionary. Decide what the agent should say. The usual rule is "no quote without a bureau record".
   Make the scripted model say it.

4. **Inspect the events.** Print `event.id`, `event.author` and `event.timestamp` for every event. Map each one to a
   line you would want in an audit log, and decide which fields contain personal data (the taxpayer ID) that must be masked before
   logging.

5. **Enforce the order with a callback.** Add a `before_tool_callback` to the agent that blocks `monthly_instalment` unless
   `get_credit_band` has already run in this session. The callback receives the tool, its arguments and a context;
   return a dictionary to short-circuit the call. Make the scripted model call `monthly_instalment` first and confirm the
   callback stops it.

6. **Use a real model (optional).** Point `ADK_MODEL` at Gemini or a LiteLLM provider, ask the same question, and
   compare the event stream with the scripted run. Check that your callback still enforces the order.

## Check yourself

<details><summary>Why use an output_key instead of reading the final event's text?</summary>
State is part of the session, so later turns and other agents in a workflow can read it without parsing events, and it
persists with the session when you use a persistent session service.
</details>

<details><summary>The instruction says "never promise approval". Is that enough?</summary>
No. Instructions guide a real model but can be ignored or overridden by injected text. Add an after-model check (an
`after_model_callback`, or a validation step in your application) that blocks replies promising approval, and keep the
decision with a credit officer.
</details>

<details><summary>Which event fields would you mask before sending traces to a shared observability tool?</summary>
The taxpayer ID in the tool arguments and any names or amounts that identify the applicant. Keep a hashed applicant ID for
correlation, as in P2 and FDE Module 16.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| The model passes `0.115` as the rate | The parameter name and docstring don't state the unit | Name units in parameters and validate ranges in the tool |
| `ImportError: LiteLLM support requires…` | LiteLlm needs the extensions extra | `pip install "google-adk[extensions]"` |
| State is empty after the run | `output_key` not set, or a different session ID was read | Set `output_key` and read the same session |
| No events printed | The loop exited before iterating | Iterate `runner.run_async(...)` with `async for` inside `asyncio.run` |

## Take it further

- Add a second agent, `affordability_checker`, that reads `precheck_summary` from state and checks the instalment against declared
  income. Run both in a `SequentialAgent`.
- Replace `InMemoryRunner` with a `Runner` using a database session service, and resume a session after a restart.
- Export the events as OpenTelemetry spans to the collector from lab 04.

## In a real client project

- Keep quotes and decisions apart: the agent can quote, but only a credit officer approves.
- Mask taxpayer IDs and other personal data in logs and traces; keep the unmasked record only in the system of record.
- Pin the ADK version and test the event stream in CI, because framework upgrades can change event shapes.
