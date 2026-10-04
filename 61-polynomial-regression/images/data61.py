"""Shared data (no output when run): the Notebook's 200 points y = 0.8x^2 + 0.9x + 2 + noise (seed 42), split 80/20
with random_state 2; and the 25-training / 200-test design of Section 4 (seed 42), as in degrees.py."""
import numpy as np
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(42)
X = 6 * rng.random((200, 1)) - 3
y = (0.8 * X ** 2 + 0.9 * X + 2 + rng.standard_normal((200, 1))).ravel()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
rng2 = np.random.default_rng(42)
f = lambda x: 0.8 * x ** 2 + 0.9 * x + 2
X_tr = 6 * rng2.random((25, 1)) - 3; y_tr = f(X_tr).ravel() + rng2.standard_normal(25)
X_te = 6 * rng2.random((200, 1)) - 3; y_te = f(X_te).ravel() + rng2.standard_normal(200)
