# The go-live gate

**From:** Deborah Okonkwo, Service Owner, Selwyn City Council

We agreed service levels for the residents' assistant before the project started. Tomorrow's go-live decision must be mechanical, not a debate: compare this week's measurements with each threshold (some are minimums, some maximums), and block go-live for any breach or any open severity-1 or severity-2 issue. I want the reasons in plain words so I can read them out at the meeting.

## Done when

- `gate(metrics, thresholds, issues)` returns {"decision": "GO" or "NO-GO", "reasons": sorted list}
- A threshold {"min": x} is breached when the metric is below x; {"max": y} when it is above y; a missing metric is a breach
- Reasons read "<metric> is <value>, below the minimum of <x>", "... above the maximum of <y>", "<metric> was not measured", or "open sev1 issue <id>" / "open sev2 issue <id>"
- Closed issues and sev3 issues do not block

## Files

`golive.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m21
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
