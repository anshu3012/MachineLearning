"""Shared model for Section 6 (no output when run on its own): RO-013's hallway as a continuous line of positions.
10 m joined into a loop (10 m is 0 m again); doors in front of 1-2, 3-4 and 7-8 m (cells 1, 3 and 7, cell k covering
k to k + 1 m). Old belief: after one "door" reading, 0.1875 per m at a door and 0.0625 per m at a wall.
Command: move 2 m. Motion model: a Gaussian centred 2 m ahead with standard deviation 0.45 m."""
import numpy as np
from scipy.stats import norm

LOOP, U, SIGMA = 10.0, 2.0, 0.45
DOORS = ((1, 2), (3, 4), (7, 8))
AT_DOOR, AT_WALL = 0.1875, 0.0625
BROWN = "#9C755F"
X = np.linspace(0, LOOP, 2001)                      # positions for drawing and checking (m)


def old_belief(x):
    """bel(x_{t-1}), per m."""
    x = np.mod(np.asarray(x, float), LOOP)
    return np.where(np.any([(x >= a) & (x < b) for a, b in DOORS], axis=0), AT_DOOR, AT_WALL)


def piece(a, b, x=X):
    """What the old belief between a and b m (inside one metre, so flat) adds to the predicted belief at x, per m:
    every point of the stretch moves 2 m on with the motion model's spread; whatever passes 10 m comes back at 0 m."""
    level = float(old_belief((a + b) / 2))
    return level * sum(norm.cdf((x - U - a - w) / SIGMA) - norm.cdf((x - U - b - w) / SIGMA)
                       for w in (-LOOP, 0.0, LOOP))


def predicted(x=X):
    """The predicted belief, the integral of the prediction step: all ten metres' pieces added."""
    return sum(piece(k, k + 1, x) for k in range(int(LOOP)))
