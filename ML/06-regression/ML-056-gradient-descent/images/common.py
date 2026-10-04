"""Shared data: the 4-point example (m fixed) and the 100-point example (no output when run)."""
import numpy as np
from sklearn.datasets import make_regression

X4, y4 = make_regression(n_samples=4, n_features=1, n_informative=1, n_targets=1, noise=80, random_state=13)
x4 = X4.ravel()
M4 = 78.35
loss_b = lambda b: float(np.sum((y4 - M4 * x4 - b) ** 2))
slope_b = lambda b: float(-2 * np.sum(y4 - M4 * x4 - b))
X100, y100 = make_regression(n_samples=100, n_features=1, n_informative=1, n_targets=1, noise=20, random_state=13)
x100 = X100.ravel()
BLUE, ORANGE, GREEN, RED, GREY, PURPLE = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
FONT = dict(family="Latin Modern Roman", size=15)


def descend_b(b0, lr, steps):
    bs = [b0]
    for _ in range(steps):
        bs.append(bs[-1] - lr * slope_b(bs[-1]))
    return np.array(bs)
