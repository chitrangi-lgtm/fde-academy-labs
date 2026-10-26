# Give the assistant a memory that fits its budget

**From:** Dr. Sofia Lindqvist, Product Director, Vireo Health Navigator

Long conversations with our assistant blow through the context window, and a privacy review found phone numbers and emails stored in its memory. I want a memory with a word budget: when it overflows, the oldest messages are folded into one short summary line, facts we pin (like the patient's allergy) are never dropped, the newest message always stays, and contact details are masked before anything is stored.

## Done when

- `Memory(budget)` with `add(role, text, pinned=False)` and `context()` returning [(role, text)] in order
- Text is stored with emails replaced by [EMAIL] and runs of 7 or more digits (spaces and dashes allowed inside) by [NUMBER]
- Size is the number of words; the summary line does not count. While the total is over budget, the oldest message that is neither pinned nor the newest is removed
- Removed messages are counted in one summary line at the start: ("system", "Summary: N earlier messages removed"), N growing as more are removed

## Files

none

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py ag04
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
