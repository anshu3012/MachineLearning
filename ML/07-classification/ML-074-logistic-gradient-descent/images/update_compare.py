"""Note ML-074 stills (Plotly).
cancel.png (Section 4): along z, the log's slope 1/y_hat (or -1/(1 - y_hat)) times the sigmoid's slope y_hat(1 - y_hat)
  gives the plain y - y_hat: the blow-up of the log is cancelled exactly.
update_compare.png (Section 5): on the Note's 100 points, the one-point rule of the sigmoid perceptron (lr 0.1, a random
  point per update, seed 0) against batch gradient descent (lr 0.5, all points per update), both from w = (1, 1, 1).
Run: python update_compare.py"""
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

warnings.simplefilter("ignore")
HERE = Path(__file__).parent
BLUE, GREEN, ORANGE, RED, GREY = "#4C78A8", "#54A24B", "#F58518", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
sig = lambda z: 1 / (1 + np.exp(-z))

# ---- cancel.png
z = np.linspace(-4, 4, 400)
s = sig(z)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("green point (y = 1): term y log ŷ", "red point (y = 0): term (1 − y) log(1 − ŷ)"))
for col, outer, name, prod, pname in ((1, 1 / s, "slope of log ŷ: 1/ŷ", 1 - s, "product: 1 − ŷ = y − ŷ"),
                                      (2, -1 / (1 - s), "slope of log(1 − ŷ): −1/(1 − ŷ)", -s, "product: −ŷ = y − ŷ")):
    assert np.allclose(outer * s * (1 - s), prod)                    # the cancellation of Sections 4.1 and 4.2
    fig.add_trace(go.Scatter(x=z, y=outer, line=dict(color=ORANGE, width=3, dash="dash", simplify=False), name=name), 1, col)
    fig.add_trace(go.Scatter(x=z, y=s * (1 - s), line=dict(color=BLUE, width=3, dash="dot", simplify=False),
                             name="sigmoid slope ŷ(1 − ŷ)", showlegend=(col == 1)), 1, col)
    fig.add_trace(go.Scatter(x=z, y=prod, line=dict(color=GREEN, width=5, simplify=False), name=pname), 1, col)
fig.update_xaxes(title="z = w·x", range=[-4, 4])
fig.update_yaxes(range=[-3, 3])
fig.update_layout(template="simple_white", width=1150, height=600, font=FONT, margin=dict(l=60, r=20, t=50, b=170),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "cancel.png", scale=2)

# ---- update_compare.png
X, y = make_classification(n_samples=100, n_features=2, n_informative=2, n_redundant=0, n_classes=2,
                           n_clusters_per_class=1, random_state=4, class_sep=1.5)
Xb = np.insert(X, 0, 1, axis=1)
sk = LogisticRegression(penalty=None, max_iter=100000, tol=1e-10).fit(X, y)
L_min = log_loss(y, sk.predict_proba(X)[:, 1])
assert round(L_min, 4) == 0.1366
N = 5000
wb, wo, rng = np.ones(3), np.ones(3), np.random.default_rng(0)
Lb, Lo = [log_loss(y, sig(Xb @ wb))], [log_loss(y, sig(Xb @ wo))]
for _ in range(N):
    wb = wb + 0.5 * Xb.T @ (y - sig(Xb @ wb)) / len(y)               # batch: all 100 points
    j = rng.integers(len(y))
    wo = wo + 0.1 * (y[j] - sig(Xb[j] @ wo)) * Xb[j]                 # one random point
    Lb.append(log_loss(y, sig(Xb @ wb))); Lo.append(log_loss(y, sig(Xb @ wo)))
Lb, Lo = np.array(Lb), np.array(Lo)
assert round(Lb[100], 4) == 0.1484 and round(Lb[1000], 4) == 0.1368 and abs(Lb[-1] - L_min) < 1e-4
print("one-point loss after 1000 / 5000 updates:", Lo[1000].round(4), Lo[-1].round(4), "batch:", Lb[-1].round(4))
assert Lo[-1] > Lb[-1]
u = np.arange(N + 1)
fig = go.Figure()
fig.add_trace(go.Scatter(x=u[1:], y=Lo[1:], line=dict(color=ORANGE, width=2), name="one random point per update (sigmoid perceptron)"))
fig.add_trace(go.Scatter(x=u[1:], y=Lb[1:], line=dict(color=BLUE, width=4), name="all 100 points per update (batch)"))
fig.add_trace(go.Scatter(x=[1, N], y=[L_min] * 2, line=dict(color=GREY, width=2, dash="dash"), name=f"scikit-learn minimum {L_min:.4f}"))
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, margin=dict(l=70, r=20, t=30, b=60),
                  xaxis=dict(title="number of updates (log scale)", type="log"), yaxis=dict(title="log loss on all 100 points", range=[0.1, 0.6]),
                  legend=dict(x=0.98, xanchor="right", y=0.98, bgcolor="rgba(255,255,255,0.9)"))
fig.write_image(HERE / "update_compare.png", scale=2)
