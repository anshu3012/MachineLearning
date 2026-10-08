"""Sampling the odometry motion model step after step, with no readings: 500 samples start on the pose (2, 1, 30 deg)
and each step applies the odometry u = (0.1 rad, 0.3 m, 0.1 rad) with the Note's noise. The cloud grows and bends.
Seeded. Run: python spread.py -> spread.gif, spread_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED, make_gif
from motion import START, sample_odometry

here = Path(__file__).parent
u = (0.1, 0.3, 0.1)
rng = np.random.default_rng(11)
n = 500
clouds = [tuple(np.full(n, v) for v in START)]
nominal = [START]
for _ in range(8):
    clouds.append(sample_odometry(u, clouds[-1], rng, n))
    x, y, th = nominal[-1]
    nominal.append((x + u[1] * np.cos(th + u[0]), y + u[1] * np.sin(th + u[0]), th + u[0] + u[2]))
nom = np.array(nominal)
spread = [np.sqrt(np.var(c[0]) + np.var(c[1])) for c in clouds]


def frame(k):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=nom[:, 0], y=nom[:, 1], mode="lines+markers", line=dict(color=GREY, dash="dash", width=2),
                             marker=dict(size=7, color=GREY)))
    fig.add_trace(go.Scatter(x=clouds[k][0], y=clouds[k][1], mode="markers",
                             marker=dict(size=4, color=BLUE, opacity=0.6)))
    fig.add_trace(go.Scatter(x=[nom[k, 0]], y=[nom[k, 1]], mode="markers", marker=dict(size=13, color=RED, symbol="x")))
    fig.update_xaxes(range=[0.6, 3.0], dtick=0.5, title="x (m)", showgrid=True, gridcolor="#eee")
    fig.update_yaxes(range=[0.8, 3.4], dtick=0.5, title="y (m)", showgrid=True, gridcolor="#eee", scaleanchor="x")
    fig.update_layout(template="simple_white", width=820, height=860, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=110, b=70),
                      title=dict(x=0.5, y=0.95, font=dict(size=22),
                                 text=f"after {k} step{'s' if k != 1 else ''} with no readings: "
                                      f"spread {spread[k]:.3f} m<br>grey: odometry's path, blue: 500 samples"))
    return fig


figs = [frame(k) for k in range(9)]
make_gif(figs, here / "spread", fps=1, holds=[2, 2, 2, 2, 1, 1, 1, 1, 4], keys=[1, 4, 8], cols=3, width=800)
print([round(s, 3) for s in spread])
