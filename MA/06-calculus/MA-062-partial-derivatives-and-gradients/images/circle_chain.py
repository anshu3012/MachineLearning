"""The multivariable chain rule on a circle (Plotly frames). The bowl f(x1, x2) = x1^2 + x1 x2 + 2 x2^2; the point moves
around the unit circle x1 = cos t, x2 = sin t. Left: the path on the contour map. Right: the value of f along the path,
f(t) = 1 + sin^2 t + (1/2) sin 2t. At t = 0 and t = pi/2 the step in t splits into an x1 part and an x2 part:
t = 0:    gradient [2, 1], velocity [0, 1]  -> 2 x 0 + 1 x 1 = 1
t = pi/2: gradient [1, 4], velocity [-1, 0] -> 1 x (-1) + 4 x 0 = -1
Idea after Khan Academy, "Multivariable chain rule" and "Multivariable chain rule intuition"; our own function.
Run: python circle_chain.py -> circle_chain.gif, circle_chain_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREEN, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
f = lambda a, b: a ** 2 + a * b + 2 * b ** 2
ft = lambda t: f(np.cos(t), np.sin(t))
dft = lambda t: np.sin(2 * t) + np.cos(2 * t)
for t, want in ((0, 1), (np.pi / 2, -1)):                          # the sums in the Note are the true slopes
    assert abs((ft(t + 1e-6) - ft(t - 1e-6)) / 2e-6 - want) < 1e-6 and abs(dft(t) - want) < 1e-12
S = 0.45                                                           # drawn length of a unit rate

g = np.linspace(-1.6, 1.6, 120)
GX, GY = np.meshgrid(g, g)
ts = np.linspace(0, 2 * np.pi, 300)


def frame(t, parts=(), slope=None, title=""):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, column_widths=[0.5, 0.5],
                        subplot_titles=("the point goes round the circle (darker = higher)", "the value of f along the path"))
    fig.add_trace(go.Contour(x=g, y=g, z=f(GX, GY), contours=dict(start=0.25, end=8, size=0.75, coloring="lines"),
                             line=dict(width=1.5), colorscale=[[0, "#9ecae1"], [1, "#08519c"]], showscale=False),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=np.cos(ts), y=np.sin(ts), mode="lines", line=dict(color=GREY, width=3, dash="dot")),
                  row=1, col=1)
    x, y = np.cos(t), np.sin(t)
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=16, color="black")), row=1, col=1)
    fig.add_trace(go.Scatter(x=ts, y=ft(ts), mode="lines", line=dict(color=GREY, width=3)), row=1, col=2)
    fig.add_trace(go.Scatter(x=[t], y=[ft(t)], mode="markers", marker=dict(size=16, color="black")), row=1, col=2)
    for name, dx, dy, color in parts:                              # x1 part then x2 part, tip to tail
        x0, y0 = (x, y) if name == "x1 part" else (x + S * (-np.sin(t)), y)
        fig.add_annotation(x=x0 + S * dx, y=y0 + S * dy, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowwidth=5, arrowsize=1, arrowcolor=color, text="")
        fig.add_annotation(x=x0 + S * dx / 2 + (0.0 if dx else 0.35), y=y0 + S * dy / 2 + (-0.17 if dx else 0.0),
                           xref="x", yref="y", text=f"<b>{name}</b>", showarrow=False, bgcolor="rgba(255,255,255,0.85)",
                           font=dict(size=20, color=color))
    if slope is not None:
        tt = np.array([t - 0.6, t + 0.6])
        fig.add_trace(go.Scatter(x=tt, y=ft(t) + slope * (tt - t), mode="lines", line=dict(color=GREEN, width=5)),
                      row=1, col=2)
        fig.add_annotation(x=0.9 if t == 0 else 2.6, y=1.0 if t == 0 else 2.6, xref="x2", yref="y2", text=f"<b>slope {slope:g}</b>",
                           showarrow=False, font=dict(size=22, color=GREEN))
    fig.update_xaxes(title="x1", range=[-1.6, 1.6], dtick=0.5, row=1, col=1)
    fig.update_yaxes(title="x2", range=[-1.6, 1.6], dtick=0.5, scaleanchor="x", row=1, col=1)
    fig.update_xaxes(title="t", range=[0, 2 * np.pi], tickvals=[0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi],
                     ticktext=["0", "π/2", "π", "3π/2", "2π"], row=1, col=2)
    fig.update_yaxes(title="f", range=[0, 3], dtick=0.5, row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=600, font=FONT, showlegend=False,
                      margin=dict(l=70, r=25, t=135, b=65), title=dict(x=0.5, y=0.965, font=dict(size=23), text=title))
    for txt in ("the point goes round the circle (darker = higher)", "the value of f along the path"):
        fig.update_annotations(selector=dict(text=txt), font_size=20)
    return fig


figs, holds, keys = [], [], []
def add(fig, hold, key=False):
    figs.append(fig); holds.append(hold)
    if key:
        keys.append(len(figs) - 1)

add(frame(0, title="t = 0:  the point is (1, 0),  f = 1"), 10)
add(frame(0, [("x2 part", 0, 1, PURPLE)],
          title="t = 0:  x1 moves 0, x2 moves 1 per unit of t;  gradient [2, 1]<br>"
                "2 × 0 = 0,   1 × 1 = 1,   sum 0 + 1 = <b>1</b>"), 6)
add(frame(0, [("x2 part", 0, 1, PURPLE)], slope=1,
          title="t = 0:  x1 moves 0, x2 moves 1 per unit of t;  gradient [2, 1]<br>"
                "2 × 0 = 0,   1 × 1 = 1,   sum 0 + 1 = <b>1</b>"), 16, key=True)
for t in np.linspace(0.2, np.pi / 2 - 0.2, 6):
    add(frame(t, title=f"t = {t:.2f}:  point ({np.cos(t):.2f}, {np.sin(t):.2f}),  f = {ft(t):.2f}"), 3)
add(frame(np.pi / 2, title="t = π/2:  the point is (0, 1),  f = 2"), 8)
add(frame(np.pi / 2, [("x1 part", -1, 0, ORANGE)],
          title="t = π/2:  x1 moves −1, x2 moves 0 per unit of t;  gradient [1, 4]<br>"
                "1 × (−1) = −1,   4 × 0 = 0,   sum −1 + 0 = <b>−1</b>"), 6)
add(frame(np.pi / 2, [("x1 part", -1, 0, ORANGE)], slope=-1,
          title="t = π/2:  x1 moves −1, x2 moves 0 per unit of t;  gradient [1, 4]<br>"
                "1 × (−1) = −1,   4 × 0 = 0,   sum −1 + 0 = <b>−1</b>"), 20, key=True)
make_gif(figs, here / "circle_chain", fps=6, holds=holds, keys=keys, cols=1, width=1000)
