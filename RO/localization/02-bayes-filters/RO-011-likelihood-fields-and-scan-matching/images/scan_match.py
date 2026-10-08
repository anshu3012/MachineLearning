"""Scan matching with a likelihood field. Background: the likelihood field built from the endpoints of scan 1
(taken at (2, 2, 0)); bright = near a scan-1 endpoint. Red: the endpoints of scan 2 (taken at the true pose
(2.3, 2.1, 5 deg)), placed by a candidate motion (dx, dy, dtheta). Each frame is one candidate, starting from the
odometry guess (0.3, 0, 0) and ending at the best of the 21 x 31 x 41 searched, (0.3, 0.1, 5 deg).
Run -> scan_match.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from fieldmodel import ANG72, DTH, DX, DY, POSE_1, POSE_2, endpoints, lookup_fast, match, scan72, scan_field
from gifkit import FONT, RED, make_gif
from fieldmodel import NX, NY, RES, X0, Y0

here = Path(__file__).parent
z1, z2 = scan72(POSE_1, 11), scan72(POSE_2, 12)
F1 = scan_field(z1)
best, S = match(F1, z2)
xs = X0 + (np.arange(NX) + 0.5) * RES
ys = Y0 + (np.arange(NY) + 0.5) * RES
qx, qy = endpoints((0.0, 0.0, 0.0), z2, ANG72)
CANDS = [(0.3, 0.0, 0), (0.1, 0.1, 0), (0.3, 0.1, 0), (0.3, 0.1, 3), (0.3, 0.1, 5)]


def score(dx, dy, dth):
    t = np.radians(dth)
    px = np.cos(t) * qx - np.sin(t) * qy + POSE_1[0] + dx
    py = np.sin(t) * qx + np.cos(t) * qy + POSE_1[1] + dy
    return px, py, np.log(lookup_fast(F1, px, py)).sum()


def frame(c, label):
    px, py, s = score(*c)
    fig = go.Figure(go.Heatmap(x=xs[::3], y=ys[::3], z=F1[::3, ::3], colorscale="Viridis", zmin=0, zmax=3.61,
                               colorbar=dict(title="per m")))
    fig.add_trace(go.Scatter(x=px, y=py, mode="markers", marker=dict(color=RED, size=6)))
    fig.update_layout(template="simple_white", width=900, height=740, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=110, b=60),
                      title=dict(x=0.5, font_size=21, text=f"{label}: move scan 2 by dx = {c[0]:.1f} m, dy = {c[1]:.1f} m,"
                                 f" dθ = {c[2]}°<br>score (sum of log field values) = {s:.0f}"))
    fig.update_xaxes(title="x (m)", range=[-0.2, 5.2], dtick=1, scaleanchor="y")
    fig.update_yaxes(title="y (m)", range=[-0.2, 4.2], dtick=1)
    return fig


labels = ["odometry guess", "candidate", "candidate", "candidate", "best candidate"]
figs = [frame(c, l) for c, l in zip(CANDS, labels)]
make_gif(figs, here / "scan_match", fps=1, holds=[3, 2, 2, 2, 5], keys=[0, len(CANDS) - 1], cols=2, width=800)
assert tuple(round(float(v), 2) for v in best) == (0.3, 0.1, 5.0)
