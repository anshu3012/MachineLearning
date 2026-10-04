"""Three obstacles for plain gradient descent (section 4). Left: the curve with a small dip of Figure 7,
L(w) = (w^2 - 4)^2 / 8 - 0.6 w; gradient descent from w = -3 (learning rate 0.05) stops in the local minimum.
Middle: a saddle, L = w1^2 - w2^2, with gradient descent starting almost on the ridge: it slows down near the
flat centre. Right: the narrow valley of Figure 1 with learning rate 0.019: the path zigzags across the steep sides.
Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
f = lambda w: (w ** 2 - 4) ** 2 / 8 - 0.6 * w
df = lambda w: w * (w ** 2 - 4) / 2 - 0.6
p = [-3.0]
for _ in range(80):
    p.append(p[-1] - 0.05 * df(p[-1]))
p = np.array(p)
assert -2.2 < p[-1] < -1.5                                # stuck in the small dip, left of the bump
s = [np.array([1.5, 0.001])]
for _ in range(32):
    x, y = s[-1]
    s.append(s[-1] - 0.1 * np.array([2 * x, -2 * y]))
s = np.array(s)
step = np.linalg.norm(np.diff(s, axis=0), axis=1)
assert step.min() < 0.05 * step[0]                       # near the saddle the steps almost stop
v = [np.array([-10.0, 0.4])]
for _ in range(25):
    a, b = v[-1]
    v.append(v[-1] - 0.019 * np.array([a, 100 * b]))
v = np.array(v)
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.07,
                    subplot_titles=("Local minimum", "Saddle point", "High curvature"))
w = np.linspace(-3.2, 3.2, 300)
fig.add_scatter(x=w, y=f(w), mode="lines", line=dict(color="#888", width=3), showlegend=False, row=1, col=1)
fig.add_scatter(x=p, y=f(p), mode="markers+lines", marker=dict(size=7, color="#4C78A8"), line=dict(color="#4C78A8"),
                showlegend=False, row=1, col=1)
fig.add_annotation(x=p[-1], y=f(p[-1]), text="stops here", ay=-45, showarrow=True, font=dict(size=16), row=1, col=1)
gx = np.linspace(-2, 2, 81)
GX, GY = np.meshgrid(gx, gx)
fig.add_trace(go.Contour(x=gx, y=gx, z=GX ** 2 - GY ** 2, colorscale="RdBu", reversescale=True, showscale=False,
                         contours=dict(coloring="lines"), line=dict(width=1.5)), row=1, col=2)
fig.add_scatter(x=s[:, 0], y=s[:, 1], mode="markers+lines", marker=dict(size=6, color="#4C78A8"),
                line=dict(color="#4C78A8"), showlegend=False, row=1, col=2)
g1, g2 = np.linspace(-11, 11, 121), np.linspace(-1, 1, 101)
G1, G2 = np.meshgrid(g1, g2)
fig.add_trace(go.Contour(x=g1, y=g2, z=(G1 ** 2 + 100 * G2 ** 2) / 2, colorscale="Greys", reversescale=True,
                         showscale=False, contours=dict(coloring="lines"), line=dict(width=1.2), ncontours=14), row=1, col=3)
fig.add_scatter(x=v[:, 0], y=v[:, 1], mode="markers+lines", marker=dict(size=6, color="#E45756"),
                line=dict(color="#E45756"), showlegend=False, row=1, col=3)
fig.update_xaxes(title_text="w", row=1, col=1)
fig.update_yaxes(title_text="loss", row=1, col=1)
fig.update_xaxes(title_text="w₁", range=[-2, 2], row=1, col=2)
fig.update_yaxes(title_text="w₂", range=[-2, 2], row=1, col=2)
fig.update_xaxes(title_text="w₁", row=1, col=3)
fig.update_yaxes(title_text="w₂", row=1, col=3)
fig.update_layout(template="simple_white", width=1500, height=520, font=dict(family="Latin Modern Roman", size=18),
                  margin=dict(l=60, r=20, t=60, b=60))
for a in fig.layout.annotations[:3]:
    a.font.size = 20
fig.write_image(HERE / "obstacles.png", scale=2)
print("dip stop", round(p[-1], 3), "saddle steps", step[[0, 10, 20, 30]].round(4), step.argmin(), step.min().round(4))
