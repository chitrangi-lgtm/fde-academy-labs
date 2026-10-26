# Self-study guide: Find the cost spike and the slow step

Agent platforms make many model calls per user request, so bills and latency can change suddenly with one feature's behaviour. Finance asks why the bill jumped; customers complain the assistant is slow. Tagging every call with its feature and step, and summarising cost, cache use and latency, answers both questions with evidence, and often shows that one oversized step is behind both problems at once.

## Revise first (in the course)

- where agent cost comes from
- prompt caching and context engineering for cost
- latency engineering

## Read the email like an FDE

The delivery manager has two complaints and four questions. Cost by feature and the spike: total cost per feature, then the day with the highest cost and the feature behind it on that day. The cache question is a share of input tokens, not of calls. The latency question asks for p95 per step, and the criteria define the nearest-rank method. The cost formula is given exactly, with cached input billed at its own price and prices per million tokens.

## Questions to ask the client first

- **Which days are business days for the bill comparison?** Weekends and promotions change normal traffic.
- **Is the p95 measured per model call or per user request?** A user waits for the whole request, not one call.
- **Should the cost spike raise an alert next time?** Daily cost per feature makes a simple, useful alert.

## How each criterion is checked

1. **One call's cost:** cost for one recorded call must match the formula exactly.
2. **Cost by feature:** report must give the total cost per feature, rounded to cents.
3. **The spike day and its cause:** report must find the day the bill spiked and the feature behind it.
4. **Cache hit rate:** report must give the share of input tokens served from cache, rounded to three places.
5. **p95 latency per step:** report must give the nearest-rank p95 latency for each step.

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
| Cost is far too high | Cached tokens were billed twice, as input and as cached. | Bill input minus cached at the input price, and cached at the cached price. |
| The spike feature is the biggest overall | The feature was chosen across all days. | Choose the biggest feature on the spike day only. |
| The cache rate is a share of calls | Calls with any cache hit were counted. | Divide cached tokens by input tokens. |
| p95 differs slightly | An interpolating percentile was used. | Use the nearest-rank rule. |

## Test yourself before you check

- Compute one call's cost by hand and compare.
- Print cost per day and look for the jump yourself.
- Print each step's sorted latencies next to your p95.
- Remove the largest call and see how the spike changes.

## What a senior reviewer also looks for

A reviewer would check that the prices come from one table, that rounding happens only in the report, and that the report says how many calls it summarised. They would also ask for cost per user request, because finance will want to compare it with the value of each request, and for the same report to run every day so the next spike is caught within hours.

## Stretch goal

Add cost per day per feature as a small table and flag any day more than twice the average, so the team gets an early warning instead of a surprise on the bill.
