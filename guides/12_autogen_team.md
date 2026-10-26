# Lab 12: A writer and a compliance reviewer in a Microsoft AutoGen team

**Time:** 45–60 minutes · **Level:** Intermediate · **Builds on:** Agentic Module 7 (multi-agent coordination), Module 9 (safety), FDE Module 16 (security and compliance)

## The problem

Albion Mutual sends thousands of letters a month about delayed health claims. The insurance regulator expects fair treatment, so the compliance team bans certain phrases. "We guarantee payment"
is one, because the insurer can't guarantee it. The client wants drafts produced by one agent, checked by another with a
deterministic tool, and revised until they pass. The loop needs a hard stop so it can't run up costs.

**AutoGen** is Microsoft's framework for multi-agent applications. Its AgentChat layer gives you agents and teams with
termination conditions, which is exactly the coordination problem from Agentic Module 7. Microsoft now points new projects
to Microsoft Agent Framework, the successor to AutoGen and Semantic Kernel, and keeps AutoGen in maintenance; the team, the
termination condition and the hard stop you build here carry over directly.

## What you'll learn

- How an `AssistantAgent` works with and without tools, and what `reflect_on_tool_use` changes.
- How a `RoundRobinGroupChat` passes the conversation between agents in turn.
- How termination conditions combine (`TextMentionTermination("APPROVED") | MaxMessageTermination(8)`), and why every
  multi-agent loop needs a budget.
- How `ReplayChatCompletionClient` makes a multi-agent protocol testable without a model.

## Before you start

Run `docker compose exec labs python 12_autogen_team.py`, or run it in a local virtual environment with
`requirements.txt` installed. Offline, both agents are played by replay clients. Set the `FDE_LLM_*` variables to use a
real OpenAI-compatible model for both.

## Key ideas

**Separation of duties.** The writer never checks its own work. The reviewer has the `check_wording` tool and the
authority to say APPROVED. That mirrors maker-checker controls in banks and insurers, and it is a direct defence
against a single model talking itself into a bad answer.

**Deterministic checks beat model opinions.** The banned-phrase check is a Python function, not a prompt. The reviewer
model calls it, then explains the result. With `reflect_on_tool_use=True`, the agent makes a second model call after the
tool to turn the raw result into a message. Without it, the tool result itself becomes the message.

**Teams and turns.** `RoundRobinGroupChat([writer, reviewer])` gives each agent the whole conversation in turn. Other team
types choose the next speaker with a model (`SelectorGroupChat`) or by handoffs (`Swarm`). Round-robin is the easiest
to predict and to test.

**Termination is your budget.** The team stops at the first message containing "APPROVED", or after eight messages,
whichever comes first. Without the cap, a reviewer that never approves would loop for ever. `result.stop_reason` tells
you which condition fired, so you log it and route timeouts to a person.

**Replays make protocols testable.** `ReplayChatCompletionClient` returns a fixed sequence of responses, including tool
calls built as `CreateResult` objects with `FunctionCall` content. The lab's script makes the first draft fail the
check, so you see the full revise-and-approve cycle every time.

## Steps

1. **Run the lab.** Expect this sequence:
   - the task;
   - draft 1, which contains "guarantee";
   - the reviewer's tool call and its result: `{"ok": false, "banned_phrases": ["guarantee"]}`;
   - "CHANGES REQUESTED";
   - draft 2;
   - a second tool call, this time with `ok: true`;
   - "APPROVED".

   The last line reports the stop reason: the APPROVED mention.

2. **Count the model calls.** The writer makes two and the reviewer four (a tool call and a reflection per review). With
   a real model, estimate the cost: messages × average tokens × price. Then change `reflect_on_tool_use` to `False`,
   adjust the reviewer's replay script to drop the reflection replies, and compare.

3. **Make the reviewer never approve.** Replace the reviewer's last reply with another "CHANGES REQUESTED" and add more
   writer drafts. The team stops after eight messages. Check `result.stop_reason`, and decide what the application does
   next: send the case to a person.

4. **Strengthen the check.** Add a rule to `check_wording` that every letter must give a next step: it must contain
   "we will" or "you can". Re-run and adjust the drafts so the second one passes both rules.

5. **Add a third agent (optional).** Add a `plain_english` agent that rewrites the approved letter at a reading age of
   about 12. Add it to the team after the reviewer, then ask yourself whether its output needs another review.

6. **Use a real model (optional).** Set the `FDE_LLM_*` variables. Real models may approve without calling the tool.
   Fix that the robust way: require a successful `check_wording` result in the conversation before any APPROVED message
   counts. One way is a custom termination condition that inspects the tool result events.

## Check yourself

<details><summary>Why does the reviewer use a Python tool instead of just reading the letter?</summary>
A banned-phrase rule is deterministic and must hold every time; a model's reading can miss it. The model's job is to
explain and suggest; the rule is enforced by code.
</details>

<details><summary>What happens if you remove MaxMessageTermination?</summary>
If the reviewer never says APPROVED, the team runs until something external stops it, which costs money and time.
Always pair a success condition with a budget condition.
</details>

<details><summary>Round-robin, selector or swarm: which suits this process, and why?</summary>
Round-robin, because the process is a fixed maker-checker cycle. A selector adds a model call to choose speakers and
makes the flow less predictable, which is only worth it when the right next agent genuinely varies.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `ValueError: The model does not support function calling` | The client's model info doesn't declare tool support | Pass `model_info` with `"function_calling": True` (needed for replay and non-OpenAI models) |
| The team stops immediately | The task or a draft contains the word APPROVED | Use a distinctive token, and make sure only the reviewer can produce it |
| `StopIteration` from the replay client | The script ran out of responses | Add a response for every model call, including reflections after tools |
| Approval without a check (real model) | The termination condition trusts text alone | Require a passing tool result before approval counts |

## Take it further

- Swap `RoundRobinGroupChat` for `SelectorGroupChat` and compare the transcripts and the number of model calls.
- Save and load the team's state (`team.save_state()` / `team.load_state()`) to resume a review after a restart.
- Write a pytest test that runs the team with the replay clients and asserts the stop reason and the final letter.

## In a real client project

- Keep compliance rules in code or configuration owned by the compliance team, with tests; models apply them, they don't
  define them.
- Log every draft, check result and approval with timestamps; regulators may ask how a letter was produced.
- Send any loop that hits the message cap to a person, and track how often it happens.
