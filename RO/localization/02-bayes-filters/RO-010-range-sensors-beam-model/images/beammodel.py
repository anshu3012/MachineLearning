"""Shared numbers and functions for this Note's figures (no output when run on its own).
The room is 5 m x 4 m; the robot stands at pose (2, 2, 0) and its laser reads up to z_max = 5 m.
Beam model (Thrun et al. 2005, Section 6.3): a weighted mix of four densities for one range reading z,
given the expected range z_star from ray casting."""
from pathlib import Path

import numpy as np

ZMAX = 5.0                     # longest reading the laser reports (m)
STEP = 0.01                    # the laser reports ranges in 1 cm steps; the max-range spike is one step wide
SIG_HIT = 0.05                 # spread of measurement noise (m)
LAM = 2.0                      # rate of the short-reading part (1/m)
W = dict(hit=0.75, short=0.12, max=0.05, rand=0.08)   # mixture weights, sum 1
ZSTAR = 3.0                    # expected range of the beam that looks at the far wall
ROOM = (5.0, 4.0)              # room width and depth (m); walls on x = 0, x = 5, y = 0, y = 4
POSE = (2.0, 2.0, 0.0)         # robot pose (x, y, theta)
DATA = Path(__file__).resolve().parent.parent / "data" / "wall_readings.csv"


def gauss(z, mu, sig):
    return np.exp(-0.5 * ((z - mu) / sig) ** 2) / (sig * np.sqrt(2 * np.pi))


def p_hit(z, zs, sig=SIG_HIT):
    """Gaussian around z_star, cut to [0, z_max] and rescaled so its area is 1."""
    from math import erf, sqrt
    area = 0.5 * (erf((ZMAX - zs) / (sig * sqrt(2))) - erf((0 - zs) / (sig * sqrt(2))))
    z = np.asarray(z, float)
    return np.where((z >= 0) & (z <= ZMAX), gauss(z, zs, sig) / area, 0.0)


def p_short(z, zs, lam=LAM):
    """Exponential that starts high at 0 and stops at z_star; eta = 1 / (1 - exp(-lam z_star))."""
    z = np.asarray(z, float)
    eta = 1.0 / (1.0 - np.exp(-lam * zs))
    return np.where((z >= 0) & (z <= zs), eta * lam * np.exp(-lam * z), 0.0)


def p_max(z):
    """The point mass at z_max, drawn as a box one sensor step wide (height 1 / STEP, area 1)."""
    z = np.asarray(z, float)
    return np.where(z >= ZMAX - STEP / 2, 1.0 / STEP, 0.0)


def p_rand(z):
    z = np.asarray(z, float)
    return np.where((z >= 0) & (z <= ZMAX), 1.0 / ZMAX, 0.0)


def mixture(z, zs, w=W, sig=SIG_HIT, lam=LAM):
    return (w["hit"] * p_hit(z, zs, sig) + w["short"] * p_short(z, zs, lam)
            + w["max"] * p_max(z) + w["rand"] * p_rand(z))


def raycast(pose, ang, room=ROOM, step=0.001):
    """Expected range: walk along the beam in small steps until it leaves the room (hits a wall)."""
    x, y, th = pose
    d = 0.0
    while d < ZMAX:
        px, py = x + d * np.cos(th + ang), y + d * np.sin(th + ang)
        if not (0 < px < room[0] and 0 < py < room[1]):
            return round(d, 2)
        d += step
    return ZMAX


def simulate(n=1000, seed=0, zs=ZSTAR):
    """n readings of the beam that faces the wall 3 m away, each from one of the four causes."""
    rng = np.random.default_rng(seed)
    cause = rng.choice(4, size=n, p=[W["hit"], W["short"], W["max"], W["rand"]])
    z = np.empty(n)
    for i, c in enumerate(cause):
        if c == 0:
            v = rng.normal(zs, SIG_HIT)
            while not 0 <= v <= ZMAX:
                v = rng.normal(zs, SIG_HIT)
        elif c == 1:                                   # first object on the beam, before the wall
            v = rng.exponential(1 / LAM)
            while v > zs:
                v = rng.exponential(1 / LAM)
        elif c == 2:
            v = ZMAX
        else:
            v = rng.uniform(0, ZMAX)
        z[i] = v
    return np.round(z, 2), cause


def em(z, zs=ZSTAR, iters=60, w0=None, sig0=0.3, lam0=0.5, history=False):
    """EM for the four weights, sigma_hit and lambda_short (Thrun et al. 2005, Section 6.3.4)."""
    w = dict(w0 or dict(hit=0.25, short=0.25, max=0.25, rand=0.25))
    sig, lam = sig0, lam0
    hist = []
    for _ in range(iters):
        parts = np.vstack([w["hit"] * p_hit(z, zs, sig), w["short"] * p_short(z, zs, lam),
                           w["max"] * p_max(z), w["rand"] * p_rand(z)])
        tot = parts.sum(0)
        hist.append((dict(w), sig, lam, np.log(tot).sum()))
        e = parts / tot                                # E-step: responsibilities, one column per reading
        n = len(z)
        w = dict(hit=e[0].sum() / n, short=e[1].sum() / n, max=e[2].sum() / n, rand=e[3].sum() / n)
        sig = np.sqrt((e[0] * (z - zs) ** 2).sum() / e[0].sum())
        lam = e[1].sum() / (e[1] * z).sum()
    parts = np.vstack([w["hit"] * p_hit(z, zs, sig), w["short"] * p_short(z, zs, lam),
                       w["max"] * p_max(z), w["rand"] * p_rand(z)])
    hist.append((dict(w), sig, lam, np.log(parts.sum(0)).sum()))
    return (w, sig, lam, hist) if history else (w, sig, lam)


def load():
    return np.loadtxt(DATA, delimiter=",", skiprows=1)
