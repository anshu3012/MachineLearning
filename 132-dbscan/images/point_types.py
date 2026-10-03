"""Core, border and noise points with their eps-neighbourhoods (Plotly). Types come from scikit-learn's DBSCAN."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances

from toy_points import EPS, MIN_SAMPLES, X

here = Path(__file__).parent
db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(X)
core = np.zeros(len(X), bool); core[db.core_sample_indices_] = True
kind = np.where(core, "core", np.where(db.labels_ == -1, "noise", "border"))
count = (pairwise_distances(X) <= EPS).sum(1)
print(list(zip(kind, count)))
assert list(kind[[2, 5, 12]]) == ["core", "border", "noise"]

fig = go.Figure()
show = {2: "#4C78A8", 5: "#F58518", 12: "#6B6B6B"}
for i, col in show.items():
    x, y = X[i]
    fig.add_shape(type="circle", x0=x - EPS, x1=x + EPS, y0=y - EPS, y1=y + EPS, line=dict(color=col, width=2.5, dash="dot"), fillcolor="rgba(0,0,0,0)", layer="below")
style = {"core": dict(color="#4C78A8", size=16, symbol="circle"),
         "border": dict(color="#F58518", size=16, symbol="circle-open", line=dict(width=3)),
         "noise": dict(color="#6B6B6B", size=14, symbol="x")}
for k in ("core", "border", "noise"):
    m = kind == k
    fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=f"{k} point", marker=style[k]))
notes = {2: (f"core: {count[2]} points within eps (at least {MIN_SAMPLES})", -30, 150),
         5: (f"border: only {count[5]} within eps,<br>but one of them is a core point", -190, -300),
         12: (f"noise: {count[12]} point within eps<br>and no core point", 60, -60)}
for i, (t, ax, ay) in notes.items():
    fig.add_annotation(x=X[i, 0], y=X[i, 1], text=t, ax=ax, ay=ay, font=dict(size=16, color=show[i]),
                       arrowcolor=show[i], bgcolor="white", align="left")
fig.update_layout(template="simple_white", width=1000, height=620, font=dict(family="Latin Modern Roman", size=17),
                  xaxis=dict(range=[-0.6, 7.6], showticklabels=False, ticks=""),
                  yaxis=dict(range=[-0.2, 5.6], scaleanchor="x", showticklabels=False, ticks=""),
                  legend=dict(x=0.78, y=0.98), margin=dict(l=20, r=20, t=20, b=20))
fig.write_image(here / "point_types.png", scale=2); fig.write_image(here / "point_types.pdf")
