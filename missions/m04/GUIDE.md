# Self-study guide: Why did the integration create duplicate orders?

'The integration created duplicates and nobody knows why' is one of the most common calls an FDE gets. The answer is almost always in the API log: retries of requests that were not safe to repeat. Reading a log into numbers, then turning the numbers into a policy the partner can implement, is everyday integration work.

## Revise first (in the course)

- HTTP methods, status codes and which failures are temporary
- classifying status codes into retry or fail fast
- a retry policy engine with backoff

## Read the email like an FDE

The manager asks for three things and one policy. 'One JSON object per line' tells you how to load the file: line by line, not as one document. 'The error rate for each kind of call' needs a grouping you must define: the method plus the resource, without the order id at the end of the path. 'Which orders were created more than once' points at successful creates (status 201) and the clue is the idempotency key: a replay with the same key is safe by design. The policy part gives you exact rules: which statuses to retry, Retry-After wins when present, otherwise exponential backoff from half a second, capped at eight.

## Questions to ask the client first

- **Which partner endpoints already accept an idempotency key?** The retry policy is only safe for creates that can be replayed without harm.
- **How many retries in total may the partner make before giving up?** Backoff without a cap on attempts can turn an outage into a flood.
- **Should errors be measured per day or per deployment?** Rates over the wrong window hide the night the duplicates happened.

## How each criterion is checked

1. **The log loads:** load must return all 11 records from the log as dictionaries.
2. **Error rates per kind of call:** error_rates must return the share of 5xx responses for each method and first path segment, rounded to three places, for exactly the three kinds of call in the log.
3. **The duplicated order is found, and keyed replays are not blamed:** duplicate_creates must return only the order created twice without an idempotency key. Orders replayed with the same key must not be listed.
4. **Only transient failures are retryable:** retryable is called with seven statuses and must say yes only to the temporary ones from the list in the acceptance criteria.
5. **Backoff grows and is capped:** backoff is called for attempts 0, 3 and 10 and must grow from half a second and stop at eight.
6. **The server's Retry-After wins:** backoff with a Retry-After value must return that value unchanged.

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
| Each order id becomes its own kind of call | The whole path was used as the key. | Keep only the first segment after the leading slash. |
| A keyed replay is reported as a duplicate | Every 201 was counted. | Count only creates without an idempotency key. |
| backoff(1, retry_after=0) waits a full second | A truthiness test treated 0 as 'not given'. | Compare retry_after with None. |
| Rates come out as 0 or 1 | Integer counts were compared or divided in the wrong place. | Count errors and calls separately and divide once per kind. |

## Test yourself before you check

- Print the records for one order reference and read the story: which request was retried, and was it keyed?
- Print your counts per kind of call before dividing, and check one by hand.
- Print backoff for attempts 0 to 6 and look for the cap.
- Try retryable with 400 and 404: a client error will never succeed on retry.

## What a senior reviewer also looks for

A reviewer would expect the retry policy to be data (a named set of statuses and named constants for the base delay and cap) so the partner can read it in a document. They would also ask for a sentence in the report recommending idempotency keys on every create, because the code finds the problem but the key is what prevents it.

## Stretch goal

Add jitter to the backoff so many clients do not retry at the same instant, and write a one-paragraph incident note for the partner explaining the duplicate and the fix.
