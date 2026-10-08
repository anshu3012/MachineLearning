"""The beam model of the beam-model Note (weights 0.75, 0.12, 0.05, 0.08; sigma 0.05 m; lambda 2 per m), used here
only to compare with the likelihood field (no output when run on its own)."""
from math import erf, sqrt

import numpy as np

from fieldmodel import ANGLES, ZMAX, raycast

W = dict(hit=0.75, short=0.12, max=0.05, rand=0.08)
SIG_HIT, LAM, STEP = 0.05, 2.0, 0.01


def mixture(z, zs):
    area = 0.5 * (erf((ZMAX - zs) / (SIG_HIT * sqrt(2))) - erf(-zs / (SIG_HIT * sqrt(2))))
    hit = np.exp(-0.5 * ((z - zs) / SIG_HIT) ** 2) / (SIG_HIT * sqrt(2 * np.pi)) / area if 0 <= z <= ZMAX else 0.0
    short = lam_short(z, zs)
    mx = 1 / STEP if z >= ZMAX - STEP / 2 else 0.0
    return W["hit"] * hit + W["short"] * short + W["max"] * mx + W["rand"] / ZMAX


def lam_short(z, zs):
    if 0 <= z <= zs:
        return LAM * np.exp(-LAM * z) / (1 - np.exp(-LAM * zs))
    return 0.0


def beam_loglik(occ, pose, z, angles=ANGLES):
    return sum(np.log(mixture(zz, raycast(occ, pose, a))) for zz, a in zip(z, angles))
