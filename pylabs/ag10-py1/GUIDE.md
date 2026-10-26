# Self-study guide: Is the new prompt really better? A paired significance test

The team ran the same 60 evaluation tasks with the old and the new agent prompt: 41 passes became 50, and product wants to ship. eval_runs.csv has one row per task with a 1 or 0 for each prompt. Because both prompts ran on the same tasks, the right test is paired (McNemar's exact test). You compute it, compare it with an unpaired test, and make the call at the 5 percent level.

## Revise first (in the course)

- statistics for agent evaluations
- just enough statistics to trust a comparison
- reliability statistics

## Questions to ask the client first

- **Were the 60 tasks fixed before the new prompt was written?** Tasks chosen after seeing the results can make any change look good.
- **How variable is a single run of the same prompt on the same task?** If one prompt passes and fails the same task on different runs, one run each is not enough.
- **What does a failed task cost compared with a passed one?** Significance says the change is real; the business case says whether it matters.

## Ideas you will use

- **Paired data:** Both prompts ran on the same tasks, so each task gives a pair of results. Tasks both prompts pass or both fail say nothing about which is better; only the tasks where they disagree do.
- **Discordant pairs:** b counts tasks the new prompt fixed (old failed, new passed); c counts tasks it broke (old passed, new failed). If the prompts were equally good, b and c would be similar.
- **McNemar's exact test:** Under 'no difference', each disagreement is a coin flip. A two-sided binomial test of c successes in b + c trials with probability 0.5 gives the exact p-value.
- **Why the unpaired test is weaker:** Fisher's exact test on the totals ignores which task is which, so the noise from easy and hard tasks hides the difference.

## Steps, check by check

1. **The discordant pairs are counted:** Count b (old failed, new passed) and c (old passed, new failed).
2. **McNemar's exact p-value is right:** Compute McNemar's exact p-value as a two-sided binomial test of c in b + c trials.
3. **The paired test is the sharper one here:** Compute Fisher's exact test on the two prompts' pass and fail totals and see that it gives a larger p-value.
4. **The call is made at the 5 percent level:** Decide 'ship' if the paired p-value is below 0.05, otherwise 'hold'.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If b and c are wrong, print the rows where the two columns differ and count them. If the paired p-value differs, check you passed c, b + c and 0.5 in that order. If the unpaired test is not larger, check the table rows are [passes, fails] for each prompt.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| b and c are swapped | The conditions were mixed up. | b is 'old failed and new passed'; c is the reverse. |
| The p-value is tiny | All 60 tasks were used as trials. | Use only the b + c disagreements as trials. |
| Fisher's test errors | The table was built from proportions. | Use counts of passes and fails. |
| decision is 'Ship' | The text was capitalised. | Use exactly 'ship' or 'hold'. |
| A one-sided p-value is used | The test only asked whether the new prompt is better. | Use the two-sided test, which also allows for the new prompt being worse. |

## What the result means for the client

Twelve tasks improved and three got worse; if the prompts were equally good, a split that uneven would be rare, so the improvement is real at the 5 percent level. The unpaired test would have said 'not significant' and held back a genuine improvement. Tell product to ship, and to keep the 60 tasks as the regression set for the next change.

## What to send the client

A note to product with the 2 by 2 table of agreements and disagreements, both p-values, the decision, and the three tasks the new prompt broke, so someone checks them before release.

## Stretch goal

Simulate a second run of both prompts by flipping each result with a small probability and see how often the decision changes, to show product how fragile a single run can be.
