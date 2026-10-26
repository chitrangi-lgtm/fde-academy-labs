# Self-study guide: A circuit breaker that survives the chaos drill

When a dependency struggles, clients that keep calling it make the outage worse and wait on timeouts. A circuit breaker turns that into fast, clear failures and gives the service room to recover. Chaos drills test exactly this, and a breaker you cannot test with a controlled clock is a breaker nobody trusts.

## Revise first (in the course)

- backoff with jitter and the three-state circuit breaker
- chaos engineering: breaking things on purpose, safely
- a deterministic chaos drill with retries and a breaker

## Read the email like an FDE

The site reliability lead describes a three-state machine in plain words. Closed: calls go through and failures in a row are counted. Open: after three failures in a row, stop calling for 30 seconds and fail fast. Half open: after the timeout, let one trial call through; success goes back to normal, failure waits another 30 seconds. 'In a row' means a success resets the count. 'Take the time from the clock you're given' means you must never read the real time.

## Questions to ask the client first

- **Which errors should count as failures: timeouts only, or also 4xx responses?** Counting a client's own bad requests can open the breaker for everyone.
- **What should users see while the breaker is open?** A friendly fallback answer is better than an error page.
- **Is there one breaker for the whole service or one per operation?** One slow endpoint should not block healthy ones.

## How each criterion is checked

1. **Successful calls pass straight through:** A successful call must return the function's result unchanged.
2. **Three failures in a row open the breaker:** Three failures in a row must move the breaker to open.
3. **While open, calls fail fast without touching the service:** While open, a call must raise CircuitOpen without calling the function at all.
4. **A success resets the failure count:** A success in between failures must reset the count, so the breaker stays closed.
5. **After the timeout one trial call is let through and a success closes it:** After the timeout on the fake clock, one trial call must go through, and its success must close the breaker.
6. **A failed trial reopens it for another full timeout:** A failed trial must reopen the breaker for another full timeout.

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
| The drill test waits 30 real seconds | time.time() was used instead of the clock passed in. | Read the time only through the injected clock. |
| The open breaker still calls the service | The state check came after the call. | Check the state before calling the function. |
| A failed trial waits less than 30 seconds | The open time was not updated on reopening. | Record the time again when the breaker reopens. |
| Errors are swallowed | The exception was caught and not re-raised. | Count the failure, then raise it again for the caller. |

## Test yourself before you check

- Write the sequence on paper: fail, fail, fail, call while open, tick 30, trial succeeds; what is the state after each step?
- Use the FakeClock and tick less than the timeout, then exactly the timeout.
- Count how many times the service function was actually called while open.
- Alternate success and failure and check the breaker never opens.

## What a senior reviewer also looks for

A reviewer would check that state changes happen in one place, that the breaker exposes its state for dashboards, and that CircuitOpen is a distinct error the caller can turn into a fallback. They would also ask whether the breaker is safe when several requests arrive at once.

## Stretch goal

Record every state change with the clock's time, so the drill report can show when the breaker opened, how long it stayed open and when it recovered.
