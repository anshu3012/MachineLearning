"""Diabetes data, learning rate 0.1, 100 epochs: test R2 after each epoch for several batch sizes (Plotly). Fixed seed."""
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
colours = {1: "#F58518", 8: "#54A24B", 32: "#4C78A8", 353: "#E45756"}
fig = go.Figure()
for bs, colour in colours.items():
    rng = np.random.default_rng(0); b, w = 0.0, np.ones(10); scores = []
    for _ in range(100):
        idx = rng.permutation(n)
        for s in range(0, n, bs):
            j = idx[s:s + bs]; err = y_train[j] - (X_train[j] @ w + b)
            b += 0.1 * 2 * err.mean(); w += 0.1 * 2 * X_train[j].T @ err / len(j)
        scores.append(r2_score(y_test, X_test @ w + b))
    label = {1: "batch size 1 (stochastic)", 353: "batch size 353 (batch)"}.get(bs, f"batch size {bs}")
    upd = -(-n // bs)
    fig.add_trace(go.Scatter(x=list(range(1, 101)), y=scores, mode="lines", name=f"{label}: {upd} update{"s" if upd > 1 else ""}/epoch",
                             line=dict(color=colour, width=3)))
    print(bs, upd, [round(scores[k], 3) for k in (9, 49, 99)])
fig.add_trace(go.Scatter(x=[1, 100], y=[0.44] * 2, mode="lines", name="OLS (0.44)", line=dict(color="#6B6B6B", dash="dash")))
fig.update_layout(template="simple_white", height=480, font=dict(family="Latin Modern Roman", size=15),
                  legend=dict(orientation="v", x=1.02, y=0.5), width=1150, margin=dict(l=70, r=30, t=50, b=60),
                  title=dict(text="Diabetes data, learning rate 0.1: test R² after each epoch", x=0.5),
                  xaxis=dict(title="epoch"), yaxis=dict(title="test R²", range=[-0.1, 0.5]))
fig.write_image(here / "batch_sizes.png", scale=2)
fig.write_image(here / "batch_sizes.pdf")
