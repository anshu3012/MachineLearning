"""Degrees of freedom of the robot's body counted point by point (close-up of the body, a disk of radius 0.25 m at
(2, 1) facing 30 degrees). A, the centre, can be anywhere: 2 numbers, 0 rules, 2 freedoms. B, 0.25 m ahead of A,
keeps its distance to A: it lies on a circle round A, 1 freedom (sliding B round the circle turns the body). C,
0.25 m to the left of A and 0.354 m from B, keeps both distances: the two circles meet in 2 points, one of them with
the body upside down, so C is fixed, 0 freedoms. Total 2 + 1 + 0 = 3: (x, y, theta).
Run: python dof_count.py -> dof_count.gif, dof_count_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from cmodel import Q0, R_BODY, TWO_PI, body_point
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif

here = Path(__file__).parent
A = np.array(Q0[:2])
B = np.array(body_point(Q0, (R_BODY, 0)))
C = np.array(body_point(Q0, (0, R_BODY)))
dAB, dAC, dBC = np.hypot(*(B - A)), np.hypot(*(C - A)), np.hypot(*(C - B))
assert np.allclose([dAB, dAC], 0.25) and round(dBC, 3) == 0.354
assert np.allclose(B, (2.217, 1.125), atol=5e-4) and np.allclose(C, (1.875, 1.217), atol=5e-4)
C2 = A + 2 * np.dot(C - A, B - A) / dAB ** 2 * (B - A) - (C - A)          # C mirrored in the line AB
assert np.isclose(np.hypot(*(C2 - A)), dAC) and np.isclose(np.hypot(*(C2 - B)), dBC)
ROWS = [("A", 2, 0, 2), ("B", 2, 1, 1), ("C", 2, 2, 0)]
assert sum(r[3] for r in ROWS) == 3


def circle(c, r, n=80):
    a = np.linspace(0, TWO_PI, n)
    return c[0] + r * np.cos(a), c[1] + r * np.sin(a)


def frame(title, th=Q0[2], show="", rows=0, total=False, space=False):
    fig = go.Figure()
    q = (A[0], A[1], th)
    bx, by = circle(A, R_BODY)
    fig.add_trace(go.Scatter(x=bx, y=by, mode="lines", fill="toself", line=dict(color=GREY, width=2),
                             fillcolor="rgba(107,107,107,0.12)"))
    b = np.array(body_point(q, (R_BODY, 0)))
    c = np.array(body_point(q, (0, R_BODY)))
    if "B" in show:
        x, y = circle(A, dAB)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=ORANGE, width=3, dash="dash")))
    if "C" in show:
        x, y = circle(b, dBC)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=PURPLE, width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=[C2[0]], y=[C2[1]], mode="markers+text", marker=dict(size=13, color=GREY,
                                 symbol="x"), text=["upside down"], textposition="bottom center",
                                 textfont=dict(size=18, color=GREY)))
    pts = [("A", A, BLUE)] + ([("B", b, ORANGE)] if "B" in show else []) + ([("C", c, PURPLE)] if "C" in show else [])
    if "B" in show:                                          # the line A to B: its direction is the heading
        fig.add_trace(go.Scatter(x=[A[0], b[0]], y=[A[1], b[1]], mode="lines", line=dict(color=RED, width=3)))
        fig.add_annotation(x=(A[0] + b[0]) / 2, y=(A[1] + b[1]) / 2, text="θ", showarrow=False, yshift=-14,
                           xshift=10, font=dict(size=22, color=RED))
    if "A" in show:
        for name, p, col in pts:
            fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers+text", marker=dict(size=15, color=col),
                                     text=[f"<b>{name}</b>"], textposition="bottom left" if name == "A" else "top right", textfont=dict(size=22, color=col)))
    # the table
    head = "<b>point   numbers − rules = freedoms</b>"
    lines = [head] + [f"{n}            {k}      −     {r}     =     {f}" for n, k, r, f in ROWS[:rows]]
    if total:
        lines += ["", "<b>total: 2 + 1 + 0 = 3</b>", "the three numbers (x, y, θ)"]
    if space:
        lines += ["", "the same count in space:", "3 + 2 + 1 = 6"]
    fig.add_annotation(x=2.68, y=1.62, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=21))
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=620, showlegend=False,
                      margin=dict(l=60, r=20, t=95, b=50), title=dict(x=0.5, text=title),
                      xaxis=dict(range=[1.5, 4.05], title="x (m)", dtick=0.5, showgrid=False),
                      yaxis=dict(range=[0.62, 1.68], title="y (m)", dtick=0.25, scaleanchor="x"))
    return fig


figs, holds = [], []
figs.append(frame("the robot's body (close-up): how many numbers fix all its points?"))
holds.append(3)
figs.append(frame("A, the centre: 2 numbers, no rule yet: 2 freedoms", show="A", rows=1))
holds.append(5)
for d in (0, 40, 80, 120, 0):
    figs.append(frame("B stays 0.25 m from A: it can only slide round the circle: 1 freedom", th=Q0[2] + np.radians(d),
                      show="AB", rows=2))
    holds.append(2)
holds[-1] = 5
figs.append(frame("C stays 0.25 m from A and 0.354 m from B:<br>the two circles meet in 2 points, so C is fixed: 0 freedoms",
                  show="ABC", rows=3))
holds.append(6)
figs.append(frame("2 + 1 + 0 = 3 degrees of freedom: (x, y, θ)", show="ABC", rows=3, total=True, space=True))
holds.append(12)
make_gif(figs, here / "dof_count", fps=2, holds=holds, keys=[1, 3, 7, 8], cols=2, width=900)
