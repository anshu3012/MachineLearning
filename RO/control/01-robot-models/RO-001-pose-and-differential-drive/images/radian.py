"""What a radian is. A string as long as the radius is bent onto the circle: the angle it covers is 1 radian
(57.3 deg). Laying radius-long pieces round the circle, a full turn takes 2 pi = 6.283 of them, so a full turn is
2 pi rad and an arc is always radius x angle. Run: python radian.py -> radian.gif, radian_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
assert abs(np.degrees(1) - 57.2958) < 1e-4


def frame(a, straight=0.0, title=""):
    """a: angle covered on the rim (rad). straight: part (0..1) of a radius-long string still straight, drawn upright."""
    fig = go.Figure()
    t = np.linspace(0, 2 * np.pi, 300)
    fig.add_trace(go.Scatter(x=np.cos(t), y=np.sin(t), mode="lines", line=dict(color=GREY, width=2)))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 0], mode="lines", line=dict(color=BLUE, width=5)))
    fig.add_annotation(x=0.5, y=-0.09, text="radius = 1", showarrow=False, font=dict(color=BLUE, size=22))
    s = np.linspace(0, a, 200)
    fig.add_trace(go.Scatter(x=np.cos(s), y=np.sin(s), mode="lines", line=dict(color=RED, width=7)))
    if straight > 0:                                         # rest of the string, still straight, tangent at the rim
        e = a
        fig.add_trace(go.Scatter(x=[np.cos(e), np.cos(e) - straight * np.sin(e)],
                                 y=[np.sin(e), np.sin(e) + straight * np.cos(e)], mode="lines",
                                 line=dict(color=RED, width=7)))
    if a > 0:
        fig.add_trace(go.Scatter(x=[0, np.cos(a)], y=[0, np.sin(a)], mode="lines", line=dict(color=ORANGE, width=3,
                                                                                            dash="dot")))
        w = np.linspace(0, a, 100)
        fig.add_trace(go.Scatter(x=0.25 * np.cos(w), y=0.25 * np.sin(w), mode="lines", line=dict(color=ORANGE, width=3)))
    for k in range(1, int(a + 1e-9) + 1):                    # one tick per whole radian laid down
        fig.add_trace(go.Scatter(x=[0.92 * np.cos(k), 1.08 * np.cos(k)], y=[0.92 * np.sin(k), 1.08 * np.sin(k)],
                                 mode="lines", line=dict(color="black", width=3)))
        fig.add_annotation(x=1.2 * np.cos(k), y=1.2 * np.sin(k), text=str(k), showarrow=False, font=dict(size=20))
    fig.update_xaxes(range=[-1.45, 1.45], visible=False)
    fig.update_yaxes(range=[-1.35, 1.45], visible=False, scaleanchor="x")
    fig.update_layout(template="simple_white", width=760, height=820, font=FONT, showlegend=False,
                      margin=dict(l=10, r=10, t=120, b=10),
                      title=dict(x=0.5, y=0.96, font=dict(size=23), text=title))
    return fig


figs, holds = [], []
for p in np.linspace(0, 1, 7):                               # bend one radius-long string onto the rim
    figs.append(frame(p, 1 - p, "bend a string as long as the radius onto the circle"))
    holds.append(2)
figs.append(frame(1.0, 0, "it covers an angle of 1 radian (57.3°)<br>arc = radius × 1"))
holds.append(14)
for a in (2, 3, 4, 5, 6, 2 * np.pi):
    txt = f"{a:.0f} radius-lengths: {a:.0f} rad" if a < 6.2 else "a full turn takes 6.283 radius-lengths<br>full turn = 2π rad = 6.283 rad"
    figs.append(frame(a, 0, txt))
    holds.append(5 if a < 6.2 else 20)
make_gif(figs, here / "radian", fps=6, holds=holds, keys=[7, len(figs) - 1], cols=2, width=700)
