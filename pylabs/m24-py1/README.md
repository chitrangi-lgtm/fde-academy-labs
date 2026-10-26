# A sensitivity chart for the steering committee

**Libraries:** pandas, matplotlib · **Level:** Intermediate · about 30 minutes

The steering committee will ask 'what if the benefits are 20 percent lower?' before it signs. Build the NPV for the claims assistant (420,000 dollars a year of benefit, 600,000 up front, 80,000 a year to run, three years, 10 percent discount rate), swing each driver by 20 percent either way, and draw a tornado chart.

Write your code in `lab.py`, then run `python tools/fde_check.py m24-py1` from the kit's folder.

<details><summary>Hints</summary>

1. `sum((benefit - run) / (1 + rate) ** t for t in range(1, years + 1)) - upfront`.
2. For each driver, copy `base`, multiply that one value by 0.8 and by 1.2, and compute both NPVs.
3. Tornado: `plt.barh(driver, high - low, left=low)` for each driver, largest swing at the top.
</details>

## Why it matters

Executives decide on ranges, not point estimates. A tornado chart shows which assumption the decision really rests on, so the committee spends its questions on the benefit case.
