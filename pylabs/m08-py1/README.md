# Attention by hand in NumPy, with a heatmap

**Libraries:** NumPy, matplotlib · **Level:** Intermediate · about 35 minutes

A client's engineers want to see self-attention, not a diagram of it. Q, K and V for a four-token sequence are already loaded. Implement scaled dot-product attention with an optional causal mask, keep it numerically stable for large scores, and draw the attention weights as a heatmap.

Write your code in `lab.py`, then run `python tools/fde_check.py m08-py1` from the kit's folder.

<details><summary>Hints</summary>

1. Scores: `Q @ K.T / np.sqrt(K.shape[1])`.
2. For the mask, set the scores above the diagonal to `-np.inf` with `np.triu(np.ones(...), 1)`; exp(-inf) is 0.
3. Subtract each row's maximum before `np.exp`: the softmax is unchanged and nothing overflows.
</details>

## Why it matters

Attention is three matrix products and a softmax. The causal mask is what makes a decoder generate left to right, and subtracting the row maximum is the standard trick that keeps softmax stable.
