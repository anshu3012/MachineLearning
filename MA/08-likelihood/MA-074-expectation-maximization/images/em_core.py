"""Plain NumPy EM for a Gaussian mixture in any dimension (imported by the figure scripts; running it runs a check).
E-step: responsibilities. M-step: weighted means, then weighted covariances around the NEW means, then weights
(the order of MML Section 11.3)."""
import numpy as np
from scipy import stats

BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
COLS = [BLUE, ORANGE, GREEN]
FONT = dict(family="Latin Modern Roman", size=20)


def weighted_dens(X, pi, mu, cov):
    """pi_k N(x_n | mu_k, cov_k) for every observation n and component k; X has shape (N, D)."""
    return np.column_stack([p * stats.multivariate_normal(m, c).pdf(X) for p, m, c in zip(pi, mu, cov)])


def loglik(X, pi, mu, cov):
    return np.log(weighted_dens(X, pi, mu, cov).sum(axis=1)).sum()


def e_step(X, pi, mu, cov):
    W = weighted_dens(X, pi, mu, cov)
    return W / W.sum(axis=1, keepdims=True)


def m_step(X, R):
    Nk = R.sum(axis=0)
    mu = (R.T @ X) / Nk[:, None]
    cov = [((R[:, k, None] * (X - mu[k])).T @ (X - mu[k])) / Nk[k] for k in range(R.shape[1])]
    return Nk / len(X), mu, np.array(cov)


def run_em(X, pi, mu, cov, iters):
    """Return the list of (pi, mu, cov, R, loglik) after 0, 1, ..., iters iterations."""
    hist = [(pi, mu, cov, e_step(X, pi, mu, cov), loglik(X, pi, mu, cov))]
    for _ in range(iters):
        R = e_step(X, pi, mu, cov)
        pi, mu, cov = m_step(X, R)
        hist.append((pi, mu, cov, e_step(X, pi, mu, cov), loglik(X, pi, mu, cov)))
    return hist


SEVEN = np.array([-3, -2.5, -1, 0, 2, 4, 5.0])[:, None]
START = (np.ones(3) / 3, np.array([[-4.0], [0.0], [8.0]]), np.array([[[1.0]], [[0.2]], [[3.0]]]))


def faithful():
    """Old Faithful eruptions: duration (minutes) and waiting time (minutes), 272 observations."""
    import pandas as pd
    from pathlib import Path
    df = pd.read_csv(Path(__file__).parent.parent / "data" / "old_faithful.csv")
    return df[["duration", "waiting"]].to_numpy(float)


FAITHFUL_START = (np.ones(2) / 2, np.array([[2.0, 90.0], [4.5, 50.0]]), np.array([np.diag([1.0, 100.0])] * 2))


def three_clusters():
    """Constructed data: two long tilted clusters and a round one (500 observations), used for random starts."""
    rng = np.random.default_rng(5)
    covs = [np.array([[6, 2.6], [2.6, 1.4]])] * 2 + [np.eye(2) * 0.6]
    means = [np.array([0, 0]), np.array([0, 4]), np.array([6, -2])]
    return np.vstack([rng.multivariate_normal(m, c, n) for m, c, n in zip(means, covs, [200, 200, 100])])


THREE_START = (np.ones(3) / 3, np.array([[-4.0, 6.0], [-3.0, -3.0], [2.0, 1.0]]), np.array([np.eye(2)] * 3))

if __name__ == "__main__":
    h = run_em(SEVEN, *START, 5)
    pi, mu, cov = h[1][:3]
    assert np.allclose(mu.ravel(), [-2.70, -0.40, 3.70], atol=0.01)            # MML Example 11.3
    assert np.allclose(cov.ravel(), [0.14, 0.44, 1.53], atol=0.01)             # MML Example 11.4
    assert np.allclose(pi, [0.29, 0.29, 0.42], atol=0.01)                      # MML Example 11.5
    assert abs(h[0][4] + 28.3) < 0.05 and abs(h[1][4] + 14.4) < 0.05
    lls = [x[4] for x in run_em(faithful(), *FAITHFUL_START, 60)]
    assert all(b >= a - 1e-9 for a, b in zip(lls, lls[1:]))
