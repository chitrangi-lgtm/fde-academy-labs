# Lab 13: A policy researcher and a briefing writer in a CrewAI crew

**Time:** 45–60 minutes · **Level:** Intermediate · **Builds on:** Agentic Module 6 (planning), Module 7 (multi-agent), FDE Module 24 (steering committees)

## The problem

Every fortnight, CrestFin's sponsor for the small-business lending pilot wants a five-line steering note: the decision needed,
the main risk, the ask, the measure and the next review date. Writing it means finding the policy rules that constrain
the pilot and turning them into language an executive acts on. The client wants that split into two roles:
- a **researcher** who searches the policies and reports rules with their IDs;
- a **writer** who turns the research into the note.

**CrewAI** models work as a crew of role-playing agents with tasks, which makes this kind of hand-off explicit.

## What you'll learn

- CrewAI's vocabulary: an `Agent` has a role, goal, backstory, tools and model; a `Task` has a description, an expected
  output and an agent; a `Crew` runs tasks in a `Process`.
- How `context=[research]` passes one task's output into the next. This is the hand-off at the heart of multi-agent work.
- How CrewAI's tool loop works (Thought → Action → Action Input → Observation → Final Answer) and how to bound it with
  `max_iter`.
- How to write a custom `BaseLLM` so a crew runs offline and deterministically.

## Before you start

Run `docker compose exec labs python 13_crewai_crew.py`, or run it in a local virtual environment with
`requirements.txt` installed. The lab turns off CrewAI's telemetry so it stays offline. A scripted model plays both
agents. Set the `FDE_LLM_*` variables to use a real OpenAI-compatible model through `crewai.LLM`.

## Key ideas

**Roles shape behaviour.** The role, goal and backstory become part of each agent's prompt. "You always quote the policy
ID" in the researcher's backstory is why its output is checkable. Write them like a job description, not like a
personality.

**Expected output is a contract.** "Exactly five numbered lines: decision, risk, ask, measure, next review" tells the
writer what done looks like, and gives you something to validate. If the output doesn't match, treat it as a failed task.

**Context is the hand-off.** `Task(..., context=[research])` puts the researcher's final answer into the writer's prompt.
Without it, the writer would invent policy details. In the sequential process, tasks run in list order, and each sees
the outputs named in its context.

**The tool loop and its limit.** The researcher's model replies in CrewAI's text format. The `Action:` and
`Action Input:` lines are parsed and the tool runs. Its result comes back as the observation, and the loop ends at
`Final Answer:`. `max_iter=4` caps the loop. The trace line `[tool] search_policies(...) -> 2 policy lines` shows that
the tool really ran.

**Scripted models need care.** The first version of this lab's scripted model checked for the word "Observation" to
decide whether the tool had run. CrewAI's own instructions contain that word, so the model skipped the tool and went
straight to a final answer, which still *looked* right. The fix was to check for the tool's actual output (`POL-2.9:`).
Always prove a tool ran; don't infer it from a plausible answer.

## Steps

1. **Run the lab.** Expect:
   - the tool trace line;
   - the researcher's answer citing POL-2.9 (two-officer approval above $500,000) and POL-4.2 (2% monthly late
     interest);
   - the writer's five numbered lines, which use both IDs.

2. **Prove the hand-off.** Remove `context=[research]` from the brief task and ask yourself what the writer would know.
   With a real model, run it and check whether the policy IDs survive. Put the context back.

3. **Validate the expected output.** After `kickoff()`, check that the writer's output has exactly five numbered lines
   and mentions every policy ID the researcher found. Make the script exit with an error if not. That is the "eval the
   deliverable" step from P8.

4. **Search for something missing.** Change the researcher's query to "foreign exchange limits". The tool returns "No
   matching policy". Update the scripted model so the researcher says it found nothing. Then decide what the writer
   should do. The right answer is to flag the gap, not to invent a rule.

5. **Bound the loop.** Set the researcher's `max_iter=1` and make the scripted model always return an Action. See how
   CrewAI forces a final answer when the limit is reached, and read what it produces.

6. **Use a real model (optional).** Set the `FDE_LLM_*` variables and run. Compare the note's quality and check the
   policy IDs against `common.py`, because real models sometimes "improve" a rule while paraphrasing it.

## Check yourself

<details><summary>Why split the work into two agents instead of one prompt?</summary>
Each role gets a focused prompt and tools: the researcher only searches and reports with IDs, and the writer only
writes from evidence. You can check the research separately, reuse it for other outputs, and see where an error entered.
</details>

<details><summary>What does context=[research] actually do?</summary>
It inserts the research task's final output into the writer's task prompt, so the writer works from the researcher's
findings rather than from its own assumptions.
</details>

<details><summary>How do you know the tool ran, rather than the model imagining a result?</summary>
Log inside the tool (the lab's trace line), or inspect the task's tool-usage records. Never infer tool use from a
plausible-looking answer.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| Plausible answer, but the tool never ran | The model skipped the action (or a scripted condition was wrong) | Log inside tools and assert they ran |
| The writer invents policy details | The brief task has no `context` | Pass the research task in `context` |
| Network calls on start-up | CrewAI telemetry | Set `CREWAI_DISABLE_TELEMETRY=true` and `OTEL_SDK_DISABLED=true` |
| `Invalid Format: I missed the 'Action:' after 'Thought:'` | The model's reply doesn't follow the format | Use a model that follows instructions well, or native function calling with a supported provider |

## Take it further

- Switch to `Process.hierarchical` with a manager agent, and compare the number of model calls and the predictability.
- Give the writer a `review` step (a third task) that checks the note against the expected output before it's final.
- Add a CrewAI Flow that runs the crew every fortnight and saves each note with its date.

## In a real client project

- Treat backstories and expected outputs as versioned prompts, reviewed like code.
- Validate every deliverable against its expected output, and keep the researcher's evidence with the final note.
- Disable or route telemetry deliberately; client data must not leave the agreed environment.
