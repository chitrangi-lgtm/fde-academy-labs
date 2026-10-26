# Self-study guide: Find the retrieval regression and the trace leak

'The answers feel worse' is not something a team can fix; a measured drop in retrieval quality after a specific change is. Enterprises also find, often too late, that their tracing stores customer prompts where they should not. Evaluation on a fixed question set and a privacy scan of telemetry are two of the most valuable things an FDE adds to an AI platform.

## Revise first (in the course)

- measuring retrieval and answer quality
- tracing LLM systems with OpenTelemetry
- just enough statistics to trust a comparison

## Read the email like an FDE

The platform lead asks for numbers that prove or disprove a regression and for a privacy finding. Hit rate at 3 asks whether any correct document appears in the top three; mean reciprocal rank rewards finding it early. Both are computed before and after the rebuild so the drop is visible. The acceptance criteria define p95 as the nearest-rank percentile, which is not what a statistics library may give you by default. A leak is any span attribute whose key mentions prompt or completion.

## Questions to ask the client first

- **Was the question set and its gold documents the same for both runs?** A changed question set makes the comparison meaningless.
- **Which span attributes are allowed to contain user text, if any?** A clear allow-list is easier to enforce than a list of forbidden words.
- **How long are traces kept, and who can read them?** A leak's severity depends on retention and access.

## How each criterion is checked

1. **Hit rate at 3 before and after the rebuild:** hit_rate at 3 must show the drop from the run before the rebuild to the run after it.
2. **MRR before and after the rebuild:** mrr must give the expected values for both runs, rounded to three places.
3. **Hit rate respects k:** hit_rate with k=1 must only look at the first retrieved document.
4. **Nearest-rank p95:** p95 must follow the nearest-rank rule on a short list and on the numbers 1 to 100.
5. **p95 per span name:** p95_by_span must return the p95 duration for each span name.
6. **Prompt and completion leaks are found:** leaks must return the ids of the spans whose attribute keys mention prompt or completion, sorted.

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
| MRR is too high | Positions were counted from 0. | Count positions from 1. |
| p95 differs slightly | A library percentile with interpolation was used. | Use the nearest-rank rule from the criteria. |
| Hit rate ignores k | The whole retrieved list was searched. | Slice the first k documents before comparing. |
| A leak with a key like 'llm.Prompt' is missed | Keys were compared without lower-casing. | Lower-case each key before looking for the words. |

## Test yourself before you check

- Compute hit rate and MRR by hand for two questions from each run.
- Check p95 on ten numbers you can sort in your head.
- Print each span name with its sorted durations next to your p95.
- Read the attributes of the spans you flag and confirm they really hold text.

## What a senior reviewer also looks for

A reviewer would want the metrics reported side by side for both runs, with the number of questions, so nobody over-reads a change on a small set. They would also ask for the leak scan to run in CI on a sample of real traces and to fail loudly, because privacy findings found by the client are much worse than ones found by the team.

## Stretch goal

Add recall at 5 and the list of questions that regressed (found before, missed after), so the team can read the failing cases instead of only the averages.
