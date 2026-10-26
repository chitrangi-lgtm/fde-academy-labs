# Self-study guide: Where did the money go? Model cost by feature

Finance saw last week's model bill jump on one day. calls.csv has a week of usage, one row per day, feature and model, with input, output and cached tokens; PRICES gives dollars per million tokens for input, cached input and output on three example models. You find what each feature cost, the spike day, the feature behind it, and the share of input tokens served from the cache.

## Revise first (in the course)

- where agent cost comes from
- prompt caching and context engineering for cost
- the cost of a run with prompt caching

## Questions to ask the client first

- **Do these example prices match your contract with the provider?** Negotiated or tiered prices change every figure; use the real table.
- **Is each feature's model choice deliberate?** Often one feature runs on an expensive model only because nobody revisited it.
- **Who should be told when daily cost passes a threshold?** A simple alert turns next month's surprise into today's message.

## Ideas you will use

- **Cost per row:** Uncached input tokens at the input price, cached tokens at the cheaper cached price, and output tokens at the output price, all divided by one million.
- **apply by row:** calls.apply(fn, axis=1) runs a function on each row and returns a column of results, which you can store as cost.
- **groupby and idxmax:** groupby('day')['cost'].sum() totals each day; idxmax returns the day with the highest total. The same pattern on one day's rows finds the costliest feature.
- **Cache hit rate:** Cached input tokens over all input tokens for the week. A low rate on an expensive model is often the cheapest saving available.

## Steps, check by check

1. **Cost per feature is right:** Add a cost column and total it per feature for the week, rounded to two decimals.
2. **The spike day is found:** Total cost per day and find the day with the highest total.
3. **Contract review caused it:** On that day, find the feature with the highest cost.
4. **The cache hit rate is right:** Divide the week's cached input tokens by all input tokens.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If feature costs are off, compute one row by hand and compare with your cost column. If the spike day is wrong, print the daily totals. If the cache rate is off, check you divided tokens, not costs or row counts. Before reporting, print the spike day's rows next to the same feature on a normal day: the difference in tokens and cached tokens is the evidence finance will ask to see.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| Costs are a million times too large | Prices are per million tokens. | Divide by one million. |
| Cached tokens are billed twice | All input tokens were billed at the full price. | Bill input minus cached at the input price. |
| spike_feature is the week's biggest | It was chosen across all days. | Choose the biggest feature on the spike day. |
| The cache rate is a share of rows | Rows with any cached tokens were counted. | Divide cached tokens by input tokens. |
| by_feature prints long decimals | Totals were not rounded. | Round each feature's total to two decimals. |

## What the result means for the client

Contract review on the most expensive model, with almost no caching, explains the spike day. Tell finance the cause in one sentence, then give the engineering team two options with their savings: cache contract review's fixed instructions, or route simple contracts to a cheaper model. Both options need a quality check before they ship, because a cheaper answer that misses a contract clause costs more than the tokens it saves.

## What to send the client

A table of cost by feature for the week, the spike day with its cause, the cache hit rate, and two costed savings options, sent to finance and the feature's engineering owner together.

## Stretch goal

Recompute the week's cost assuming contract review reached the cache hit rate of the other features, and report the saving in dollars a week. Then estimate the saving from moving half of contract review's calls to the middle model, and say which option you would test first and why.
