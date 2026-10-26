# Is the new prompt really better? A paired significance test

**Libraries:** SciPy, pandas · **Level:** Advanced · about 35 minutes

The team ran the same 60 evaluation tasks with the old and the new agent prompt: 41 passes became 50. Product wants to ship. Because both prompts ran on the same tasks, the right test is paired (McNemar's exact test). Compute it, compare with an unpaired test, and make the call at the 5 percent level.

Write your code in `lab.py`, then run `python tools/fde_check.py ag10-py1` from the kit's folder. `GUIDE.md` has the ideas, the steps check by check and the common mistakes.

<details><summary>Hints</summary>

1. Only tasks where the prompts disagree carry information: `((runs.old_prompt_passed == 0) & (runs.new_prompt_passed == 1)).sum()`.
2. `binomtest(c, b + c, 0.5).pvalue` is the exact McNemar test.
3. `fisher_exact([[50, 10], [41, 19]]).pvalue` treats the two runs as unrelated samples.
</details>

## Why it matters

Agent evaluations usually compare two versions on the same tasks, so use a paired test. Here the paired test is significant while the unpaired one is not: the wrong test would have held back a real improvement.
