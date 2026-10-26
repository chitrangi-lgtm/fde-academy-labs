# Lab 05: Evaluations as unit tests that fail the build

**Time:** 45 minutes · **Level:** Intermediate · **Builds on:** Professional Practice P1 and P8, FDE Module 18 (evaluation), Agentic Module 10 (evaluating agents)

## The problem

CrestFin's policy assistant once told a borrower that late small-business instalments attract 3% interest a month. The policy says
2%. Nobody noticed until a complaint arrived, because the team only tested the assistant by hand before releases. The
head of engineering now wants answers checked automatically on every change, so a build with a wrong rate or limit can't
be merged.

This lab writes evaluations as ordinary pytest tests with **DeepEval**, an open-source evaluation library. One metric is
deterministic and runs anywhere; the other uses a model as a judge and runs only when a judge model is configured.

## What you'll learn

- How DeepEval represents a test case: the input, the actual output and the retrieved context.
- How to write a custom deterministic metric by subclassing `BaseMetric`.
- How `assert_test` turns a metric into a pass or fail that pytest, and therefore CI, understands.
- When to use a model-judged metric such as `FaithfulnessMetric`, and what it needs to be trustworthy.

## Before you start

1. From `realtools/`: `docker compose up -d --build`.
2. Run `docker compose exec labs python -m pytest -q 05_deepeval_tests.py`.
3. Without Docker: install the requirements in a virtual environment, `cd labs`, and run the same pytest command.

DeepEval's telemetry is switched off in the labs container (`DEEPEVAL_TELEMETRY_OPT_OUT=YES`). The model-judged tests are
skipped unless `OPENAI_API_KEY` is set, because DeepEval's default judge is an OpenAI model.

## Key ideas

**An evaluation is a test.** Each `LLMTestCase` holds a question, the assistant's answer and the context it retrieved.
`assert_test(case, [metric])` measures the case and raises an assertion error if the metric fails, exactly like any other
failing unit test. CI blocks the merge.

**Deterministic checks catch the expensive errors.** `NumbersGroundedMetric` extracts every number from the answer and
checks that each appears in the retrieved context. An invented rate or limit has no source, so the score drops below 1.0
and the test fails. It's cheap, fast and gives the same result every time.

**Model judges cover what rules can't.** `FaithfulnessMetric` asks a judge model whether each claim in the answer is
supported by the context. It catches unsupported statements that contain no numbers, but it costs money, varies slightly
between runs and must be checked against human labels before you trust its threshold.

**Thresholds are decisions.** The numbers metric requires 1.0 (every number grounded); faithfulness uses 0.8. Choose
thresholds from data on your own cases, and write down why.

## Steps

1. **Run the tests.** Expected result: `2 passed, 2 skipped`. The two numbers tests pass; the two faithfulness tests are
   skipped with the reason `LLM-judged metric needs a judge model key`.

2. **Break the build.** Change the late-payment answer to `"Late small-business instalments attract 3% interest per month."` and run
   again. Now one test fails with `AssertionError: Metrics: Numbers grounded (score: 0.0, threshold: 1.0, ...
   reason: 0/1 numbers grounded) failed.` The answer contains one number, 3, and the policy text doesn't. In CI, this
   red test is what stops the wrong rate reaching borrowers. Put the answer back.

3. **Read the metric.** In `measure`, follow how the numbers are extracted with a regular expression, how they're
   compared with the context, and how `score`, `success` and `reason` are set. Think of an answer that would wrongly pass,
   such as one that quotes the right number with the wrong unit.

4. **Add a case.** Add a test case for the gold-loan LTV with the answer `"Gold loans are capped at 75% of the gold value,
   for up to 12 months."` and the policy as context. Predict the result before running: 12 has no source, so it fails.

5. **Add a second deterministic metric.** Write `MustCitePolicyMetric`, which passes only if the answer contains a policy
   id such as `POL-7.1`. Update the answers to cite their policy and make all cases pass.

6. **Run the judge (optional).** If you have an OpenAI key, export `OPENAI_API_KEY` and run again. The faithfulness tests
   now run. Change an answer to add an unsupported claim without numbers, such as "no collateral is needed", and see
   whether the judge catches it.

## Check yourself

<details><summary>Why start with a deterministic metric rather than a model judge?</summary>
It's free, fast and repeatable, so it can run on every commit. Wrong numbers are among the most damaging errors in
financial assistants, and a simple rule catches them reliably.
</details>

<details><summary>What does a model judge need before you rely on it in CI?</summary>
A pinned judge model and prompt, a set of cases labelled by people, and evidence that the judge agrees with those labels
well enough at your chosen threshold. Recheck that agreement when you change the judge.
</details>

<details><summary>Why are the model-judged tests skipped rather than failed without a key?</summary>
A missing key is an environment issue, not a quality problem. Skipping keeps local runs and forks working; in the main
CI pipeline you'd make sure the key is present so they always run.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: deepeval` | Running outside the container or the virtual environment | Use `docker compose exec labs ...` or activate the environment |
| The faithfulness tests are always skipped | `OPENAI_API_KEY` isn't set in the environment pytest runs in | Pass it with `docker compose exec -e OPENAI_API_KEY=... labs ...` |
| A correct answer fails the numbers metric | The answer formats a number differently from the context (for example 75 percent and 75%) | Normalise numbers in the metric, or keep formats consistent |
| Evaluation results change between runs | A model judge at non-zero temperature | Pin the judge model and use temperature 0 where the provider allows |

## Take it further

- Load the test cases from a JSON file of real questions and answers produced by your assistant.
- Report scores per case to a file and fail the build only if the overall pass rate drops below the last release.
- Add a latency budget test that fails if any answer took more than 3 seconds to generate.

## In a real client project

- Build the evaluation set from real, anonymised questions, reviewed by the client's subject experts.
- Run the evaluations on every change to prompts, models, retrieval settings and tools, not just code.
- Keep the results of each release so you can show auditors how quality was checked.
