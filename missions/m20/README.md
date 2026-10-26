# Answer the security questionnaire from evidence

**From:** Hannah Whitfield, Vendor Risk Manager, Oriel Pensions

Before we sign, your assistant must pass our vendor security questionnaire. Your team keeps a register of implemented controls with evidence. I don't want answers from memory: generate each answer from the register, attach the evidence ids, mark a control that is only partly in place as Partial, and give me the list of gaps you'll close before go-live.

## Done when

- `answer(questionnaire, register)` returns {question id: {"answer": "Yes" | "Partial" | "No", "evidence": [evidence ids, sorted]}}
- Yes when every control the question needs is implemented; Partial when at least one is implemented or partial but not all are implemented; No when none is
- Evidence lists the evidence of every implemented or partial control the question needs
- `gaps(answers)` returns the sorted ids of questions answered Partial or No

## Files

`questionnaire.json`, `register.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m20
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module m20) records your score.
