# Nudges (open only if stuck)

1. Loop over the thresholds (not the metrics), so a missing measurement is noticed.

2. Collect every reason first; the decision is simply NO-GO when the list is not empty.

## The approach, in plain English (open last)

1. Loop over the thresholds, not the metrics, so a missing measurement is noticed.
2. For each threshold, add a 'not measured', 'below the minimum' or 'above the maximum' reason as it applies.
3. Loop over the issues and add a reason for each open severity-1 or severity-2 issue.
4. The decision is NO-GO when there is any reason, and the reasons are returned sorted.
