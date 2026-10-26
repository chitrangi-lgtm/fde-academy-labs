# Make the approval workflow survive a restart

**From:** Ivan Petrov, Automation Lead, Calder Facilities

Our purchase-approval agent drafts a request, waits for a manager, then sends the order. When the server restarted last week, it re-drafted everything and one supplier got the same order twice. I need the workflow to checkpoint its state to a file after every step, pick up exactly where it left off, wait for an 'approve' or 'reject' event, and never send an order twice, no matter how often it's called.

## Done when

- `run(state_path, event=None)` returns the workflow's status: "waiting_for_approval", "sent" or "rejected"
- State is saved as JSON at state_path after every step, with "step", "drafts" and "sent" counts
- Calling run again resumes from the file: it never drafts or sends twice
- An 'approve' event while waiting sends the order once; 'reject' ends the workflow without sending
- Events that arrive in the wrong state are ignored

## Files

none

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m15
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module m15) records your score.
