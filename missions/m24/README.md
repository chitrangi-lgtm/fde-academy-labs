# The numbers for the steering committee

**From:** Jonathan Pryce, Chief Operating Officer, Albion Claims (capstone client)

On Thursday the steering committee decides whether to roll the claims-status assistant out to every region. Finance will check your numbers, so use their conventions: NPV at the given discount rate with costs and benefits at the end of each year and the upfront cost today; payback in years from undiscounted cash, interpolated within the year; ROI as total net benefit over total cost. The committee's rule: approve if NPV is positive and payback is within two years, otherwise send it back for revision.

## Done when

- `business_case(benefit, upfront, run, years, rate)` returns {"npv", "payback_years", "roi"}: npv and roi rounded to 2, payback rounded to 2 (None if never paid back within the years)
- NPV = -upfront + sum over years of (benefit - run) / (1 + rate) ** year
- Payback: the point where cumulative undiscounted cash (starting at -upfront) reaches zero, assuming even cash within each year
- ROI = (years x (benefit - run) - upfront) / (upfront + years x run)
- `recommendation(case)` returns "approve" or "revise" by the committee's rule

## Files

none

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m24
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module m24) records your score.
