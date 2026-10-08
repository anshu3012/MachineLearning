"""Shared three-step hallway run for smoothing and Viterbi (no output when run on its own).
t = 1: stay, reads door; t = 2: move 2, reads door; t = 3: move 2, reads wall. True cells 1, 3, 5. p(x1) = 0.1 each."""
import numpy as np

from hallplot import KERNEL, N, likelihood

T = np.zeros((N, N))                       # T[i, j] = p(x_t = j | move 2, x_t-1 = i)
for i in range(N):
    for step, p in KERNEL.items():
        T[i, (i + step) % N] += p
ZS = [1, 1, 0]
ALPHA = [0.1 * likelihood(ZS[0])]
for z in ZS[1:]:
    ALPHA.append(likelihood(z) * (ALPHA[-1] @ T))
BETA = [np.ones(N)]
for z in ZS[:0:-1]:
    BETA.insert(0, T @ (likelihood(z) * BETA[0]))
FILTERED = [a / a.sum() for a in ALPHA]
SMOOTHED = [a * b / (a * b).sum() for a, b in zip(ALPHA, BETA)]
M = [0.1 * likelihood(ZS[0])]
BACK = []
for z in ZS[1:]:
    cand = M[-1][:, None] * T
    BACK.append(cand.argmax(axis=0))
    M.append(likelihood(z) * cand.max(axis=0))
PATH = [int(M[-1].argmax())]
for bp in BACK[::-1]:
    PATH.insert(0, int(bp[PATH[0]]))
