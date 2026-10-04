"""The two problems of section 5, measured on the digits data with useless random features added (the red line of
Figure 2: same seed). Left: the share of images whose nearest other image shows the same digit (98.8, 91.0, 72.5
percent at 64, 164, 464 features). Right: time to score KNN with 5-fold cross-validation, best of 3 runs (machine
dependent)."""
from pathlib import Path
import time
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_digits
from sklearn.metrics import pairwise_distances
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier

here = Path(__file__).parent
X, y = load_digits(return_X_y=True)
noise = np.random.default_rng(0).uniform(0, 16, (len(X), 400))
NS = [0, 50, 100, 200, 300, 400]
same, secs = [], []
for n in NS:
    Z = np.hstack([X, noise[:, :n]])
    D = pairwise_distances(Z); np.fill_diagonal(D, np.inf)
    same.append(np.mean(y[D.argmin(axis=1)] == y))
    t = []
    for _ in range(3):
        s = time.perf_counter(); cross_val_score(KNeighborsClassifier(), Z, y, cv=5); t.append(time.perf_counter() - s)
    secs.append(min(t))
assert [round(100 * same[i], 1) for i in (0, 2, 5)] == [98.8, 91.0, 72.5] and secs[-1] > secs[0]
F = [64 + n for n in NS]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, subplot_titles=[
    "1. performance: nearest image shows the same digit", "2. computation: time to score KNN"])
fig.add_scatter(x=F, y=[100 * s for s in same], mode="lines+markers+text", text=[f"{100 * s:.1f}%" for s in same],
                textposition="top right", cliponaxis=False, line=dict(color="#E45756", width=4), marker=dict(size=10), row=1, col=1)
fig.add_scatter(x=F, y=secs, mode="lines+markers", line=dict(color="#4C78A8", width=4), marker=dict(size=10), row=1, col=2)
fig.update_xaxes(title_text="features (64 pixels + random)", range=[40, 500], row=1, col=1)
fig.update_xaxes(title_text="features (64 pixels + random)", row=1, col=2)
fig.update_yaxes(title_text="percent of images", range=[60, 103], row=1, col=1)
fig.update_yaxes(title_text="seconds (this machine)", rangemode="tozero", row=1, col=2)
for a in fig.layout.annotations[:2]:
    a.font.size = 19
fig.update_layout(template="simple_white", width=1400, height=500, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=60, b=70))
fig.write_image(here / "two_problems.png", scale=2)
fig.write_image(here / "two_problems.pdf")
