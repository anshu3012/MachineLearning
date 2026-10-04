"""Shared run (no output when run): the GDRegressor of Section 4 on the diabetes data (353 training patients,
random_state 2), learning rate 0.5, 1,000 epochs, from intercept 0 and every coefficient 1; history per epoch."""
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
NAMES = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]
ols = LinearRegression().fit(X_train, y_train)
n = len(X_train)
b, w = 0.0, np.ones(X.shape[1])
HIST = [(b, w.copy(), r2_score(y_test, X_test @ w + b))]
for _ in range(1000):
    err = y_train - (X_train @ w + b)
    b, w = b - 0.5 * (-2 * err.mean()), w - 0.5 * (-2 * (X_train.T @ err) / n)
    HIST.append((b, w.copy(), r2_score(y_test, X_test @ w + b)))
assert n == 353 and round(HIST[-1][0], 2) == 152.01 and round(HIST[-1][2], 3) == 0.453
assert round(ols.intercept_, 2) == 151.88 and round(ols.score(X_test, y_test), 3) == 0.440
