"""Euler steps of the kinematic model from pose (2, 1, 30 deg) with v = 0.5 m/s, omega = 1 rad/s, dt = 0.1 s.
Dots: the pose after each step. Dashed: the true circle, centre (1.75, 1.433), radius v/omega = 0.5 m.
After 63 steps (6.3 s) the path has closed the circle. Run: python euler_path.py -> euler_path.gif, euler_path_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREY, RED, make_gif
from robotdraw import robot, step

here = Path(__file__).parent
v, w, dt = 0.5, 1.0, 0.1
qs = [(2.0, 1.0, np.radians(30))]
for _ in range(63):
    qs.append(step(qs[-1], v, w, dt))
qs = np.array(qs)
assert np.allclose(qs[1], [2.0433, 1.0250, 0.6236], atol=5e-5) and np.allclose(qs[2], [2.0839, 1.0542, 0.7236], atol=5e-5)
cx, cy = 2 - 0.5 * np.sin(np.radians(30)), 1 + 0.5 * np.cos(np.radians(30))


def frame(k):
    fig = go.Figure()
    t = np.linspace(0, 2 * np.pi, 200)
    fig.add_trace(go.Scatter(x=cx + 0.5 * np.cos(t), y=cy + 0.5 * np.sin(t), mode="lines",
                             line=dict(color=GREY, width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=qs[:k + 1, 0], y=qs[:k + 1, 1], mode="lines+markers",
                             line=dict(color=RED, width=2), marker=dict(size=7, color=RED)))
    for tr in robot(tuple(qs[k])):
        fig.add_trace(tr)
    x, y, th = qs[k]
    fig.update_xaxes(range=[1.05, 2.55], dtick=0.25, title="x (m)", showgrid=True, gridcolor="#eee")
    fig.update_yaxes(range=[0.75, 2.1], dtick=0.25, title="y (m)", showgrid=True, gridcolor="#eee", scaleanchor="x")
    fig.update_layout(template="simple_white", width=900, height=860, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=120, b=70),
                      title=dict(x=0.5, y=0.95, font=dict(size=23),
                                 text=f"step {k}  (t = {k * dt:.1f} s):  x = {x:.3f},  y = {y:.3f},  θ = {th:.2f} rad"
                                      "<br>red dots: Euler steps of 0.1 s   dashed: true circle"))
    return fig


ks = [0, 1, 2, 5, 10, 16, 23, 31, 40, 50, 63]
figs = [frame(k) for k in ks]
holds = [6, 6, 6] + [3] * (len(ks) - 4) + [18]
make_gif(figs, here / "euler_path", fps=6, holds=holds, keys=[2, len(ks) - 1], cols=2, width=900)
