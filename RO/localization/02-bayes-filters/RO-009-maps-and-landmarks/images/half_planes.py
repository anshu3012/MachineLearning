"""The table as the intersection of four half-planes. Each frame shades one more half-plane f_i(x, y) <= 0; grey: the region inside all
half-planes so far; the last one is the table. Last frame: the test points (4, 2), inside, and (5.5, 1.5), outside because
f_2 = 1 > 0. Run: python half_planes.py -> half_planes.gif, half_planes_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from roommap import TABLE, TABLE_F, f_table

here = Path(__file__).parent
names = ["f₁ = 1 − y", "f₂ = 3x − y − 14", "f₃ = 2x + 8y − 31", "f₄ = 11 − 4x + y"]
cols = [BLUE, ORANGE, GREEN, PURPLE]
assert f_table(4, 2) == [-1, -4, -7, -3] and f_table(5.5, 1.5)[1] == 1.0


BOX = [(2, 0), (6.5, 0), (6.5, 4), (2, 4)]


def clip(poly, abc):
    """Keep the part of a polygon where a x + b y + c <= 0 (one Sutherland-Hodgman pass)."""
    a, b, c = abc
    f = lambda p: a * p[0] + b * p[1] + c
    out = []
    for i, p in enumerate(poly):
        q = poly[(i + 1) % len(poly)]
        if f(p) <= 0:
            out.append(p)
        if f(p) * f(q) < 0:
            t = f(p) / (f(p) - f(q))
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def shade(fig, poly, color, opacity):
    px, py = zip(*(poly + [poly[0]]))
    fig.add_trace(go.Scatter(x=px, y=py, fill="toself", mode="lines", line=dict(width=0), fillcolor=color,
                             opacity=opacity))


def frame(k, test=False):
    fig = go.Figure()
    if k:
        shade(fig, clip(BOX, TABLE_F[k - 1]), cols[k - 1], 0.25)          # the newest half-plane
        region = BOX
        for i in range(k):
            region = clip(region, TABLE_F[i])
        shade(fig, region, GREY, 0.35)                                      # inside all half-planes so far
    for i in range(k):
        a, b, c = TABLE_F[i]
        if b != 0:
            lx = np.array([2, 6.5])
            fig.add_trace(go.Scatter(x=lx, y=-(a * lx + c) / b, mode="lines", line=dict(color=cols[i], width=3)))
        else:
            fig.add_trace(go.Scatter(x=[-c / a] * 2, y=[0, 4], mode="lines", line=dict(color=cols[i], width=3)))
    if k == 4:
        px, py = zip(*(TABLE + [TABLE[0]]))
        fig.add_trace(go.Scatter(x=px, y=py, mode="lines", line=dict(color="black", width=4)))
    if test:
        fig.add_trace(go.Scatter(x=[4, 5.5], y=[2, 1.5], mode="markers+text", marker=dict(size=14, color=[GREEN, RED]),
                                 text=["(4, 2): all four ≤ 0, inside", "(5.5, 1.5): f₂ = 1 > 0, outside"],
                                 textposition=["top center", "bottom center"], textfont=dict(size=17)))
    title = ("table = where all four are ≤ 0" if k == 4 else
             f"half-plane {k}: {names[k - 1]} ≤ 0" if k else "the table's four edges, one half-plane each")
    fig.update_xaxes(range=[2, 6.5], dtick=0.5, title="x (m)")
    fig.update_yaxes(range=[0, 4], dtick=0.5, title="y (m)", scaleanchor="x")
    fig.update_layout(template="simple_white", width=820, height=800, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=100, b=70),
                      title=dict(text=title, x=0.5, y=0.95, font=dict(size=22)))
    if 0 < k:
        fig.add_annotation(x=2.1, y=3.85, xanchor="left", showarrow=False, align="left", font=dict(size=17),
                           text="<br>".join(f"<span style='color:{cols[i]}'>{names[i]} ≤ 0</span>" for i in range(k)))
    return fig


figs = [frame(k) for k in range(5)] + [frame(4, test=True)]
make_gif(figs, here / "half_planes", fps=1, holds=[2, 3, 3, 3, 3, 6], keys=[1, 2, 4, 5], cols=2, width=800)
