"""Shared: the Notebook's 64 MNIST 0s and 1s, shrunk to 6 x 6, and its small CNN's forward pass (no output when run)."""
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).parent
with np.load(Path.home() / ".keras" / "datasets" / "mnist.npz") as d:
    x_train, y_train = d["x_train"], d["y_train"]
keep = np.isin(y_train, [0, 1])
BIG = x_train[keep][:64] / 255.0
SMALL = np.array([np.array(Image.fromarray(im).resize((6, 6), Image.BILINEAR)) for im in x_train[keep][:64]]) / 255.0
Y = (y_train[keep][:64] == 1).astype(float)
P = np.load(HERE.parent / "data" / "digit_example.npz")
W1, b1, W2, b2 = P["W1"], float(P["b1"]), P["W2"], float(P["b2"])
assert np.allclose(SMALL[0], P["X"]) and Y[0] == P["t"]


def F_of(X):
    n = 4
    Z1 = np.array([[(X[i:i + 3, j:j + 3] * W1).sum() for j in range(n)] for i in range(n)]) + b1
    A1 = np.maximum(Z1, 0)
    return A1.reshape(2, 2, 2, 2).max(axis=(1, 3)).reshape(4, 1)
