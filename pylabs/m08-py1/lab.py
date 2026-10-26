import numpy as np
Q = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.5, -0.5]])
K = np.array([[1.0, 0.5], [0.0, 1.0], [1.0, -1.0], [0.5, 0.5]])
V = np.array([[1.0, 0.0], [0.0, 2.0], [3.0, 1.0], [0.5, 0.5]])

import numpy as np
import matplotlib.pyplot as plt

# Q, K and V (4 tokens x 2 dimensions) are already loaded.
print(Q, K, V, sep="\n\n")

def attention(Q, K, V, causal=False):
    """Return (output, weights): weights = softmax(Q K^T / sqrt(d)), output = weights V.
    With causal=True a token may only attend to itself and earlier tokens."""
    weights = np.zeros((Q.shape[0], K.shape[0]))
    return weights @ V, weights

out, w = attention(Q, K, V, causal=True)
# Draw w as a heatmap here (plt.imshow), with a colour bar and token numbers on the axes.
