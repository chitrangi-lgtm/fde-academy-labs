# Self-study guide: The go-live gate

Go-live meetings go wrong when the decision is a debate. Service levels agreed before the project started, compared mechanically with this week's measurements, protect both sides: the team cannot be talked into a risky launch, and the client hears specific, measurable reasons. A gate like this is part of every mature release process, and writing it as code means the same rules apply at every future release, not only at the first one.

## Revise first (in the course)

- operational readiness and handover
- an operational readiness review with a weighted checklist
- measuring quality before deciding

## Read the email like an FDE

The service owner asks for a mechanical decision and readable reasons. Thresholds come in two kinds, minimums and maximums, and each is checked in its own direction. 'Block go-live for any breach or any open severity-1 or severity-2 issue' adds a second source of reasons. The criteria add a rule that is easy to miss: a metric that was not measured is a breach, not a pass. The reasons' wording is fixed so they can be read out at the meeting.

## Questions to ask the client first

- **Who signs the go-live decision, and can they override a NO-GO?** An override needs an owner and a written reason, or the gate means nothing.
- **Over what period is each metric measured?** A week's average can hide a bad day; the window should be agreed in advance.
- **What counts as closed for an issue: fixed, or fixed and verified?** Closing an issue on paper before it is verified defeats the gate.

## How each criterion is checked

1. **This week is a NO-GO, for the right reasons:** This week's data must give NO-GO with exactly three reasons: a latency breach, a missing measurement and an open severity-2 issue, worded as specified and sorted.
2. **A clean week is a GO:** A clean week must give GO with no reasons.
3. **Minimums are enforced:** A metric below its minimum must give the minimum reason in the exact wording.
4. **Sev3 and closed issues do not block:** Severity-3 issues and closed issues must not block.
5. **An open sev1 blocks:** An open severity-1 issue alone must give NO-GO with its reason.

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
| A missing metric passes | The loop went over the metrics. | Loop over the thresholds. |
| Wording does not match | The reason text was paraphrased. | Use the exact phrases from the criteria. |
| A closed severity-1 issue blocks | Status was not checked. | Only open issues block. |
| A metric equal to its maximum is a breach | The comparison included equality. | Breach means strictly above a maximum or strictly below a minimum. |

## Test yourself before you check

- Read golive.json and decide GO or NO-GO by hand, with reasons.
- Remove one measurement from a clean week and check the reason appears.
- Set a metric exactly on its threshold and confirm it passes.
- Read your reasons out loud: would the service owner understand them?

## What a senior reviewer also looks for

A reviewer would check that the gate cannot be satisfied by leaving data out, that the thresholds come from the agreed document rather than the code, and that the result is stored with the date and the measurements it used, so the decision can be audited later.

## Stretch goal

Add warnings for metrics within 5 percent of a threshold, reported separately from the blocking reasons, so the service owner knows what to watch after go-live.
