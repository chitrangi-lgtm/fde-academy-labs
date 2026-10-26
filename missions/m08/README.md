# Show the client what attention attends to

**From:** Leila Haddad, Principal Data Scientist, Morrow Analytics

Our engineers don't trust what they can't inspect. For a four-token example I've attached the query, key and value vectors from one attention head. Please implement scaled dot-product attention in plain Python (our review environment has no NumPy), with the causal mask a decoder uses, and tell us for each token which earlier token it attends to most. It must not overflow when scores get large.

## Done when

- `softmax(xs)` returns probabilities that sum to 1 and works for very large inputs
- `attention(Q, K, V, causal=False)` returns (outputs, weights) as lists of lists, with weights = softmax of Q·K / sqrt(d) and outputs = weights × V
- With causal=True, a token gives zero weight to later tokens
- `most_attended(weights)` returns, for each token, the index it gives the most weight to

## Files

`qkv.json`

## Work and check

Write your code in `solution.py`, then from the kit's folder run:

```bash
python tools/fde_check.py m08
```

There are no steps: how you build it is up to you. `GUIDE.md` explains how to read the email, how each criterion is checked and the common mistakes. If you are stuck, `NUDGES.md` has two hints and then the approach in plain English. The course site's version of this challenge records your score.
