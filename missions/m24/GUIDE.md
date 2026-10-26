# Self-study guide: The numbers for the steering committee

Steering committees decide with numbers, and finance checks every one. Using finance's own conventions, and saying so, is what makes the committee trust the case; a different convention, even a reasonable one, starts an argument instead of a decision. NPV, payback and ROI answer different questions, and the committee's rule combines value and risk.

## Revise first (in the course)

- presenting ROI, TCO, payback and sensitivity
- what a steering committee decides
- an investment case: payback, NPV and ROI

## Read the email like an FDE

The COO fixes the conventions, and each one changes the numbers. NPV discounts each year's net benefit at the end of the year, with the upfront cost today and not discounted. Payback uses undiscounted cash and is interpolated within the year, assuming the cash arrives evenly. ROI is total net benefit over total cost, and the criteria give the exact formula. The committee's rule needs both conditions: positive NPV and payback within two years. A case that never pays back within the years must say so rather than invent a number.

## Questions to ask the client first

- **Which discount rate does finance use for projects like this one?** The rate is a finance policy; using your own invites the first objection.
- **Are benefits expected from day one, or after a ramp-up?** Adoption ramps delay benefits and move payback.
- **Should the case include the cost of the team's time inside the client?** Hidden internal costs are a common challenge from the CFO.

## How each criterion is checked

1. **NPV follows finance's convention:** business_case for the main scenario must give the NPV exactly as finance would calculate it.
2. **Payback is interpolated within the year:** The same case must give the payback in years, interpolated within the year and rounded.
3. **ROI is net benefit over total cost:** The same case must give the ROI from the formula in the criteria.
4. **A case that never pays back says so:** A case whose cash never covers the upfront cost within the years must return None for payback.
5. **The committee's rule:** recommendation must approve the main case and send a weaker four-year case back for revision.

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
| NPV is too low | The upfront cost was discounted too. | Only the yearly amounts are discounted. |
| Payback is a whole number | It counted whole years only. | Interpolate within the year the running total crosses zero. |
| recommendation crashes | None was compared with 2. | Check payback for None first. |
| Values differ by a cent | Rounding happened inside the loop. | Round only the final values. |

## Test yourself before you check

- Work the main case's payback by hand: how far into year 2 does the running total reach zero?
- Compute NPV with a spreadsheet-style table of years, discount factors and present values.
- Lower the benefit until payback becomes None and check the recommendation.
- Change the discount rate and confirm only NPV moves.

## What a senior reviewer also looks for

A reviewer from finance would look for the conventions stated next to the numbers, consistent rounding, and inputs kept separate from the formulas, so they can try their own assumptions. They would also ask for a sensitivity view, because the committee's first question is usually 'what if the benefit is lower?'

## Stretch goal

Add a sensitivity table showing NPV and payback when the benefit is 20 percent lower and the upfront cost 20 percent higher, and say in one sentence whether the recommendation survives.
