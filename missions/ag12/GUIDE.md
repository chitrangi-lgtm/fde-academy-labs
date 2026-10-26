# Self-study guide: Canary, hold or roll back?

Releasing a new agent version to everyone at once turns any regression into an incident. Canary releases limit the damage, but only if the decision to promote, hold or roll back is consistent. Writing that decision as reviewed code makes releases boring in the best way: the same evidence always gives the same answer.

## Revise first (in the course)

- release management: flags, canaries and shadows
- a canary rollout with automatic rollback
- canary assignment and the rollout controller

## Read the email like an FDE

The platform owner orders the decisions by severity. Roll back first: errors clearly worse, or evaluation quality clearly worse, by the agreed thresholds. Only if neither applies, hold: too little traffic to judge, or latency worse by more than the agreed share. Otherwise promote to the next stage. The order matters: a quality regression rolls back even when traffic is thin. The criteria say the error threshold is absolute and the latency one is relative.

## Questions to ask the client first

- **Is the baseline measured over the same hours as the canary?** Traffic patterns differ by hour and can fake a regression.
- **Who is told when a rollback happens automatically?** Automatic rollbacks still need a person to investigate.
- **Can a person override a hold to meet a deadline?** Overrides need an owner and a written reason.

## How each criterion is checked

1. **A healthy canary is promoted:** A healthy canary must be promoted with no reasons.
2. **More errors means rollback:** A canary with a clearly higher error rate must be rolled back.
3. **Worse quality means rollback, even with little traffic:** A canary with clearly lower evaluation quality must be rolled back, even with little traffic.
4. **Too little traffic or slower responses mean hold:** A canary with too little traffic, or with slower responses, must be held.
5. **Reasons explain a decision:** A canary with two reasons to hold must report both.
6. **Rollout stages:** next_stage must step through 1, 5, 25, 50 and 100, staying at 100.

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
| A quality drop with thin traffic is held | Hold conditions were checked first. | Check rollback conditions before hold conditions. |
| Latency compares in milliseconds instead of percent | The relative threshold was used as an absolute one. | Compare with the baseline's p95 times one plus the allowed increase. |
| Division by zero with no traffic | The canary's error rate divided by zero requests. | Treat zero requests as no errors and let the traffic rule hold it. |
| next_stage(100) fails | No stage is above 100. | Return 100 when there is no next stage. |

## Test yourself before you check

- Work out both error rates for each test case by hand.
- Build a canary that should roll back and also has too little traffic, and check the decision.
- Print the reasons for each decision and read them as the on-call engineer would.
- Walk next_stage from 1 to 100.

## What a senior reviewer also looks for

A reviewer would check that thresholds come from the agreed file, that reasons include the numbers compared, and that every decision is recorded with its evidence so a rollback can be explained the next morning. They would also ask how long a canary may stay on hold before someone looks at it.

## Stretch goal

Require the hold or promote decision to be stable for two checks in a row before promoting, and record the decisions with timestamps for the release report.
