import numpy as np
_rng = np.random.default_rng(7)
W = _rng.normal(size=(64, 4)) @ _rng.normal(size=(4, 64)) + 0.01 * _rng.normal(size=(64, 64))

import numpy as np

# W (64 x 64) is already loaded.
print(W.shape, "rank", np.linalg.matrix_rank(W, tol=1e-6))

def approx(W, r):
    """The best rank-r approximation of W (truncated SVD)."""
    return W

def rel_error(W, r):
    """||W - approx(W, r)|| / ||W|| (Frobenius norm)."""
    return 1.0

best_r = 64            # the smallest r with rel_error below 0.05

def params_saved(d, k, r):
    """Parameters saved by training B (d x r) and A (r x k) instead of a d x k matrix."""
    return 0
