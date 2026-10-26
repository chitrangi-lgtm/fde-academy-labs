# Why LoRA works: low-rank approximation with SVD

**Libraries:** NumPy · **Level:** Advanced · about 30 minutes

A client asks why fine-tuning only a few million parameters can adapt a billion-parameter model. Show it: a 64 x 64 weight update W is already loaded. Approximate it with rank r, measure the error, find the smallest rank within 5 percent, and count the parameters LoRA trains instead of the full matrix.

Write your code in `lab.py`, then run `python tools/fde_check.py m19-py1` from the kit's folder. `GUIDE.md` has the ideas, the steps check by check and the common mistakes.

<details><summary>Hints</summary>

1. `U, S, Vt = np.linalg.svd(W)`; the rank-r approximation is `(U[:, :r] * S[:r]) @ Vt[:r]`.
2. Frobenius norm: `np.linalg.norm(M)`.
3. A d x k matrix has d*k parameters; B and A together have r*(d + k).
</details>

## Why it matters

Fine-tuning updates tend to be low rank, so two thin matrices capture almost all of the change. That is why LoRA trains well under 1 percent of a layer's parameters and fits on a free GPU.
