"""Shared data (no output when run): the 16 points of the Note's figures, 8 green (+1) and 8 red (-1)."""
import numpy as np

G = np.array([(2, 6), (3.5, 7.5), (4.5, 6), (6, 7.5), (2.5, 8.5), (5, 9), (7, 9), (7.5, 6.8)])
R = np.array([(1, 1.5), (2.5, 3), (3.5, 1), (5, 2.5), (6.5, 1.5), (7, 3.5), (1.5, 3.8), (4, 3.5)])
X, y = np.r_[G, R], np.r_[np.ones(len(G)), -np.ones(len(R))]
xs = np.array([0, 8.5])
line = lambda w, b, shift=0.0: (shift - b - w[0] * xs) / w[1]
