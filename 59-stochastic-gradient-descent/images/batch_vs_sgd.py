"""Test R2 on the diabetes data after each epoch: batch (learning rate 0.5) vs stochastic (learning rate 0.01) (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_diabetes
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
n = len(X_train)
rng = np.random.default_rng(0)
bb, wb, bs, ws = 0.0, np.ones(10), 0.0, np.ones(10)
rb, rs = [], []
for e in range(60):
    err = y_train - (X_train @ wb + bb)
    bb += 0.5 * 2 * err.mean(); wb += 0.5 * 2 * X_train.T @ err / n
    for _ in range(n):
        i = rng.integers(n); er = y_train[i] - (X_train[i] @ ws + bs)
        bs += 0.01 * 2 * er; ws += 0.01 * 2 * er * X_train[i]
    rb.append(r2_score(y_test, X_test @ wb + bb)); rs.append(r2_score(y_test, X_test @ ws + bs))
ep = list(range(1, 61))
fig = go.Figure()
fig.add_trace(go.Scatter(x=ep, y=rb, mode="lines", name="batch: 1 update per epoch", line=dict(color="#E45756", width=4)))
fig.add_trace(go.Scatter(x=ep, y=rs, mode="lines", name="stochastic: 353 updates per epoch", line=dict(color="#F58518", width=4)))
fig.add_trace(go.Scatter(x=[1, 60], y=[0.44] * 2, mode="lines", name="OLS (0.44)", line=dict(color="#6B6B6B", dash="dash")))
fig.update_layout(template="simple_white", width=950, height=460, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(x=0.5, y=0.6), margin=dict(l=70, r=30, t=50, b=60),
                  title=dict(text="Diabetes data: test R² after each epoch", x=0.5),
                  xaxis=dict(title="epoch"), yaxis=dict(title="test R²", range=[-0.05, 0.5]))
print("epoch 10:", round(rb[9], 3), round(rs[9], 3), " epoch 40:", round(rb[39], 3), round(rs[39], 3))
fig.write_image(here / "batch_vs_sgd.png", scale=2)
fig.write_image(here / "batch_vs_sgd.pdf")
