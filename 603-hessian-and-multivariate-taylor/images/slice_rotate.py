"""Slicing a saddle in every direction (Plotly frames: a 3-D surface plus a chart). f = x^2 - y^2 is cut by a vertical
plane through the origin at angle theta to the x-axis. The slice is the parabola f = cos(2 theta) s^2, so its second
derivative is 2 cos(2 theta): +2 along x (curves up), 0 on the diagonal (flat), -2 along y (curves down).
Idea after Khan Academy, "Saddle points". Run: python slice_rotate.py -> slice_rotate.gif, slice_rotate_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
f = lambda x, y: x ** 2 - y ** 2
g = np.linspace(-1.5, 1.5, 50)
X, Y = np.meshgrid(g, g)
s = np.linspace(-1.5, 1.5, 80)
curv = lambda deg: 2 * np.cos(2 * np.radians(deg))
h = 1e-3                                             # the formula against a numerical second derivative, at 30 degrees
c, sn = np.cos(np.radians(30)), np.sin(np.radians(30))
assert abs((f(h * c, h * sn) - 2 * f(0, 0) + f(-h * c, -h * sn)) / h ** 2 - curv(30)) < 1e-6
angles = list(range(0, 181, 15))


def frame(k):
    deg = angles[k]
    t = np.radians(deg)
    xs, ys = s * np.cos(t), s * np.sin(t)
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "scene"}, {"type": "xy"}]], column_widths=[0.56, 0.44],
                        horizontal_spacing=0.06)
    fig.add_trace(go.Surface(x=X, y=Y, z=f(X, Y), colorscale="Blues", reversescale=True, showscale=False, opacity=0.55), row=1, col=1)
    fig.add_trace(go.Scatter3d(x=xs, y=ys, z=f(xs, ys), mode="lines", line=dict(color=RED, width=10)), row=1, col=1)
    fig.add_trace(go.Scatter3d(x=xs, y=ys, z=0 * s - 2.6, mode="lines", line=dict(color=GREY, width=5, dash="dash")), row=1, col=1)
    dense = np.linspace(0, 180, 181)
    fig.add_trace(go.Scatter(x=dense, y=curv(dense), line=dict(color="#CCCCCC", width=2, dash="dot")), row=1, col=2)
    fig.add_trace(go.Scatter(x=dense[:deg + 1], y=curv(dense[:deg + 1]), line=dict(color=BLUE, width=5)), row=1, col=2)
    fig.add_trace(go.Scatter(x=[deg], y=[curv(deg)], mode="markers", marker=dict(size=16, color=RED)), row=1, col=2)
    fig.update_xaxes(title="direction of the slice θ (degrees)", range=[-5, 185], tickvals=[0, 45, 90, 135, 180], row=1, col=2)
    fig.update_yaxes(title="second derivative of the slice", range=[-2.5, 2.5], zeroline=True, zerolinecolor="#999999", row=1, col=2)
    tick = dict(tickfont=dict(size=14))
    fig.update_scenes(xaxis=dict(title="x", nticks=4, **tick), yaxis=dict(title="y", nticks=4, **tick),
                      zaxis=dict(title="f", range=[-2.6, 2.6], nticks=4, **tick), aspectmode="manual",
                      aspectratio=dict(x=1, y=1, z=0.8), camera=dict(eye=dict(x=1.5, y=-1.35, z=0.8), center=dict(x=0, y=0, z=-0.1)))
    v = round(float(curv(deg)), 6) + 0.0
    kind = "the slice curves up" if v > 0.01 else "the slice curves down" if v < -0.01 else "the slice is flat"
    fig.update_layout(template="simple_white", width=1100, height=600, font=FONT, showlegend=False,
                      margin=dict(l=0, r=20, t=95, b=65),
                      title=dict(x=0.5, y=0.96, font=dict(size=22),
                                 text=f"f = x² − y² cut along the direction θ = {deg}°<br>"
                                      f"second derivative of the slice = 2·cos(2θ) = <b>{v:.1f}</b>:  {kind}"))
    return fig


figs = [frame(k) for k in range(len(angles))]
holds = [10 if a in (0, 45, 90) else 12 if a == 180 else 3 for a in angles]
make_gif(figs, here / "slice_rotate", fps=6, holds=holds, keys=[0, angles.index(45), angles.index(90), angles.index(135)], width=1000)
