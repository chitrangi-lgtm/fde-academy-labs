# Fit the documents into the context budget

**From:** Sven Aaltonen, Search Lead, Quillon Legal Search

Our assistant sends whole documents to the model and keeps hitting the context limit. We want to count tokens the way our model's tokenizer does and send only the chunks that fit. The tokenizer is byte-pair encoding: attached are its merge rules in priority order. Please give me a tokenizer for single lower-case words, a token count for a sentence, and a packer that keeps chunks in their ranked order and skips any chunk that would overflow the budget, then keeps trying the rest.

## Done when

- `bpe(word, merges)` returns the tokens for a lower-case word: start from characters and repeatedly merge the adjacent pair with the best (earliest) rule until no rule applies
- `count_tokens(text, merges)` adds up the tokens of each whitespace-separated word
- `pack(chunks, budget, merges)` takes [(chunk_id, text)] in ranked order and returns the ids it keeps, skipping chunks that would exceed the budget

## Files

`merges.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m07
```

There are no steps: how you build it is up to you. If you are stuck, `NUDGES.md` has two hints. The course site's version of this challenge (Module m07) records your score.
