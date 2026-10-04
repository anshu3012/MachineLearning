"""Example placement data shared by this Note's figures: IQ, CGPA -> placed (1) or not (0)."""
import numpy as np


def placement_data(n=60, seed=4):
    rng = np.random.default_rng(seed)
    iq = rng.uniform(75, 135, n)
    cgpa = rng.uniform(5.0, 9.8, n)
    score = 0.04 * iq + cgpa                       # higher IQ and CGPA -> more likely placed
    placed = (score + rng.normal(0, 0.35, n) > 11.8).astype(int)
    return np.column_stack([iq, cgpa]), placed
