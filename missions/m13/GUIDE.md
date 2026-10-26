# Self-study guide: The cheapest model setup that meets the latency target

Model choice is a cost decision the client's finance team will review every month. At tens of thousands of conversations a day, a few tenths of a cent per request becomes a large bill, and prompt caching or a smaller model can cut it several times over. Clients expect an FDE to show the trade-off in dollars a month against a latency target, not in prices per million tokens.

## Revise first (in the course)

- the KV cache and prefix-caching economics
- cost engineering for LLM workloads
- monthly input-token cost with prefix caching

## Read the email like an FDE

The product director gives you the traffic shape and the pricing rule. The system prompt and policy pack never change, so they are the prefix that caching can bill at the cached rate, but only for the share of requests that hit the cache. The conversation tokens change every time, so they are always billed at the full input price, and output has its own price. Prices are per million tokens. 'A month' is defined as 30 days. 'Cheapest while keeping p95 latency within 1,500 ms' is a filter first and a minimum second, and an empty result is possible.

## Questions to ask the client first

- **Is the measured p95 latency from your own region and at your peak hour?** Latency measured off-peak or far away can pass the filter and fail in production.
- **How stable is the system prompt between releases?** Every change to the prefix resets the cache, so the real hit rate may be lower than hoped.
- **Will traffic grow, and should the model choice hold at double the volume?** A choice that is cheapest today may cross a pricing tier or rate limit later.

## How each criterion is checked

1. **One request without caching:** request_cost for the middle model without caching must equal half a cent per request, to many decimal places.
2. **One request with a 90 percent cache hit on the prefix:** request_cost for the same model with 90 percent of the prefix cached must equal the expected smaller cost.
3. **Monthly cost without caching:** monthly_cost for all three models without caching must match the expected monthly totals, rounded to cents.
4. **Monthly cost with caching:** monthly_cost for all three models with 90 percent caching must match the expected totals.
5. **The cheapest model within the latency target:** cheapest with a 1,500 ms target and caching must pick the expected small model.
6. **A tight target leaves only the fast models; an impossible one leaves none:** cheapest must pick the faster of two models under a tight target, and return None when no model is fast enough.

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
| Costs are a million times too big | Prices are per million tokens and were used per token. | Divide by one million once, at the end of the request cost. |
| Caching saves too much | The conversation tokens were treated as cacheable. | Only the fixed prefix can hit the cache. |
| cheapest crashes when nothing is fast enough | min() was called on an empty list. | Return None when no model passes the filter. |
| The monthly total is a few cents off | Rounding happened per request. | Round only the monthly figure. |

## Test yourself before you check

- Work one request by hand for the middle model: tokens times price, divided by a million.
- Print a table of monthly cost with and without caching for all three models.
- Try a hit rate of 0 and of 1 and check the cost moves between the two extremes.
- Lower the latency target step by step and watch which models drop out.

## What a senior reviewer also looks for

A reviewer would want the assumptions (30 days, hit rate, token counts) shown next to the result, because finance will challenge them. They would check the code never mixes up input, cached and output prices, and that the latency filter comes before the cost comparison, so a cheap but slow model can never be recommended.

## Stretch goal

Add a sensitivity row: the monthly cost of the chosen model at 50, 70 and 90 percent cache hit rates, so the client sees how much depends on keeping the prompt stable.
