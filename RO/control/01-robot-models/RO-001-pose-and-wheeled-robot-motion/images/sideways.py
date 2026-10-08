"""Moving sideways with legal moves only: from pose (0, 0, 0) spin 90 deg left on the spot, drive 0.5 m forward,
spin 90 deg right. The robot ends at (0, 0.5, 0): 0.5 m to its left, same heading. Faint: the start pose.
Run: python sideways.py -> sideways.gif, sideways_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREY, make_gif
from robotdraw import robot

here = Path(__file__).parent
STAGES = [("1. spin 90° left on the spot (v = 0)", lambda s: (0, 0, s * np.pi / 2)),
          ("2. drive 0.5 m forward (ω = 0)", lambda s: (0, 0.5 * s, np.pi / 2)),
          ("3. spin 90° right on the spot (v = 0)", lambda s: (0, 0.5, np.pi / 2 * (1 - s)))]
assert np.allclose(STAGES[2][1](1), (0, 0.5, 0))


def frame(stage, s):
    fig = go.Figure()
    for tr in robot((0, 0, 0), scale=1.5, opacity=0.25):
        fig.add_trace(tr)
    if stage >= 1:
        y_end = 0.5 * s if stage == 1 else 0.5
        fig.add_trace(go.Scatter(x=[0, 0], y=[0, y_end], mode="lines", line=dict(color=GREY, width=3, dash="dot")))
    for tr in robot(STAGES[stage][1](s), scale=1.5):
        fig.add_trace(tr)
    fig.update_xaxes(range=[-0.6, 0.6], dtick=0.25, title="x (m)", showgrid=True, gridcolor="#eee")
    fig.update_yaxes(range=[-0.35, 0.85], dtick=0.25, title="y (m)", showgrid=True, gridcolor="#eee", scaleanchor="x")
    x, y, th = STAGES[stage][1](s)
    fig.update_layout(template="simple_white", width=800, height=860, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=120, b=70),
                      title=dict(x=0.5, y=0.95, font=dict(size=23),
                                 text=f"{STAGES[stage][0]}<br>pose = ({x:.2f}, {y:.2f}, {np.degrees(th):.0f}°)"))
    return fig


figs, holds, keys = [], [], []
for st in range(3):
    for s in np.linspace(0, 1, 7)[(1 if st else 0):]:
        figs.append(frame(st, s))
        holds.append(2)
    holds[-1] = 10
    keys.append(len(figs) - 1)
holds[-1] = 20
make_gif(figs, here / "sideways", fps=6, holds=holds, keys=[3] + keys, cols=2, width=800)
