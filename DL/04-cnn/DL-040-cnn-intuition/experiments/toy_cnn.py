"""A toy CNN on 6 x 6 letters O and X (the size of the example in StatQuest's CNN video; our own letters, weights
and code). Pipeline: one 3 x 3 filter + bias -> 4 x 4 feature map -> ReLU -> max pooling -> Flatten -> one ReLU
node -> two outputs (O, X). Each network is fitted to the two centred letters only (targets O = (1, 0), X = (0, 1),
squared error, BFGS), then tested on the 8 letters shifted by one pixel (left, right, up, down).
Three networks, 50 random starts each: an ANN on the 36 flattened pixels, the CNN with 2 x 2 pooling, and the same
CNN with pooling over the whole 4 x 4 map. Only starts that learn both training letters (loss < 0.0001) are counted.
NumPy and SciPy only, so the numbers repeat exactly.  Run: python experiments/toy_cnn.py -> data/toy_cnn.json"""
import json
from pathlib import Path
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent.parent
O, X = np.zeros((6, 6)), np.zeros((6, 6))
for r, c in [(1, 2), (1, 3), (4, 2), (4, 3), (2, 1), (3, 1), (2, 4), (3, 4)]:
    O[r, c] = 1
for i in range(4):
    X[1 + i, 1 + i] = X[1 + i, 4 - i] = 1
SHIFTS = {"right": (0, 1), "left": (0, -1), "down": (1, 0), "up": (-1, 0)}
shift = lambda a, d: np.roll(np.roll(a, d[0], 0), d[1], 1)       # the letters have a 1-pixel margin: nothing wraps
x_train, y_train = np.stack([O, X]), np.array([[1.0, 0.0], [0.0, 1.0]])
x_test = np.stack([shift(a, d) for a in (O, X) for d in SHIFTS.values()])
y_test = np.array([0] * 4 + [1] * 4)


def cnn_stages(w, x, pool):
    """Every stage of the CNN for a batch x; pool = 2 (2 x 2 windows) or 4 (the whole map)."""
    K, b = w[:9].reshape(3, 3), w[9]
    fmap = np.einsum("nijkl,kl->nij", sliding_window_view(x, (3, 3), axis=(1, 2)), K) + b
    relu = np.maximum(fmap, 0)
    q = 4 // pool
    pooled = relu.reshape(len(x), q, pool, q, pool).max((2, 4))
    flat = pooled.reshape(len(x), -1)
    d = flat.shape[1]
    W1, b1, W2, b2 = w[10:10 + d], w[10 + d], w[11 + d:13 + d], w[13 + d:15 + d]
    hidden = np.maximum(flat @ W1 + b1, 0)
    out = hidden[:, None] * W2 + b2
    return dict(K=K, b=b, fmap=fmap, relu=relu, pooled=pooled, W1=W1, b1=b1, hidden=hidden, W2=W2, b2=b2, out=out)


def ann_out(w, x):
    flat = x.reshape(len(x), -1)
    hidden = np.maximum(flat @ w[:36] + w[36], 0)
    return hidden[:, None] * w[37:39] + w[39:41]


MODELS = {"ANN on 36 flattened pixels": (41, ann_out),
          "CNN, 2 x 2 max pooling": (19, lambda w, x: cnn_stages(w, x, 2)["out"]),
          "CNN, max pooling over the whole map": (16, lambda w, x: cnn_stages(w, x, 4)["out"])}
summary, first_fit = {}, None
for name, (n, f) in MODELS.items():
    accs = []
    for seed in range(50):
        w0 = np.random.default_rng(seed).normal(0, 0.5, n)
        res = minimize(lambda w: ((f(w, x_train) - y_train) ** 2).mean(), w0, method="BFGS")
        if res.fun < 1e-4:
            accs.append(float((f(res.x, x_test).argmax(1) == y_test).mean()))
            if name.startswith("CNN, 2") and first_fit is None:
                first_fit = (seed, res.x)
    summary[name] = dict(weights=n, starts_that_fit=len(accs), shifted_accuracy=round(float(np.mean(accs)), 3))
    print(f"{name:38s} weights {n:2d}  fitted {len(accs):2d} of 50  shifted letters right: {np.mean(accs):.1%}")

seed, w = first_fit
st = cnn_stages(w, x_train, 2)
assert np.allclose(st["out"], y_train, atol=0.02)
walk = {k: np.round(v, 2).tolist() for k, v in st.items()}
shifted = cnn_stages(w, x_test, 2)["out"]
print("walk-through network: start", seed, "| outputs for O and X:", np.round(st["out"], 2).tolist())
print("its answers on the 8 shifted letters:", ["OX"[i] for i in shifted.argmax(1)], "truth: O O O O X X X X")
json.dump(dict(O=O.tolist(), X=X.tolist(), seed=seed, walk=walk, summary=summary,
               shifted_out=np.round(shifted, 2).tolist()), open(HERE / "data" / "toy_cnn.json", "w"), indent=1)
