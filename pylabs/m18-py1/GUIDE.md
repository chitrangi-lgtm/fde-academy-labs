# Self-study guide: Find the slow span: p95 latency from traces

Users of a claims assistant say it is 'sometimes slow'. traces.csv has 24 traces, each with five spans (auth, retrieve, rerank, generate, guardrail) and their durations in milliseconds. You find each span's 95th-percentile latency, the span that dominates, and the traces whose spans add up to more than the 2.5-second budget, and draw a chart the operations lead can read in ten seconds.

## Revise first (in the course)

- tracing LLM systems with OpenTelemetry
- a trace bottleneck analyser
- service levels, error budgets and dashboards

## Questions to ask the client first

- **Is the 2.5-second budget for the whole request or for the assistant's part only?** Network and front-end time may already use part of the budget.
- **Are these traces from a normal day or from the slow period users complained about?** A quiet sample can hide the problem entirely.
- **Which percentile does your service level agreement use?** p95 and p99 tell different stories; report the one in the agreement.

## Ideas you will use

- **Spans and traces:** A trace is one user request; spans are its steps. Adding a trace's spans gives its total time, and grouping spans by name shows where time goes across requests.
- **Percentiles:** The 95th percentile is the time 95 percent of requests stay under. Averages hide slow requests; p95 shows what the slowest users experience.
- **groupby and quantile:** groupby('span')['ms'].quantile(0.95) computes every span's p95 in one line, using pandas' interpolated percentile, which is what the check expects here.
- **Charts for executives:** A horizontal bar chart sorted by value, with the unit on the axis and a title that states the finding, can be read at a glance.

## Steps, check by check

1. **p95 per span is right:** Compute each span's 95th-percentile duration, rounded to one decimal, into p95.
2. **Generation dominates the latency:** Find the span with the highest p95 and store its name in slowest_span.
3. **Two traces breached the budget:** Add up each trace's spans and list the traces over 2,500 ms, sorted.
4. **A chart is drawn:** Draw a bar chart of p95 by span with a labelled axis and a title.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If p95 values differ slightly, check you used pandas' quantile on each span's durations and rounded to one decimal. If the slow traces are wrong, print each trace's total and compare with 2,500. If the chart check fails, make sure your code draws a figure. Then go further than the checks: print the five spans of each slow trace side by side with a typical trace, and see which step is out of line. That comparison, not the percentile table, is what tells the team what to fix.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| p95 is computed over all spans together | The data was not grouped by span. | Group by span before taking the percentile. |
| slow_traces lists spans, not traces | Individual spans were compared with the budget. | Add up each trace's spans first. |
| A trace exactly at 2,500 ms is listed | The comparison included equality. | List only traces above the budget. |
| The chart has no labels | Only the bars were drawn. | Add the unit and a title that states the finding. |
| The slowest span is chosen by average | Means were compared instead of p95. | Pick the span with the highest p95, as the brief asks. |

## What the result means for the client

Generation has the highest p95, but the two traces over budget are slow because retrieval stalled, not because the model was slow. Tell the operations lead both facts: speeding up generation helps every request a little, while fixing the retrieval stalls removes the slow experiences users complain about.

## What to send the client

The chart, the p95 table and the two slow traces with their spans side by side, with a recommendation that separates the retrieval stalls (fix first) from generation speed (improve later), and a proposal to alert when any trace passes the budget so the next stall is caught the day it happens.

## Stretch goal

Draw each slow trace as a stacked bar of its spans next to a typical trace, so the stalled retrieval is visible at a glance, and add the budget as a vertical line.
