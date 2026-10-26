# Self-study guide: A sensitivity chart for the steering committee

The steering committee will ask 'what if the benefits are 20 percent lower?' before it signs. The claims assistant's case is 420,000 dollars a year of benefit, 600,000 up front and 80,000 a year to run, over three years at a 10 percent discount rate. You build the NPV, swing each driver by 20 percent either way, rank the drivers by how much they move the NPV, and draw a tornado chart.

## Revise first (in the course)

- presenting ROI, TCO, payback and sensitivity
- ROI, payback and a tornado table
- a tornado sensitivity table for the CFO

## Questions to ask the client first

- **Which assumptions has finance already challenged?** The tornado should test the assumptions the committee doubts most.
- **Is 20 percent the right swing for every driver?** Upfront costs are often known more precisely than benefits; equal swings can mislead.
- **Does the committee want three years or a longer horizon?** A longer horizon changes NPV and can change which driver matters most.

## Ideas you will use

- **Net present value:** Money in later years is worth less today. Each year's net benefit is divided by (1 + rate) to the power of the year and added up, then the upfront cost, paid today, is subtracted.
- **One-at-a-time sensitivity:** Change one driver, keep the others at their base values, and recompute. The low and high NPVs show how much the decision depends on that one assumption.
- **Swing:** The difference between a driver's high and low NPV. Ranking drivers by swing tells the committee where to spend its questions.
- **Tornado chart:** One horizontal bar per driver, from its low to its high NPV, the largest swing at the top and a line at the base NPV. Its shape gives the chart its name.

## Steps, check by check

1. **The base NPV is right:** Write npv so the base case matches finance's figure and a simple two-year case also works.
2. **Each driver has a low and a high case:** For each of the three drivers, compute the NPV with that driver 20 percent lower and 20 percent higher.
3. **A 20 percent lower benefit is costed:** Check that the lower-benefit case gives the expected, much smaller NPV.
4. **Benefits matter most, then the upfront cost:** Rank the drivers by swing, largest first.
5. **A chart is drawn:** Draw the tornado chart with a line at the base NPV.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If the base NPV is off, print each year's discounted amount and check the upfront cost is not discounted. If a driver's range is wrong, make sure you changed only that driver and kept the base values of the others. If the ranking is wrong, print each swing.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| NPV is too low | The upfront cost was discounted. | Subtract the upfront cost as it is, today's money. |
| Every driver moves together | The base dictionary was changed in place. | Copy the base values before changing one driver. |
| The running cost's low case gives the lower NPV | Low and high were taken from the factor, not the result. | Store the smaller and larger NPV, whichever factor produced them. |
| The chart's bars start at zero | The bars' left edge was not set. | Start each bar at its low NPV and make it as long as the swing. |

## What the result means for the client

The case stays positive even with benefits 20 percent lower, but only just, and the benefit assumption moves the NPV far more than the upfront or running cost. Tell the committee the decision rests on the benefit case, and propose how the benefits will be measured in the first quarter after go-live.

## What to send the client

One slide for the steering committee: the base NPV, the tornado chart, and one sentence naming the assumption the decision depends on and how it will be tracked.

## Stretch goal

Find the benefit level at which NPV becomes zero (the break-even benefit) and add it to the slide as the number the programme must beat.
