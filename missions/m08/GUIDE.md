# Self-study guide: Show the client what attention attends to

Sceptical engineering teams ask how a model reaches its output before they let it near their systems. Computing attention by hand, mask and all, lets you show them, and the numerical-stability trick in it is the same one inside every framework. It also builds the intuition you need to explain context, decoding and hallucination to clients.

## Revise first (in the course)

- scaled dot-product attention step by step
- causal attention with a mask
- a numerically stable softmax

## Read the email like an FDE

The data scientist sets three technical conditions. 'Plain Python, no NumPy' means lists and loops. 'The causal mask a decoder uses' means a token may only look at itself and earlier tokens. 'It must not overflow when scores get large' points at softmax: exponentials of large numbers overflow unless you shift the scores first. 'Which earlier token it attends to most' is a question about the weights, not the outputs.

## Questions to ask the client first

- **Which head and layer do these vectors come from?** Explanations from one head can mislead; the client should know what the example shows.
- **Is the output for engineers only, or for a wider audience?** The level of detail and the way weights are shown depend on who reads it.
- **Should padding tokens be masked too?** Real batches pad sequences, and attention to padding distorts the picture.

## How each criterion is checked

1. **softmax sums to 1:** softmax of three numbers must sum to 1.
2. **softmax survives huge scores:** softmax of two huge equal scores must return two halves instead of overflowing.
3. **Attention outputs and weights are right:** attention without the mask must match the expected outputs and weights to many decimal places.
4. **The causal mask hides later tokens:** attention with the mask must give the first token exactly zero weight on the second, and match the expected weights.
5. **Each token's favourite is found:** most_attended on the masked weights must return each token's favourite index.

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
| OverflowError in math.exp | The largest score was not subtracted first. | Shift by the maximum before taking exponentials. |
| Masked weights are small but not zero | A large negative number was used instead of minus infinity. | Use minus infinity; its exponential is exactly zero. |
| Outputs have the wrong shape | Rows and columns of V were mixed up. | Each output has one value per column of V, summed over tokens. |
| Weights are too sharp | The scaling by the square root of the dimension was left out. | Divide every dot product by the square root of the key length. |

## Test yourself before you check

- Check that every row of weights sums to 1.
- Print the masked weights as a grid: everything above the diagonal should be zero.
- Compute one weight by hand for the first two tokens and compare.
- Feed softmax a list of large and small numbers together and look for nan.

## What a senior reviewer also looks for

A reviewer would look for small, named functions (dot product, softmax, weighted sum) that each map to a line of the formula, so the client's engineers can check them against a paper. They would also check that the mask is applied before the softmax, not after, and that inputs are not changed in place.

## Stretch goal

Add a temperature argument to softmax and show the client how the favourite tokens change as it rises and falls, with a short note on what that means for decoding.
