"""Section 5's example on the Note's 14 points (toy_points.py) with eps = 1 and MinPts = 3: the circle of radius eps
around (1, 1) holds 4 points, itself included, so the region is dense; the circle around (2.7, 2.3) holds 2, so it
is sparse. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy.spatial.distance import cdist
from toy_points import X, EPS

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=18)
D = cdist(X, X)
count = (D <= EPS).sum(1)
assert count[0] == 4 and count[5] == 2
th = np.linspace(0, 2 * np.pi, 120)
fig = go.Figure()
fig.add_scatter(x=X[:, 0], y=X[:, 1], mode="markers", marker=dict(size=11, color="#6B6B6B"), showlegend=False)
for i, col, word in ((0, "#4C78A8", "dense"), (5, "#E45756", "sparse")):
    fig.add_scatter(x=X[i, 0] + EPS * np.cos(th), y=X[i, 1] + EPS * np.sin(th), mode="lines", line=dict(color=col, width=3, dash="dot"),
                    showlegend=False)
    inside = D[i] <= EPS
    fig.add_scatter(x=X[inside, 0], y=X[inside, 1], mode="markers", marker=dict(size=13, color=col), showlegend=False)
    fig.add_annotation(x=X[i, 0], y=X[i, 1] + EPS + 0.08, text=f"{count[i]} points within eps: {word}", showarrow=False,
                       font=dict(size=17, color=col), yanchor="bottom")
fig.update_layout(template="simple_white", width=900, height=560, font=FONT, title=dict(text="eps = 1, MinPts = 3", x=0.5),
                  xaxis=dict(range=[-0.5, 7.2], title="feature 1"), yaxis=dict(range=[-0.2, 4.0], title="feature 2", scaleanchor="x"),
                  margin=dict(l=60, r=20, t=60, b=60))
fig.write_image(here / "eps_count.png", scale=2)
fig.write_image(here / "eps_count.pdf")
