"""A car pulling one trailer (hitch length d1 = 2 m), driving straight (omega = 0) from the same start: car heading
40 deg, trailer heading 10 deg. Trailer: theta1' = (v / d1) sin(theta0 - theta1) (LaValle eq. 13.19).
Forward (v = 1 m/s): the angle between them shrinks to 0. Reverse (v = -1 m/s): it grows (jackknifing).
Run: python trailer_drive.py -> trailer_drive.gif, trailer_drive_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, PURPLE, make_gif

here = Path(__file__).parent
d1, dt = 2.0, 0.01
th0 = np.radians(40)
assert abs(1 / d1 * np.sin(np.radians(30)) - 0.25) < 1e-12


def run(v, T):
    x, y, th1, out = 0.0, 0.0, np.radians(10), []
    for k in range(round(T / dt) + 1):
        out.append((k * dt, x, y, th1))
        th1 += v / d1 * np.sin(th0 - th1) * dt
        x, y = x + v * np.cos(th0) * dt, y + v * np.sin(th0) * dt
    return np.array(out)


fwd, rev = run(1.0, 6.0), run(-1.0, 2.6)


def rect(cx, cy, th, lb, lf, hw):                            # rectangle from lb behind to lf ahead of (cx, cy)
    p = np.array([(-lb, -hw), (lf, -hw), (lf, hw), (-lb, hw), (-lb, -hw)])
    c, s = np.cos(th), np.sin(th)
    return cx + c * p[:, 0] - s * p[:, 1], cy + s * p[:, 0] + c * p[:, 1]


def draw(fig, st, col):
    t, x, y, th1 = st
    tx, ty = x - d1 * np.cos(th1), y - d1 * np.sin(th1)      # middle of the trailer's axle
    for (px, py), color, fc in [(rect(x, y, th0, 0.5, 3.2, 0.8), BLUE, "rgba(76,120,168,0.2)"),
                                (rect(tx, ty, th1, 1.0, 1.0, 0.7), PURPLE, "rgba(178,121,162,0.2)")]:
        fig.add_trace(go.Scatter(x=px, y=py, mode="lines", fill="toself", line=dict(color=color, width=3),
                                 fillcolor=fc), row=1, col=col)
    fig.add_trace(go.Scatter(x=[tx, x], y=[ty, y], mode="lines+markers", line=dict(color="black", width=3),
                             marker=dict(size=8, color="black")), row=1, col=col)


def frame(i, j):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                        subplot_titles=[f"<b>forward, v = +1 m/s</b><br>t = {fwd[i, 0]:.1f} s, angle between = "
                                        f"{np.degrees(th0 - fwd[i, 3]):.0f}°",
                                        f"<b>reverse, v = −1 m/s</b><br>t = {rev[j, 0]:.1f} s, angle between = "
                                        f"{np.degrees(th0 - rev[j, 3]):.0f}°"])
    for col, run_, k in ((1, fwd, i), (2, rev, j)):
        fig.add_trace(go.Scatter(x=run_[:k + 1, 1], y=run_[:k + 1, 2], mode="lines",
                                 line=dict(color=GREY, width=2, dash="dot")), row=1, col=col)
        draw(fig, run_[k], col)
    fig.update_xaxes(range=[-6, 8], dtick=2, title="x (m)", showgrid=True, gridcolor="#eee", row=1, col=1)
    fig.update_yaxes(range=[-4, 7], dtick=2, title="y (m)", showgrid=True, gridcolor="#eee", scaleanchor="x", row=1, col=1)
    fig.update_xaxes(range=[-7, 5], dtick=2, title="x (m)", showgrid=True, gridcolor="#eee", row=1, col=2)
    fig.update_yaxes(range=[-6, 5], dtick=2, showgrid=True, gridcolor="#eee", scaleanchor="x2", row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=640, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=120, b=60))
    fig.update_annotations(font_size=21)
    return fig


n = 10
idx_f = np.linspace(0, len(fwd) - 1, n).round().astype(int)
idx_r = np.linspace(0, len(rev) - 1, n).round().astype(int)
figs = [frame(i, j) for i, j in zip(idx_f, idx_r)]
holds = [8] + [3] * (n - 2) + [20]
make_gif(figs, here / "trailer_drive", fps=6, holds=holds, keys=[0, n - 1], cols=1, width=1000)
print(f"forward end angle {np.degrees(th0 - fwd[-1, 3]):.1f}, reverse end angle {np.degrees(th0 - rev[-1, 3]):.1f}")
