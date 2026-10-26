# Self-study guide: Why LoRA works: low-rank approximation with SVD

A client asks why fine-tuning only a few million parameters can adapt a billion-parameter model. A 64 by 64 weight update W is already loaded; it is almost low rank, like real fine-tuning updates. You approximate it with rank r using the singular value decomposition, measure the error, find the smallest rank within 5 percent, and count the parameters LoRA trains instead of the full matrix.

## Revise first (in the course)

- fine-tuning versus retrieval, and LoRA
- LoRA trainable parameters and QLoRA memory
- a LoRA adapter planner

## Questions to ask the client first

- **Which layers would you fine-tune, and how large are they?** The parameter savings depend on the layer shapes and how many layers are adapted.
- **Have you measured how well the base model does without fine-tuning?** If prompting or retrieval already meets the target, fine-tuning may not be needed.
- **Which GPU will training run on?** On a free 16 GB GPU, the adapter's small size is what makes training possible at all.

## Ideas you will use

- **Rank:** The rank of a matrix is how many independent directions it really uses. A 64 by 64 matrix can have rank up to 64, but one built from a 64 by 4 and a 4 by 64 matrix has rank at most 4.
- **Singular value decomposition:** np.linalg.svd splits a matrix into U, S and Vt; the singular values in S are sorted from largest to smallest. Keeping the first r of them gives the best possible rank-r approximation.
- **Relative error:** The Frobenius norm of the difference divided by the norm of the original says how much of the matrix the approximation misses, as a share. Below 0.05 means within 5 percent.
- **LoRA's two thin matrices:** Instead of training a d by k matrix, LoRA trains B (d by r) and A (r by k): r times (d + k) parameters. For large layers and small r, that is under one percent.

## Steps, check by check

1. **approx keeps the shape:** Write approx so it returns a 64 by 64 matrix built from the first r singular values and vectors.
2. **A rank-1 approximation has rank 1:** Check that the rank-1 approximation really has rank 1.
3. **The error falls as the rank grows:** Write rel_error and check that the error falls as the rank grows.
4. **best_r is the smallest rank within 5 percent:** Find the smallest rank whose relative error is below 0.05 and store it in best_r.
5. **LoRA with r=8 on a 4096 x 4096 layer saves 16,711,680 parameters:** Write params_saved: the full matrix's parameters minus those of the two thin matrices.

## How to work it

1. The first run downloads Python and the lab's libraries into your browser (about 10 MB) and can take a minute; after that they are kept, and runs take a second or two.
2. Run the starter before changing anything: it prints the data and its types, which is where most surprises are.
3. Do one step at a time and print the result of each, comparing it with what you expect from the data.
4. Press Check my work after each step: the checks run in your browser, so they are free and instant.
5. When a check fails, read its name and message, then print the variable it looks at.
6. When everything passes, read the 'what the result means' section and write the two-sentence answer you would send the client: the number, what it means for them, and anything you excluded or assumed.
7. Open the reference solution only after you pass or after three real attempts, and look for one idea you did not use.

## When a check fails

If approx has the wrong shape, check that you multiply U's first r columns, the first r singular values and Vt's first r rows in that order. If the error does not fall, print the singular values: they must be used from the largest. If best_r is wrong, print the error for ranks 1 to 8.

## Common mistakes

| What you see | Why | Fix |
|---|---|---|
| approx returns a 64 by 4 matrix | Only part of the product was computed. | Multiply all three parts back together. |
| The rank-1 matrix has rank 2 | Two singular values were kept. | Slice with :r, which keeps exactly r. |
| best_r is one too high | The search started at 0 or used 'below or equal'. | Start at rank 1 and use strictly below 0.05. |
| params_saved is negative | The two counts were subtracted the wrong way round. | Subtract the adapter's parameters from the full matrix's. |

## What the result means for the client

The update is captured almost perfectly by a very small rank, so two thin matrices hold nearly all of the change. On a real 4,096 by 4,096 layer with rank 8, LoRA trains about 65 thousand parameters instead of 16.8 million. That is the answer for the client: fine-tuning changes are low rank, so LoRA keeps quality while making training cheap enough for a free GPU.

## What to send the client

A short explainer for the client with the error-by-rank table, the smallest rank within 5 percent, and the parameter count for one of their real layers, ending with a recommendation on the rank to start with.

## Stretch goal

Plot the relative error against the rank and mark the 5 percent line, so the client can see where adding rank stops paying for itself.
