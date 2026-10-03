"""Shared numbers for the 640 figures (imported, not a figure itself): the mixture of MML Figure 11.2,
p(x) = 0.5 N(x | -2, 0.5) + 0.2 N(x | 1, 2) + 0.3 N(x | 4, 1) (second numbers are variances)."""
import numpy as np
from scipy import stats

BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
COLS = [BLUE, ORANGE, GREEN]
PI = np.array([0.5, 0.2, 0.3])
MU = np.array([-2.0, 1.0, 4.0])
VAR = np.array([0.5, 2.0, 1.0])
FONT = dict(family="Latin Modern Roman", size=20)


def components(x):
    """Weighted component densities, shape (len(x), 3)."""
    return PI * stats.norm(MU, np.sqrt(VAR)).pdf(np.asarray(x)[:, None])


def mixture(x):
    return components(x).sum(axis=1)


def sample(n, rng):
    """Two-step sampling: pick a component with probabilities PI, then draw from it."""
    z = rng.choice(3, size=n, p=PI)
    return z, rng.normal(MU[z], np.sqrt(VAR[z]))


if __name__ == "__main__":
    g = np.linspace(-10, 12, 20001)
    assert abs(np.trapezoid(mixture(g), g) - 1) < 1e-6
