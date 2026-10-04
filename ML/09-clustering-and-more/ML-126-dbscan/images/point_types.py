"""Core, border and noise points with their eps-neighbourhoods (Plotly), eps = 1 and MinPts = 5.
Types come from scikit-learn's DBSCAN; the circled points hold 5, 3 and 2 points."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances

# core (0) with 4 neighbours; border (1) shares one more neighbour (2) with it; noise (5) has one non-core neighbour
X = np.array([[2.0, 2.0], [2.95, 2.1], [2.5, 2.6], [1.4, 2.3], [1.9, 1.2], [5.0, 2.0], [5.6, 2.5]])
EPS, MIN_SAMPLES = 1.0, 5

here = Path(__file__).parent
db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(X)
core = np.zeros(len(X), bool); core[db.core_sample_indices_] = True
kind = np.where(core, "core", np.where(db.labels_ == -1, "noise", "border"))
count = (pairwise_distances(X) <= EPS).sum(1)
print(list(zip(kind, count)))
assert list(kind[[0, 1, 5]]) == ["core", "border", "noise"]
assert list(count[[0, 1, 5]]) == [5, 3, 2]

fig = go.Figure()
show = {0: "#4C78A8", 1: "#F58518", 5: "#6B6B6B"}
for i, col in show.items():
    x, y = X[i]
    fig.add_shape(type="circle", x0=x - EPS, x1=x + EPS, y0=y - EPS, y1=y + EPS, line=dict(color=col, width=2.5, dash="dot"), fillcolor="rgba(0,0,0,0)", layer="below")
style = {"core": dict(color="#4C78A8", size=16, symbol="circle"),
         "border": dict(color="#F58518", size=16, symbol="circle-open", line=dict(width=3)),
         "noise": dict(color="#6B6B6B", size=14, symbol="x")}
for k in ("core", "border", "noise"):
    m = kind == k
    fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=f"{k} point", marker=style[k]))
notes = {0: (f"core: {count[0]} points within eps<br>(at least {MIN_SAMPLES})", -120, 140),
         1: (f"border: only {count[1]} within eps,<br>but one of them is a core point", 60, -160),
         5: (f"noise: {count[5]} points within eps<br>and no core point", 60, 130)}
for i, (t, ax, ay) in notes.items():
    fig.add_annotation(x=X[i, 0], y=X[i, 1], text=t, ax=ax, ay=ay, font=dict(size=16, color=show[i]),
                       arrowcolor=show[i], bgcolor="white", align="left")
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=17),
                  xaxis=dict(range=[0.2, 7.4], showticklabels=False, ticks=""),
                  yaxis=dict(range=[0.3, 3.9], scaleanchor="x", showticklabels=False, ticks=""),
                  legend=dict(x=0.78, y=0.98), margin=dict(l=20, r=20, t=20, b=20))
fig.write_image(here / "point_types.png", scale=2); fig.write_image(here / "point_types.pdf")
