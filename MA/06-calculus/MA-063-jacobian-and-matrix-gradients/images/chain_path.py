"""The multivariable chain rule as a moving point (Plotly frames). f(x, y) = x y^2; the point moves along the path
x(t) = 2t, y(t) = t + 1. Left: the path on the contour map of f. Right: the value f along the path, h(t) = 2t (t + 1)^2.
At t = 1 the point is (2, 2) and f = 8. A step in t splits into a step along x (rate dx/dt = 2) and a step along y
(rate dy/dt = 1). Through x, f changes at 4 x 2 = 8; through y at 8 x 1 = 8; together 16, the slope of h at t = 1.
Idea after Khan Academy, "Multivariable chain rule intuition" (nudge dt -> small move (dx, dy) -> two contributions).
Run: python chain_path.py -> chain_path.gif, chain_path_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREEN, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
f = lambda x, y: x * y ** 2
path = lambda t: (2 * t, t + 1)
h = lambda t: 2 * t * (t + 1) ** 2
assert h(1) == 8 and 4 * 2 + 8 * 1 == 16
assert abs((h(1 + 1e-6) - h(1 - 1e-6)) / 2e-6 - 16) < 1e-6          # the sum is the true slope of h at t = 1
DT = 0.35                                                          # drawn step in t (large, so the arrows show)

gx, gy = np.linspace(0, 3.4, 120), np.linspace(0.6, 2.6, 120)
GX, GY = np.meshgrid(gx, gy)
ts = np.linspace(0, 1.3, 200)


def frame(t, step=0, title=""):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.13, column_widths=[0.55, 0.45],
                        subplot_titles=("the point moves on the map of f (darker = higher)", "the value of f along the path"))
    fig.add_trace(go.Contour(x=gx, y=gy, z=f(GX, GY), contours=dict(start=2, end=20, size=2, coloring="lines"),
                             line=dict(width=1.5), colorscale=[[0, "#9ecae1"], [1, "#08519c"]], showscale=False),
                  row=1, col=1)
    px, py = path(ts)
    fig.add_trace(go.Scatter(x=px, y=py, mode="lines", line=dict(color=GREY, width=3, dash="dot")), row=1, col=1)
    x, y = path(t)
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=16, color="black")), row=1, col=1)
    fig.add_trace(go.Scatter(x=ts, y=h(ts), mode="lines", line=dict(color=GREY, width=3)), row=1, col=2)
    fig.add_trace(go.Scatter(x=[t], y=[h(t)], mode="markers", marker=dict(size=16, color="black")), row=1, col=2)
    arrows = []
    if step >= 1:                                                  # the x part of the step: dx = 2 dt
        arrows.append(dict(x=x + 2 * DT, y=y, ax=x, ay=y, color=ORANGE, text="x part"))
    if step >= 2:                                                  # the y part: dy = 1 dt
        arrows.append(dict(x=x + 2 * DT, y=y + DT, ax=x + 2 * DT, ay=y, color=PURPLE, text="y part"))
    for a in arrows:
        fig.add_annotation(x=a["x"], y=a["y"], ax=a["ax"], ay=a["ay"], xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowwidth=5, arrowsize=1, arrowcolor=a["color"], text="")
        fig.add_annotation(x=(a["x"] + a["ax"]) / 2 + (0.0 if a["text"] == "x part" else 0.45),
                           y=(a["y"] + a["ay"]) / 2 + (-0.13 if a["text"] == "x part" else 0.0), xref="x", yref="y",
                           text=f"<b>{a['text']}</b>", showarrow=False, font=dict(size=20, color=a["color"]))
    if step >= 3:                                                  # tangent of h at t = 1: slope 16
        tt = np.array([0.75, 1.25])
        fig.add_trace(go.Scatter(x=tt, y=8 + 16 * (tt - 1), mode="lines", line=dict(color=GREEN, width=5)), row=1, col=2)
        fig.add_annotation(x=0.95, y=14.5, xref="x2", yref="y2", text="<b>slope 16</b>", showarrow=False,
                           font=dict(size=22, color=GREEN))
    fig.update_xaxes(title="x", range=[0, 3.4], dtick=1, row=1, col=1)
    fig.update_yaxes(title="y", range=[0.6, 2.6], dtick=0.5, row=1, col=1)
    fig.update_xaxes(title="t", range=[0, 1.3], dtick=0.25, row=1, col=2)
    fig.update_yaxes(title="f", range=[0, 18], dtick=4, row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=580, font=FONT, showlegend=False,
                      margin=dict(l=70, r=25, t=135, b=65),
                      title=dict(x=0.5, y=0.965, font=dict(size=23), text=title))
    fig.update_annotations(selector=dict(text="the point moves on the map of f (darker = higher)"), font_size=21)
    fig.update_annotations(selector=dict(text="the value of f along the path"), font_size=21)
    return fig


figs, holds, keys = [], [], []
for t in (0.25, 0.4, 0.55, 0.7, 0.85, 1.0):
    x, y = path(t)
    figs.append(frame(t, 0, f"t = {t:g}:  x = 2t = {x:g},  y = t + 1 = {y:g}<br>f = x·y² = {f(x, y):.2f}"))
    holds.append(3 if t < 1 else 10)
keys.append(len(figs) - 1)
figs.append(frame(1, 1, "Through x:  x moves 2 per unit of t,  f rises 4 per unit of x<br>"
                        "effect through x = 4 × 2 = <b>8</b>"))
holds.append(14)
keys.append(len(figs) - 1)
figs.append(frame(1, 2, "Through y:  y moves 1 per unit of t,  f rises 8 per unit of y<br>"
                        "effect through y = 8 × 1 = <b>8</b>"))
holds.append(14)
keys.append(len(figs) - 1)
figs.append(frame(1, 3, "Add the two effects:  8 + 8 = <b>16</b><br>"
                        "= the slope of f along the path at t = 1"))
holds.append(20)
keys.append(len(figs) - 1)
make_gif(figs, here / "chain_path", fps=6, holds=holds, keys=[keys[1], keys[3]], cols=1, width=1000)
