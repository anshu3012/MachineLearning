"""The students data (IIT = sparse 0/1 feature, package = target) and five optimizers for the figures."""
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
d = pd.read_csv(DATA / "students.csv")
X = np.c_[d.iit, np.ones(len(d))]                 # columns: IIT (for m), constant 1 (for b)
y = d.package.to_numpy()
BEST = np.linalg.lstsq(X, y, rcond=None)[0]
START = np.array([-4.0, -4.0])


def loss(p):
    return np.mean((y - X @ p) ** 2)


def grad(p):
    return -2 * X.T @ (y - X @ p) / len(y)


def run(kind, eta, steps=300, b1=0.9, b2=0.999):
    p, m, v, P = START.copy(), np.zeros(2), np.zeros(2), [START.copy()]
    for t in range(1, steps + 1):
        g = grad(p)
        if kind == "gd":
            p = p - eta * g
        elif kind == "momentum":
            m = b1 * m + eta * g
            p = p - m
        elif kind == "adagrad":
            v = v + g ** 2
            p = p - eta * g / (np.sqrt(v) + 1e-8)
        elif kind == "rmsprop":
            v = 0.9 * v + 0.1 * g ** 2
            p = p - eta * g / (np.sqrt(v) + 1e-8)
        else:                                          # Adam
            m = b1 * m + (1 - b1) * g
            v = b2 * v + (1 - b2) * g ** 2
            p = p - eta * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + 1e-8)
        P.append(p.copy())
    return np.array(P)


def steps_to(P, tol=0.01):
    gap = np.array([loss(p) for p in P]) - loss(BEST)
    return int(np.argmax(gap < tol)) if (gap < tol).any() else None


SETTINGS = {"gradient descent, η = 0.3": ("gd", 0.3), "momentum, η = 0.1": ("momentum", 0.1),
            "AdaGrad, η = 2": ("adagrad", 2.0), "RMSProp, η = 0.3": ("rmsprop", 0.3), "Adam, η = 0.5": ("adam", 0.5)}
