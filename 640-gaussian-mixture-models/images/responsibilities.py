"""Responsibilities for the running example of MML Section 11.2: seven points -3, -2.5, -1, 0, 2, 4, 5 and the
starting mixture N(-4, 1), N(0, 0.2), N(8, 3) with equal weights 1/3. Top: weighted components and points.
Bottom: r_k(x), the share of the mixture density at x that comes from component k (the three always add to 1)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

from common import COLS, FONT

HERE = Path(__file__).parent
X = np.array([-3, -2.5, -1, 0, 2, 4, 5.0])
PI = np.ones(3) / 3
MU = np.array([-4.0, 0.0, 8.0])
VAR = np.array([1.0, 0.2, 3.0])
wcomp = lambda v: PI * stats.norm(MU, np.sqrt(VAR)).pdf(np.asarray(v)[:, None])
resp = lambda v: wcomp(v) / wcomp(v).sum(axis=1, keepdims=True)
R = resp(X)
assert np.allclose(R.sum(axis=1), 1) and abs(R[2, 1] - 0.943) < 1e-3 and abs(R[4, 2] - 0.934) < 1e-3

g = np.linspace(-6, 10, 600)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.5, 0.5])
fig.add_trace(go.Scatter(x=g, y=wcomp(g).sum(axis=1), mode="lines", line=dict(color="#BBBBBB", width=8),
                         name="mixture"), 1, 1)
for k in range(3):
    fig.add_trace(go.Scatter(x=g, y=wcomp(g)[:, k], mode="lines", line=dict(color=COLS[k], width=3, dash="dash"),
                             name=f"(1/3) × N(x | {MU[k]:g}, {VAR[k]:g})"), 1, 1)
fig.add_trace(go.Scatter(x=X, y=np.zeros_like(X), mode="markers", marker=dict(size=12, color="black"),
                         showlegend=False), 1, 1)
for k in range(3):
    fig.add_trace(go.Scatter(x=g, y=resp(g)[:, k], mode="lines", line=dict(color=COLS[k], width=4),
                             showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=X, y=R[:, k], mode="markers", marker=dict(size=11, color=COLS[k],
                             line=dict(color="black", width=1)), showlegend=False), 2, 1)
fig.update_yaxes(title_text="weighted density", range=[0, 0.32], row=1, col=1)
fig.update_yaxes(title_text="responsibility r<sub>k</sub>(x)", range=[-0.05, 1.05], row=2, col=1)
fig.update_xaxes(title_text="x", row=2, col=1)
fig.update_layout(template="simple_white", width=1000, height=720, font=FONT, legend=dict(x=0.55, y=0.99),
                  margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(HERE / "responsibilities.png", scale=2)
fig.write_image(HERE / "responsibilities.pdf")
print(R.round(3))
