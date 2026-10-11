"""Systematic odometry error, played. The model uses wheel radius 0.05 m for both wheels, but the right wheel is really
0.0505 m (1 percent larger). Both encoders count the same ticks, so odometry's robot (grey) drives straight along x;
the true robot (red) turns left, because its right wheel covers 1 percent more ground. Each frame adds 1 m of ticks;
the gap between the two grows to 2.49 m at 10 m.
Run: python calib_anim.py -> calib_anim.gif, calib_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREY, RED, make_gif
from robotdraw import L, robot

here = Path(__file__).parent


def true_pose(s):
    """True pose after each wheel has rolled s m by its tick count: right 1.01 s, left s; heading turned (dR - dL)/L."""
    th = 0.01 * s / L
    if th == 0:
        return 0.0, 0.0, 0.0
    R = 1.005 * s / th                                   # distance driven over angle turned
    return R * np.sin(th), R * (1 - np.cos(th)), th


S = np.linspace(0, 10, 200)
P = np.array([true_pose(s) for s in S])
X10, Y10, TH10 = true_pose(10)
GAP = lambda s: np.hypot(true_pose(s)[0] - s, true_pose(s)[1])
assert round(TH10, 9) == 0.5 and (round(X10, 2), round(Y10, 2)) == (9.64, 2.46) and round(GAP(10), 2) == 2.49
SC = 2.5                                                 # robots drawn 2.5 times RO-001's size, to be seen at 10 m


def frame(s):
    fig = go.Figure()
    k = S <= s + 1e-9
    fig.add_trace(go.Scatter(x=[0, s], y=[0, 0], mode="lines", line=dict(color=GREY, dash="dash", width=3)))
    fig.add_trace(go.Scatter(x=P[k, 0], y=P[k, 1], mode="lines", line=dict(color=RED, width=3)))
    xt, yt, th = true_pose(s)
    if s > 0:
        fig.add_shape(type="line", x0=s, y0=0, x1=xt, y1=yt, line=dict(color="black", width=1.5, dash="dot"))
    for tr in robot((s, 0, 0), scale=SC, color=GREY, opacity=0.5, fill="rgba(107,107,107,0.15)"):
        fig.add_trace(tr)
    for tr in robot((xt, yt, th), scale=SC, color=RED, fill="rgba(228,87,86,0.18)"):
        fig.add_trace(tr)
    last = s == 10
    fig.add_annotation(x=s + 0.35 if not last else 10, y=-0.6, text=f"odometry says: ({s:.0f}, 0)", showarrow=False,
                       xanchor="right" if last else "center", font=dict(size=19, color=GREY))
    if s > 0:
        fig.add_annotation(x=xt - 0.2, y=yt + 0.65, text=("true end" if last else "true") + f" ({xt:.2f}, {yt:.2f})",
                           showarrow=False, font=dict(size=19, color=RED))
    if last:
        fig.add_annotation(x=10.15, y=1.2, text=f"gap {GAP(10):.2f} m", showarrow=False, xanchor="left",
                           font=dict(size=19))
    fig.update_xaxes(range=[-0.6, 11.6], title="x (m)")
    fig.update_yaxes(range=[-0.9, 3.4], title="y (m)", scaleanchor="x")
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=120, b=70),
                      title=dict(x=0.5, y=0.95, font=dict(size=22),
                                 text="right wheel 1 percent larger than the model thinks: 10 m 'straight'<br>"
                                      f"<span style='font-size:20px'>after {s:.0f} m of ticks: true heading "
                                      f"{th:.2f} rad, gap {GAP(s):.2f} m</span>"))
    return fig


ss = list(range(11))
figs = [frame(s) for s in ss]
holds = [8] + [3] * 9 + [24]
make_gif(figs, here / "calib_anim", fps=4, holds=holds, keys=[5, 10], cols=2, width=950)
