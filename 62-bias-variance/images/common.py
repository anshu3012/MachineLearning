"""Shared: the true curve, and polynomial models fitted to many training sets (no output when run).

Fixed design (ESL §7.3): every training set has the same 20 inputs x; only the noise in y is new each time.
Bias² and variance are measured at those 20 inputs."""
import warnings
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

warnings.simplefilter("ignore")
f = lambda x: np.sin(1.5 * x) + 0.5 * x
NOISE, N, SETS = 0.5, 20, 10_000
rng = np.random.default_rng(0)
X = np.sort(rng.uniform(-3, 3, (N, 1)), axis=0)        # the same 20 inputs in every training set
Y = f(X) + rng.normal(0, NOISE, (N, SETS))              # one column of noisy targets per training set
xs = np.linspace(-2.8, 2.8, 200)


def fits(degree):
    """Fit one model per training set (all at once: one target column each).
    Returns predictions at the training inputs (N x SETS) and on the plotting grid xs (200 x SETS)."""
    m = make_pipeline(PolynomialFeatures(degree, include_bias=False), StandardScaler(), LinearRegression()).fit(X, Y)
    return m.predict(X), m.predict(xs.reshape(-1, 1))


def decompose(P):
    """Bias squared and variance of the predictions P (inputs x sets), averaged over the training inputs."""
    return float(np.mean((P.mean(axis=1) - f(X).ravel()) ** 2)), float(np.mean(P.var(axis=1)))
