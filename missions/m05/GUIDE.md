# Self-study guide: Twelve supplier quotes, fast and polite

Every quote, search or comparison page in an enterprise fans out to many slow systems. Done one by one it is slow; done all at once it overloads partners who have contracts limiting how hard you may call them. Fast, bounded and fault-tolerant fan-out is a pattern you will build again in agents that call many tools.

## Revise first (in the course)

- I/O-bound work and asyncio.gather
- semaphores and other ways to limit concurrency
- timeouts and cancellation

## Read the email like an FDE

Read the constraints as a contract. 'As fast as possible' means calls must overlap. 'Never more than four requests open at once' is a hard limit agreed with suppliers, so it will be measured. 'Gives up on a supplier after 0.2 seconds' means a per-call timeout, not one for the whole page. 'Still returns the other quotes in the order we asked' means one slow supplier must not fail the rest, and the output order follows the input order, not the order answers arrive. The provided fetch_quote counts how many calls are open, so the checks can see your concurrency.

## Questions to ask the client first

- **What should the page show for a supplier that timed out?** Product and design need to know whether to hide it, grey it out or offer a retry.
- **Is the four-request limit per supplier or across all suppliers?** The two readings need different limiters, and the contract decides which one.
- **Can a late quote still be used if it arrives after the page is shown?** That changes whether timed-out calls are cancelled or left to finish.

## How each criterion is checked

1. **Every supplier answers, in the order asked:** gather_quotes is run for twelve suppliers and must return one result per supplier in the order given.
2. **Prices come through:** Prices from the quick suppliers must come through unchanged.
3. **The two slow suppliers are timed out, not waited for:** The two slow suppliers must be returned as timeouts, with every other supplier still answered.
4. **Never more than four calls at once:** The peak number of calls open at once, measured by fetch_quote, must never exceed four.
5. **Calls really do overlap:** The same peak must be at least two, which proves calls really overlap.
6. **It finishes well under the sequential time:** The whole call must finish in well under the time of calling the suppliers one after another.

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
| It takes several seconds | The suppliers were awaited one after another in a loop. | Create all the calls first and gather them together. |
| The peak goes above four | The limiter was created inside the per-supplier coroutine, so each has its own. | Create one limiter outside and share it. |
| One slow supplier fails the whole call | The timeout exception escaped from gather. | Catch the timeout inside the per-supplier coroutine and return an error result. |
| The order is wrong | Results were collected as they finished. | Let gather return them; it keeps the order of the calls you passed in. |

## Test yourself before you check

- Time your function with time.perf_counter and compare it with 12 calls one by one.
- Print the provided peak counter after your run.
- Change the limit to 2 and to 12 and watch the time and the peak change.
- Make a third supplier slow and check it times out too.

## What a senior reviewer also looks for

A reviewer would check that the limit and timeout come from the arguments, not constants, that the timeout wraps only the supplier call (not the wait for a slot), and that the error result has the same shape every time so the quote page can show it. They would also ask what is logged when a supplier times out, because the supplier relationship team will want numbers.

## Stretch goal

Add one retry for a timed-out supplier when time allows, and return how long each supplier took so the page can show the slowest ones to the procurement team.
