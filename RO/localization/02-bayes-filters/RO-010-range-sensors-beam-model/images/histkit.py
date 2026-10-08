"""Helpers for the histogram figures of the 1000 wall readings (no output when run on its own)."""
import numpy as np

from beammodel import ZMAX, ZSTAR, p_hit, p_rand, p_short

EDGES = np.round(np.arange(0, ZMAX + 0.051, 0.05), 3)       # 0.05 m bins; the last bin [5.00, 5.05) holds the max readings


def counts(z):
    return np.histogram(z, bins=EDGES)[0]


def expected_counts(n, w, sig, lam, zs=ZSTAR):
    """How many of n readings the model puts in each bin: n x (area of the mixture over the bin)."""
    out = []
    for a, b in zip(EDGES[:-1], EDGES[1:]):
        if a >= ZMAX - 1e-9:
            out.append(n * w["max"])                        # the whole failure spike sits in the last bin
            continue
        g = np.linspace(a, min(b, ZMAX), 201)
        dens = w["hit"] * p_hit(g, zs, sig) + w["short"] * p_short(g, zs, lam) + w["rand"] * p_rand(g)
        out.append(n * np.trapezoid(dens, g))
    return np.array(out)
