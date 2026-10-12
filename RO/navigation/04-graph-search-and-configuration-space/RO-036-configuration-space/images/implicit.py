"""Two ways to write the heading while the robot turns from 330 to 30 degrees, 5 degrees per frame. Left: the heading
on a dial and the point (cos theta, sin theta) on the circle x^2 + y^2 = 1. Right: the numbers so far. The explicit
coordinate theta (one number, from 0 to 2 pi) jumps from about 6.28 down to 0 when the heading passes 360 degrees;
the implicit pair (cos theta, sin theta) (two numbers with one rule) changes smoothly.
Run: python implicit.py -> implicit.gif, implicit_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
DEG = np.arange(330, 391, 5)                               # heading, unwrapped, in degrees
assert round(np.radians(359), 3) == 6.266 and round(np.radians(1), 3) == 0.017
assert round(np.cos(np.radians(1)), 4) == 0.9998 and round(np.sin(np.radians(1)), 4) == 0.0175


def frame(k, title):
    fig = make_subplots(rows=2, cols=2, column_widths=[0.38, 0.62], horizontal_spacing=0.1, vertical_spacing=0.2,
                        specs=[[{"rowspan": 2}, {}], [None, {}]],
                        subplot_titles=["the heading on a dial", "explicit: one number θ, from 0 to 2π",
                                        f"implicit: two numbers, <span style='color:{ORANGE}'>cos θ</span> and "
                                        f"<span style='color:{GREEN}'>sin θ</span>, with cos² θ + sin² θ = 1"])
    a = np.linspace(0, 2 * np.pi, 200)
    fig.add_trace(go.Scatter(x=np.cos(a), y=np.sin(a), mode="lines", line=dict(color=GREY, width=2)), 1, 1)
    d = np.radians(DEG[:k + 1])
    fine = np.radians(np.linspace(DEG[0], DEG[k], 10 * k + 2))
    fig.add_trace(go.Scatter(x=np.cos(fine), y=np.sin(fine), mode="lines", line=dict(color=ORANGE, width=6)), 1, 1)
    th = d[-1]
    fig.add_annotation(x=np.cos(th), y=np.sin(th), ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", text="",
                       showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=3, arrowcolor=RED)
    fig.add_trace(go.Scatter(x=[np.cos(th)], y=[np.sin(th)], mode="markers", marker=dict(size=14, color=ORANGE)), 1, 1)
    fig.add_annotation(x=1.05, y=0, text="0° = 360°", showarrow=False, xanchor="left", font=dict(size=18), row=1, col=1)
    fig.add_annotation(x=0, y=-1.32, text=f"(cos θ, sin θ) = ({np.cos(th) + 0:.3f}, {np.sin(th) + 0:.3f})".replace("-0.000", "0.000"), showarrow=False,
                       font=dict(size=19, color=ORANGE), row=1, col=1)
    # the numbers against the heading turned so far
    x = DEG[:k + 1] - 330
    w = np.mod(d, 2 * np.pi)
    xs, ys = [], []
    for j in range(len(w)):
        if j and w[j] < w[j - 1]:
            frac = (360 - DEG[j - 1]) / 5
            xm = x[j - 1] + 5 * frac
            xs += [xm, None, xm]
            ys += [2 * np.pi, None, 0]
            fig.add_trace(go.Scatter(x=[xm, xm], y=[2 * np.pi, 0], mode="lines", line=dict(color=BLUE, width=2,
                                                                                         dash="dot")), 1, 2)
            fig.add_annotation(x=xm, y=3.1, text="  θ jumps by 2π", showarrow=False, xanchor="left",
                               font=dict(size=20, color=BLUE), row=1, col=2)
        xs.append(x[j])
        ys.append(w[j])
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", line=dict(color=BLUE, width=4),
                             marker=dict(size=7)), 1, 2)
    xf = np.linspace(0, x[-1], 10 * k + 2)
    fig.add_trace(go.Scatter(x=xf, y=np.cos(np.radians(330 + xf)), mode="lines", line=dict(color=ORANGE, width=4)), 2, 2)
    fig.add_trace(go.Scatter(x=xf, y=np.sin(np.radians(330 + xf)), mode="lines", line=dict(color=GREEN, width=4)), 2, 2)
    fig.update_xaxes(visible=False, range=[-1.5, 1.9], row=1, col=1)
    fig.update_yaxes(visible=False, range=[-1.45, 1.3], scaleanchor="x", row=1, col=1)
    for r in (1, 2):
        fig.update_xaxes(range=[0, 61], tickvals=[0, 15, 30, 45, 60], ticktext=["330°", "345°", "360°", "15°", "30°"],
                         title="heading" if r == 2 else None, row=r, col=2)
    fig.update_yaxes(range=[-0.4, 6.8], tickvals=[0, np.pi, 2 * np.pi], ticktext=["0", "π", "2π"], row=1, col=2)
    fig.update_yaxes(range=[-1.15, 1.15], tickvals=[-1, 0, 1], ticktext=["−1", "0", "1"], row=2, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=680, showlegend=False,
                      margin=dict(l=20, r=20, t=110, b=60), title=dict(x=0.5, y=0.96, text=title))
    for an in fig.layout.annotations[:3]:
        an.font.size = 20
    return fig


figs, holds = [], []
for k, dg in enumerate(DEG):
    shown = dg % 360
    if dg == 360:
        title = "heading 360° = 0°: θ drops from 2π to 0, while (cos θ, sin θ) moves on smoothly"
        h = 6
    elif k == len(DEG) - 1:
        title = "heading 30°: θ has one jump; cos θ and sin θ have none"
        h = 12
    else:
        title = f"heading {shown}°: θ = {np.radians(shown):.3f} rad"
        h = 4 if k == 0 else 1
    figs.append(frame(k, title))
    holds.append(h)
make_gif(figs, here / "implicit", fps=2, holds=holds, keys=[0, 5, 6, len(DEG) - 1], cols=2, width=950)
