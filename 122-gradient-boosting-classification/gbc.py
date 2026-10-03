"""Gradient boosting for binary classification, written out (log loss), plus the two-Gaussians data.
Used by the Notebook and by images/figs.py."""
import numpy as np
from sklearn.datasets import make_gaussian_quantiles
from sklearn.tree import DecisionTreeRegressor


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def boost(X, y, n_trees, learning_rate=1.0, max_leaf_nodes=4):
    """Return F0 (log-odds of class 1) and a list of (tree, leaf values)."""
    f0 = np.log(y.mean() / (1 - y.mean()))          # stage 1: log(#ones / #zeros)
    F = np.full(len(y), f0)                         # current log-odds of every row
    stages = []
    for _ in range(n_trees):
        p = sigmoid(F)                              # log-odds -> probability
        r = y - p                                   # pseudo-residual: actual minus probability
        tree = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=42).fit(X, r)
        leaf = tree.apply(X)                        # which leaf each row lands in
        values = {j: r[leaf == j].sum() / (p[leaf == j] * (1 - p[leaf == j])).sum()   # leaf value in log-odds
                  for j in np.unique(leaf)}
        F = F + learning_rate * np.array([values[j] for j in leaf])
        stages.append((tree, values))
    return f0, stages


def log_odds(f0, stages, learning_rate, X_new, m=None):
    """F0 + learning_rate * (leaf value of tree 1 + ... + tree m)."""
    F = np.full(len(X_new), f0)
    for tree, values in stages[:m]:
        F = F + learning_rate * np.array([values[j] for j in tree.apply(X_new)])
    return F


def two_gaussians():
    """A ring-shaped class pattern: a wide Gaussian split by distance from (0, 0), plus a second Gaussian at (4, 4)
    with its labels flipped. 1500 points, two classes."""
    X1, y1 = make_gaussian_quantiles(cov=3.0, n_samples=1000, n_features=2, n_classes=2, random_state=1)
    X2, y2 = make_gaussian_quantiles(mean=(4, 4), cov=1, n_samples=500, n_features=2, n_classes=2, random_state=1)
    return np.vstack([X1, X2]), np.concatenate([y1, 1 - y2])
