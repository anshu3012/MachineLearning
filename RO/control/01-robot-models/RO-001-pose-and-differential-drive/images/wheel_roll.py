"""A wheel of radius r = 0.05 m rolls one full turn without slipping. The angle turned (radians) times r is the
distance moved: after 2 pi rad = 6.283 rad it has moved 2 pi r = 0.314 m. A rim point (red) traces its path.
Run: python wheel_roll.py -> wheel_roll.gif, wheel_roll_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
r = 0.05
assert abs(2 * np.pi * r - 0.314) < 1e-3


def frame(a):                                                # a: angle turned so far (rad)
    cx = r * a                                               # rolling without slipping: centre moves r * angle
    fig = go.Figure()
    fig.add_shape(type="line", x0=-0.06, x1=0.39, y0=0, y1=0, line=dict(color="black", width=3))
    th = np.linspace(0, 2 * np.pi, 120)
    fig.add_trace(go.Scatter(x=cx + r * np.cos(th), y=r + r * np.sin(th), mode="lines", fill="toself",
                             fillcolor="rgba(76,120,168,0.15)", line=dict(color=BLUE, width=4)))
    s = np.linspace(0, a, 200)                               # path of the rim point, which starts at the bottom
    fig.add_trace(go.Scatter(x=r * s - r * np.sin(s), y=r - r * np.cos(s), mode="lines",
                             line=dict(color=RED, width=2, dash="dot")))
    px, py = cx - r * np.sin(a), r - r * np.cos(a)
    fig.add_trace(go.Scatter(x=[cx, px], y=[r, py], mode="lines", line=dict(color=RED, width=3)))
    fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers", marker=dict(size=14, color=RED)))
    fig.add_trace(go.Scatter(x=[0, cx], y=[-0.012, -0.012], mode="lines", line=dict(color=GREY, width=6)))
    fig.update_xaxes(range=[-0.06, 0.39], title="distance along the floor (m)", dtick=0.05)
    fig.update_yaxes(range=[-0.03, 0.13], visible=False, scaleanchor="x")
    fig.update_layout(template="simple_white", width=1000, height=420, font=FONT, showlegend=False,
                      margin=dict(l=30, r=30, t=110, b=70),
                      title=dict(x=0.5, y=0.93, font=dict(size=23),
                                 text=f"angle turned = {a:.3f} rad<br>distance = r × angle = 0.05 × {a:.3f} = {r * a:.3f} m"))
    return fig


angles = np.linspace(0, 2 * np.pi, 13)
figs = [frame(a) for a in angles]
holds = [5] + [2] * 11 + [18]
make_gif(figs, here / "wheel_roll", fps=6, holds=holds, keys=[6, 12], cols=1, width=900)
