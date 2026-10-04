"""The students data (IIT = sparse 0/1 feature, package = target) and AdaGrad / RMSProp paths for the figures."""
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
d = pd.read_csv(DATA / "students.csv")
X = np.c_[d.iit, np.ones(len(d))]                 # columns: IIT (for m), constant 1 (for b)
y = d.package.to_numpy()
BEST = np.linalg.lstsq(X, y, rcond=None)[0]       # the minimum (m, b)
START = np.array([-4.0, -4.0])
ETA = 0.2


def loss(p):
    return np.mean((y - X @ p) ** 2)


def grad(p):
    return -2 * X.T @ (y - X @ p) / len(y)


def run(kind, eta=ETA, steps=300, beta=0.9):
    """Path of (m, b) and the accumulator v for 'adagrad' (sum of squares) or 'rmsprop' (EWMA of squares)."""
    p, v, P, V = START.copy(), np.zeros(2), [START.copy()], []
    for _ in range(steps):
        g = grad(p)
        v = v + g ** 2 if kind == "adagrad" else beta * v + (1 - beta) * g ** 2
        p = p - eta * g / (np.sqrt(v) + 1e-8)
        P.append(p.copy())
        V.append(v.copy())
    return np.array(P), np.array(V)


def steps_to(P, tol=0.01):
    gap = np.array([loss(p) for p in P]) - loss(BEST)
    return int(np.argmax(gap < tol)) if (gap < tol).any() else None
