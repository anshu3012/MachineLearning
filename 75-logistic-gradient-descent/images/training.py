"""Logistic regression by batch gradient descent vs scikit-learn (penalty=None) on 100 overlapping points (Plotly)."""
from pathlib import Path
import numpy as np
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
warnings.simplefilter("ignore")

here = Path(__file__).parent
sig = lambda z: 1 / (1 + np.exp(-z))
X, y = make_classification(n_samples=100, n_features=2, n_informative=2, n_redundant=0, n_classes=2,
                           n_clusters_per_class=1, random_state=4, class_sep=1.5)
sk = LogisticRegression(penalty=None, max_iter=100000, tol=1e-10).fit(X, y)
w_sk = np.r_[sk.intercept_, sk.coef_[0]]
loss_sk = log_loss(y, sk.predict_proba(X)[:, 1])
Xb = np.insert(X, 0, 1, axis=1)
w = np.ones(3)
losses, snaps = [], {}
for e in range(1, 5001):
    w = w + 0.5 * (Xb.T @ (y - sig(Xb @ w))) / len(y)
    losses.append(log_loss(y, sig(Xb @ w)))
    if e in (10, 100, 1000, 5000):
        snaps[e] = w.copy()

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=("Log loss per epoch", "The line after 10, 100, 1000 and 5000 epochs"))
ep = np.arange(1, 5001)
fig.add_trace(go.Scatter(x=ep, y=losses, mode="lines", line=dict(color="#4C78A8", width=4), name="gradient descent"), 1, 1)
fig.add_trace(go.Scatter(x=[1, 5000], y=[loss_sk] * 2, mode="lines", line=dict(color="black", width=3, dash="dash"),
                         name=f"scikit-learn's minimum ({loss_sk:.4f})"), 1, 1)
for k, c in ((1, "#54A24B"), (0, "#4C78A8")):
    fig.add_trace(go.Scatter(x=X[y == k, 0], y=X[y == k, 1], mode="markers", marker=dict(color=c, size=8, opacity=0.8),
                             showlegend=False), 1, 2)
xs = np.array([-4.5, 1.2])
shades = {10: "#FDD0A2", 100: "#FDAE6B", 1000: "#F16913", 5000: "#A63603"}
for e, wv in snaps.items():
    fig.add_trace(go.Scatter(x=xs, y=-(wv[0] + wv[1] * xs) / wv[2], mode="lines", line=dict(color=shades[e], width=3),
                             name=f"epoch {e}"), 1, 2)
fig.add_trace(go.Scatter(x=xs, y=-(w_sk[0] + w_sk[1] * xs) / w_sk[2], mode="lines", line=dict(color="black", width=2, dash="dash"),
                         showlegend=False), 1, 2)
fig.update_xaxes(type="log", title="epoch", row=1, col=1, exponentformat="power", dtick=1)
fig.update_yaxes(title="log loss", row=1, col=1, range=[0.12, 0.3])
fig.update_xaxes(title="x₁", range=[-4.5, 1.2], row=1, col=2)
fig.update_yaxes(title="x₂", range=[-4.3, 3.8], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=520, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=20, t=50, b=110))
fig.write_image(here / "training.png", scale=2); fig.write_image(here / "training.pdf")
print(w.round(4), w_sk.round(4))
