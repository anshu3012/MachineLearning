"""Block-diagram algebra on the PID heading loop, one move per frame (Kp = Kd = 0.4, the robot 1 / (0.1 s^2) = 10 / s^2,
the D part on the measured turn, Ki left as a symbol).
0: the loop. 1: the P and I blocks are in parallel, so they add: 0.4 + Ki/s = (0.4 s + Ki)/s.
2: the inner loop (robot with the D feedback) becomes forward / (1 + loop) = 10 / (s^2 + 4 s).
3: the two blocks in series multiply: (4 s + 10 Ki) / (s^3 + 4 s^2).
4: the outer loop: (4 s + 10 Ki) / (s^3 + 4 s^2 + 4 s + 10 Ki).
Run: python blocks_anim.py -> blocks_anim.gif, blocks_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent

# check each move with numbers at s = 1 and Ki = 0.2 (any test point would do)
s, ki = 1.0, 0.2
c, p, h = 0.4 + ki / s, 10 / s ** 2, 0.4 * s
inner = p / (1 + h * p)
assert abs(c - (0.4 * s + ki) / s) < 1e-12 and abs(inner - 10 / (s ** 2 + 4 * s)) < 1e-12
fwd = c * inner
assert abs(fwd - (4 * s + 10 * ki) / (s ** 3 + 4 * s ** 2)) < 1e-12
assert abs(fwd / (1 + fwd) - (4 * s + 10 * ki) / (s ** 3 + 4 * s ** 2 + 4 * s + 10 * ki)) < 1e-12

FRAMES = [
    ("the PID heading loop", None),
    ("move 1: parallel blocks add", "0.4 + Ki/s = (0.4 s + Ki) / s"),
    ("move 2: a loop is forward ÷ (1 + loop)", "(10/s²) ÷ (1 + 0.4 s · 10/s²) = 10 / (s² + 4 s)"),
    ("move 3: series blocks multiply", "(0.4 s + Ki)/s · 10/(s² + 4 s) = (4 s + 10 Ki) / (s³ + 4 s²)"),
    ("move 4: the outer loop, forward ÷ (1 + forward)", "one block from command to heading"),
]


def box(fig, x0, x1, y, text, color=GREY, hi=False):
    fig.add_shape(type="rect", x0=x0, x1=x1, y0=y - 0.55, y1=y + 0.55, line=dict(color=ORANGE if hi else color,
                  width=5 if hi else 2.5), fillcolor="rgba(245,133,24,0.12)" if hi else "rgba(76,120,168,0.08)")
    fig.add_annotation(x=(x0 + x1) / 2, y=y, text=text, showarrow=False, font=dict(size=27))


def arrow(fig, x0, y0, x1, y1, label=None, lx=0, ly=0.5):
    fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=2, arrowsize=1.3, arrowwidth=2.5, arrowcolor=GREY, text="")
    if label:
        fig.add_annotation(x=(x0 + x1) / 2 + lx, y=(y0 + y1) / 2 + ly, text=label, showarrow=False,
                           font=dict(size=24, color=PURPLE))


def line(fig, xs, ys):
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=GREY, width=2.5)))


def summer(fig, x, y, signs):
    fig.add_shape(type="circle", x0=x - 0.32, x1=x + 0.32, y0=y - 0.32, y1=y + 0.32, line=dict(color=GREY, width=2.5),
                  fillcolor="white")
    for sx, sy, sg in signs:
        fig.add_annotation(x=x + sx, y=y + sy, text=sg, showarrow=False, font=dict(size=28))


def frame(n):
    title, rule = FRAMES[n]
    fig = go.Figure()
    Y = 4.0
    arrow(fig, 0.2, Y, 1.68, Y, "command θ<sub>r</sub>", lx=-0.1)
    if n <= 3:
        summer(fig, 2.0, Y, [(-0.5, -0.45, "+"), (0.45, -0.65, "−")])
    if n <= 1:
        box(fig, 3.2, 5.9, Y, "0.4 + Ki/s" if n == 0 else "(0.4 s + Ki) / s", hi=n == 1)
        arrow(fig, 2.32, Y, 3.2, Y)
        arrow(fig, 5.9, Y, 6.98, Y, "torque")
        summer(fig, 7.3, Y, [(-0.5, -0.45, "+"), (0.45, -0.65, "−")])
        box(fig, 8.6, 11.0, Y, "robot 10 / s²")
        arrow(fig, 7.62, Y, 8.6, Y)
        line(fig, [11.0, 12.3], [Y, Y])
        line(fig, [12.3, 12.3, 10.9], [Y, 2.3, 2.3])
        box(fig, 8.6, 10.9, 2.3, "D: 0.4 s", color=BLUE)
        line(fig, [8.6, 7.3], [2.3, 2.3])
        arrow(fig, 7.3, 2.3, 7.3, Y - 0.32)
        fig.add_trace(go.Scatter(x=[12.3], y=[Y], mode="markers", marker=dict(color=GREY, size=11)))
    if n == 2:
        box(fig, 3.2, 5.9, Y, "(0.4 s + Ki) / s")
        arrow(fig, 2.32, Y, 3.2, Y)
        box(fig, 7.0, 11.5, Y, "10 / (s² + 4 s)", hi=True)
        arrow(fig, 5.9, Y, 7.0, Y, "torque")
        line(fig, [11.5, 12.3], [Y, Y])
    if n == 3:
        box(fig, 3.0, 11.5, Y, "(4 s + 10 Ki) / (s³ + 4 s²)", hi=True)
        arrow(fig, 2.32, Y, 3.0, Y)
        line(fig, [11.5, 12.3], [Y, Y])
    if n <= 3:
        line(fig, [12.3, 13.4], [Y, Y])
        line(fig, [13.4, 13.4, 2.0], [Y, 0.9, 0.9])
        arrow(fig, 2.0, 0.9, 2.0, Y - 0.32)
        fig.add_trace(go.Scatter(x=[13.4], y=[Y], mode="markers", marker=dict(color=GREY, size=11)))
        arrow(fig, 13.4, Y, 15.3, Y, "heading θ")
    if n == 4:
        box(fig, 2.0, 13.4, Y, "(4 s + 10 Ki) / (s³ + 4 s² + 4 s + 10 Ki)", hi=True)
        arrow(fig, 1.6, Y, 2.0, Y)
        arrow(fig, 13.4, Y, 15.3, Y, "heading θ")
    if rule:
        fig.add_annotation(x=7.8, y=-0.1, text=rule, showarrow=False, font=dict(size=28, color=ORANGE))
    fig.update_xaxes(range=[0, 16], visible=False)
    fig.update_yaxes(range=[-0.5, 5.0], visible=False)
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=560, showlegend=False,
                      margin=dict(l=20, r=20, t=90, b=20), title=dict(x=0.5, y=0.95, text=title))
    return fig


figs = [frame(n) for n in range(5)]
make_gif(figs, here / "blocks_anim", fps=1, holds=[4, 4, 4, 4, 10], keys=[0, 1, 2, 3, 4], cols=2, width=900)
