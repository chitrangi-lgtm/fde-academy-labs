# Self-study guide: Attention by hand in NumPy, with a heatmap

A client's engineers want to see self-attention working, not a diagram of it. Q, K and V for a four-token sequence are already loaded as NumPy arrays (four rows, two columns each). You implement scaled dot-product attention with an optional causal mask, keep it stable for very large scores, and draw the attention weights as a heatmap they can read.

## Revise first (in the course)

- scaled dot-product attention step by step
- causal attention with a mask
- a numerically stable softmax

## Questions to ask the client first

- **Do your engineers want to see one head or all heads of a layer?** One head is easy to read; a model has many, and they behave differently.
- **Will they compare this with the weights from the real model?** Matching numbers with the real model builds more trust than any diagram.
- **Should padding positions be shown?** Real batches include padding that is masked out, and that changes the picture.

## Ideas you will use

- **Scores:** Q @ K.T compares every query with every key in one matrix product; dividing by the square root of the key length keeps the scores in a range where softmax is not too sharp.
- **Softmax by row:** Each row of scores becomes probabilities that add up to 1. Subtracting the row's largest value before taking exponentials gives the same result and never overflows.
- **Causal mask:** In a decoder a token may only look at itself and earlier tokens. Setting the scores above the diagonal to minus infinity makes their weights exactly zero after the softmax.
- **Heatmap:** plt.imshow draws a matrix as coloured squares. With a colour bar and token labels on both axes, engineers can read which token attends to which.

## Steps, check by check

1. **The output matches scaled dot-product attention:** Compute the scores, apply the softmax by row and multiply the weights by V to get the output.
2. **The causal weights match:** Add the causal mask before the softmax when causal is true.
3. **Each row of weights sums to 1:** Make sure every row of weights adds up to 1.
4. **Token 1 cannot attend to token 2 under the mask:** Check that the first token gives exactly zero weight to the second under the mask.
5. **Large scores do not overflow (no NaN):** Subtract each row's maximum before the exponentials so very large scores do not produce NaN.
6. **A heatmap is drawn:** Draw the causal weights as a heatmap with a colour bar and labelled axes.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If the output check fails but the weights look right, check the order of the final product: weights times V. If the NaN check fails, print the scores for Q times 1000 and look at the exponentials. If the heatmap check fails, make sure a figure was actually drawn by your code, after the attention call.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| NaN appears with large scores | Exponentials overflowed. | Subtract each row's maximum first. |
| Masked weights are small but not zero | A large negative number was used instead of minus infinity. | Use minus infinity so the exponential is exactly zero. |
| Rows do not sum to 1 | The softmax divided by the sum of the whole matrix. | Divide each row by its own sum (keepdims helps). |
| Shapes do not match | K was not transposed. | Use Q @ K.T for the scores. |

## What the result means for the client

The heatmap shows, for each token, which earlier tokens it draws information from, with nothing above the diagonal because of the mask. For the client's engineers, this turns 'the model pays attention' into numbers they can inspect, and the stability trick explains why real frameworks never overflow.

## What to send the client

The heatmap and the weights table, with two sentences explaining the mask and the stability trick, sent to the client's engineers alongside the code so they can run it on their own vectors.

## Stretch goal

Add a temperature argument that divides the scores before the softmax, draw the weights at two temperatures side by side, and describe in one sentence how attention becomes sharper or flatter, and what that would mean for the model's output.
