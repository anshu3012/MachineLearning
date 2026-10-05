"""The six-point hand example (shared module, not a figure): points 1, 2, 3, 6, 7, 8 and a deliberately poor start of
two normal curves A and B, both with variance 4 and weight 0.5, centred at 2 and 4. Provides E-step, M-step and
log-likelihood; running it checks the numbers quoted in the Notes."""
import numpy as np
from scipy.stats import norm

BLUE, ORANGE, GREY, RED = "#4C78A8", "#F58518", "#6B6B6B", "#E45756"
COLS = [BLUE, ORANGE]
FONT = dict(family="Latin Modern Roman", size=22)
X = np.array([1, 2, 3, 6, 7, 8.0])
START = (np.array([0.5, 0.5]), np.array([2.0, 4.0]), np.array([4.0, 4.0]))   # weights, means, variances


def weighted(x, pi, mu, var):
    """pi_k N(x | mu_k, var_k) for every point and component, shape (len(x), 2)."""
    return pi * norm.pdf(np.asarray(x)[:, None], mu, np.sqrt(var))


def e_step(pi, mu, var):
    w = weighted(X, pi, mu, var)
    return w / w.sum(axis=1, keepdims=True)


def m_step(r):
    n = r.sum(axis=0)
    mu = (r * X[:, None]).sum(axis=0) / n
    var = (r * (X[:, None] - mu) ** 2).sum(axis=0) / n
    return n / len(X), mu, var


def loglik(pi, mu, var):
    return np.log(weighted(X, pi, mu, var).sum(axis=1)).sum()


def run(iters):
    """List of (pi, mu, var, loglik) at iteration 0..iters."""
    p = START
    out = [(*p, loglik(*p))]
    for _ in range(iters):
        p = m_step(e_step(*p))
        out.append((*p, loglik(*p)))
    return out


if __name__ == "__main__":
    r = e_step(*START)
    assert np.allclose(r[:, 0], [0.731, 0.622, 0.5, 0.182, 0.119, 0.076], atol=0.001)
    pi, mu, var = m_step(r)
    assert np.allclose(mu, [2.695, 5.569], atol=0.001) and np.allclose(var, [3.937, 5.609], atol=0.001)
    assert np.allclose(pi, [0.372, 0.628], atol=0.001)
    h = run(12)
    assert abs(h[0][3] + 15.819) < 0.001 and abs(h[1][3] + 14.152) < 0.001 and all(b[3] >= a[3] - 1e-9 for a, b in zip(h, h[1:]))
    print([round(s[3], 3) for s in h])
