"""Section 7: density-connected points on the Note's 14 points with eps = 1 and min_samples = 4 (the animation's
settings). Lines join core points at most eps apart; every point reachable along such a chain is in the same cluster.
The two groups are not linked: no chain of core points crosses the gap. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
from toy_points import X, EPS, MIN_SAMPLES

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=18)
m = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(X)
core = np.zeros(len(X), bool)
core[m.core_sample_indices_] = True
assert core.sum() == 8 and set(m.labels_) == {-1, 0, 1}
D = cdist(X, X)
COL = {0: "#4C78A8", 1: "#F58518", -1: "#6B6B6B"}
fig = go.Figure()
for i in range(len(X)):
    for j in range(i + 1, len(X)):
        if D[i, j] <= EPS and core[i] and core[j]:
            fig.add_scatter(x=X[[i, j], 0], y=X[[i, j], 1], mode="lines", line=dict(color=COL[m.labels_[i]], width=3), showlegend=False)
        elif D[i, j] <= EPS and (core[i] or core[j]):
            fig.add_scatter(x=X[[i, j], 0], y=X[[i, j], 1], mode="lines", line=dict(color="#BBBBBB", width=2, dash="dot"), showlegend=False)
for kind, mask, sym, size in (("core", core, "circle", 15), ("border or noise", ~core, "circle-open", 13)):
    fig.add_scatter(x=X[mask, 0], y=X[mask, 1], mode="markers", name=kind,
                    marker=dict(size=size, symbol=sym, color=[COL[l] for l in m.labels_[mask]], line=dict(width=2.5)))
fig.update_layout(template="simple_white", width=900, height=560, font=FONT,
                  title=dict(text="solid lines: core points at most eps apart (a chain); dotted: a core point reaching a border point", x=0.5, font=dict(size=16)),
                  xaxis=dict(range=[-0.5, 7.2], title="feature 1"), yaxis=dict(range=[0.2, 4.2], title="feature 2", scaleanchor="x"),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18), margin=dict(l=60, r=20, t=60, b=90))
fig.write_image(here / "chains.png", scale=2)
fig.write_image(here / "chains.pdf")
