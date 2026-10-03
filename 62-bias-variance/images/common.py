"""Shared: the true curve, and polynomial models fitted to many resampled training sets (no output when run)."""
import warnings
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

warnings.simplefilter("ignore")
f = lambda x: np.sin(1.5 * x) + 0.5 * x
NOISE = 0.5
xs = np.linspace(-2.8, 2.8, 200)


def fits(degree, n_sets=200, n=40, seed=0):
    """Predictions on xs from one model per random training set."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n_sets):
        X = rng.uniform(-3, 3, (n, 1)); y = f(X).ravel() + rng.normal(0, NOISE, n)
        m = make_pipeline(PolynomialFeatures(degree, include_bias=False), StandardScaler(), LinearRegression()).fit(X, y)
        out.append(m.predict(xs.reshape(-1, 1)))
    return np.array(out)


def decompose(P):
    """Average over xs of bias squared and variance of the predictions P (sets x points)."""
    mean = P.mean(axis=0)
    return float(np.mean((mean - f(xs)) ** 2)), float(np.mean(P.var(axis=0)))
