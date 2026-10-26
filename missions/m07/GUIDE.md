# Self-study guide: Fit the documents into the context budget

Context windows are a budget, and every token costs money and latency. Teams that estimate tokens by words or characters overflow the limit in production or waste half of it. Counting the way the model's own tokenizer does, and filling the window with the best evidence first, is basic hygiene for any retrieval-based assistant.

## Revise first (in the course)

- how byte-pair encoding merges characters into tokens
- watching BPE merges step by step
- training merges and encoding new words

## Read the email like an FDE

The search lead describes an algorithm and a policy. 'Merge rules in priority order' means the position of a rule in the list is its rank: earlier rules win. 'Single lower-case words' limits what bpe must handle, and count_tokens is simply the words added up. The packer's policy is in the last sentence: keep the chunks in their ranked order, skip one that would overflow, and keep trying the rest, so a large chunk early on must not stop smaller ones later from fitting.

## Questions to ask the client first

- **Does the budget have to leave room for the question and the answer?** Packing the whole context window with evidence leaves the model no space to reply.
- **Is it better to cut a long chunk than to skip it?** Trimming keeps some of the best evidence, at the risk of losing the key sentence.
- **Will the tokenizer's rules change when the model is upgraded?** Counts tied to one tokenizer must be re-checked on every model change.

## How each criterion is checked

1. **A fully mergeable word is one token:** A word that every rule can merge must come back as one token.
2. **Merges follow rule priority:** A word where two rules compete must follow rule priority, producing the tokens the earliest rules create.
3. **Unmergeable letters stay single:** Letters that no rule joins must stay as single characters, including a word with no rules at all.
4. **A sentence's tokens add up:** count_tokens on a three-word sentence must equal the tokens of each word added up.
5. **The packer skips a chunk that overflows and keeps trying:** pack with a budget of 6 must keep the first chunk, skip the second because it would overflow, and still keep the third.
6. **Nothing fits a zero budget:** pack with a budget of 0 must keep nothing.

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
| 'newest' comes out as different tokens | Rules were applied in the order pairs appear in the word. | Pick the pair with the best rank across the whole word at each step. |
| The loop never ends | A merged pair was not replaced, so the same pair is found again. | Replace the two tokens with their joined token before looking again. |
| pack stops after the first chunk that does not fit | The loop breaks on overflow. | Skip that chunk and continue with the next one. |
| Single letters disappear | Characters without a rule were dropped. | Keep every token; merging only joins neighbours. |

## Test yourself before you check

- Print the token list after each merge for 'newest' and compare with the rule order.
- Count the tokens of the packer's chunks by hand before running pack.
- Try a budget exactly equal to the first chunk's tokens: it should still be kept.
- Try an empty text and a word of one letter.

## What a senior reviewer also looks for

A reviewer would check that the rank lookup is built once rather than searched on every step, that the packer reports how much of the budget it used, and that the code says what happens with characters the tokenizer has never seen. They would also ask for one test per rule of the email.

## Stretch goal

Make the packer reserve part of the budget for the question and the answer, and return the token count it used, so the assistant can log how full each request was.
