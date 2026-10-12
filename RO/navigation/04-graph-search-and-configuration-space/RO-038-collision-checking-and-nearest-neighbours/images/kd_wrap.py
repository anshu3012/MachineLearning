"""Animation: nearest-neighbour search in a k-d tree over 8 stored configurations (x, heading), for the query
x = 3.55 m, heading 350 degrees. Distances count 0.25 m per radian of heading, so the vertical axis is drawn in those
metres and a circle of equal distance is round. Plain search treats headings as numbers from 0 to 360: it prunes the
cell of headings 0 to 175 degrees as 175 degrees (0.764 m) away and returns H (3.40 m, 320 degrees) at 0.199 m.
Search with wrap-around measures that cell the short way round, 10 degrees (0.044 m), visits it and returns
E (3.60 m, 15 degrees) at 0.120 m. The circle of the best distance so far wraps from the top edge to the bottom.
Run -> kd_wrap.gif, kd_wrap_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import collide as k
import drawkit as dk
from gifkit import BLUE, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
WR = k.W_RAD
TOP = 2 * np.pi * WR
P = [("A", 3.10, 40), ("B", 3.30, 120), ("C", 3.55, 200), ("D", 3.85, 300), ("E", 3.60, 15), ("F", 3.20, 250),
     ("G", 3.90, 150), ("H", 3.40, 320)]
pts = [(x, np.radians(t), n) for n, x, t in P]
Q = (3.55, np.radians(350))
root = k.build_kd(pts)
runs = {}
for wrap in (False, True):
    log = []
    best = k.search_kd(root, Q, wrap, (None, np.inf), log)
    runs[wrap] = (best, log)
assert runs[False][0][0][2] == "H" and round(runs[False][0][1], 3) == 0.199
assert runs[True][0][0][2] == "E" and round(runs[True][0][1], 3) == 0.120
assert round(runs[False][1][2][4], 3) == 0.764 and round(k.cell_gap(Q, runs[False][1][2][0], True), 3) == 0.044
splits = []


def walk(n):
    if "pts" in n:
        return
    (x0, t0), (x1, t1) = n["cell"]
    s = n["split"]
    splits.append(([s, s], [WR * t0, WR * t1]) if n["axis"] == 0 else ([x0, x1], [WR * s, WR * s]))
    for kid in n["kids"]:
        walk(kid)


walk(root)


def frame(title, wrap, upto, lines):
    best, log = runs[wrap]
    fig = go.Figure()
    for xs, ys in splits:
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=GREY, width=2), hoverinfo="skip"))
    cur = None
    for cell, kind, b, p, d in log[:upto]:
        (x0, t0), (x1, t1) = cell
        fill = "rgba(84,162,75,0.18)" if kind == "leaf" else "rgba(228,87,86,0.14)"
        fig.add_trace(dk.poly_trace([x0, x1, x1, x0, x0], [WR * t0, WR * t0, WR * t1, WR * t1, WR * t0], fill,
                                    GREEN if kind == "leaf" else RED, 3))
        cur = b
    for x, t, n in pts:
        fig.add_trace(go.Scatter(x=[x], y=[WR * t], mode="markers+text", text=[f"{n} ({np.degrees(t):.0f}°)"],
                                 textposition="top center", marker=dict(size=12, color=BLUE),
                                 textfont=dict(size=16, color=BLUE), hoverinfo="skip"))
    if cur and cur[0]:
        r, a = cur[1], np.linspace(0, 2 * np.pi, 100)
        for shift in ((0, -TOP) if wrap else (0,)):
            fig.add_trace(go.Scatter(x=Q[0] + r * np.cos(a), y=WR * Q[1] + shift + r * np.sin(a), mode="lines",
                                     line=dict(color=ORANGE, width=3, dash="dot"), hoverinfo="skip"))
        ty = WR * cur[0][1]
        if wrap and abs(WR * Q[1] - ty) > TOP / 2:              # the short way crosses the top and bottom edges
            ty += TOP if ty < WR * Q[1] else -TOP
        for shift in ((0, -TOP) if ty > TOP else (0,)):
            fig.add_trace(go.Scatter(x=[Q[0], cur[0][0]], y=[WR * Q[1] + shift, ty + shift], mode="lines",
                                     line=dict(color=ORANGE, width=3), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[Q[0]], y=[WR * Q[1]], mode="markers+text", text=["query (350°)"],
                             textposition="middle right", marker=dict(size=18, color=RED, symbol="star"),
                             textfont=dict(size=16, color=RED), hoverinfo="skip"))
    for i, (s, col) in enumerate(lines):
        fig.add_annotation(x=0.6, y=0.95 - 0.075 * i, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           text=s, showarrow=False, font=dict(size=18, color=col))
    fig.update_xaxes(range=[2.95, 4.05], dtick=0.25, title="x (m)", domain=[0, 0.56], constrain="domain")
    fig.update_yaxes(range=[-0.02, TOP + 0.02], tickvals=[WR * np.radians(d) for d in range(0, 361, 90)],
                     ticktext=[f"{d}°" for d in range(0, 361, 90)], title="heading", scaleanchor="x",
                     constrain="domain")
    dk.layout(fig, 1350, 720, title, margin=dict(l=90, r=20, t=80, b=60))
    return fig


figs, holds = [], []
figs.append(frame("8 stored configurations in a k-d tree; the query at 350°", False, 0,
                  [("cells split alternately on x and heading", "black"),
                   ("distance: metres, plus 0.25 m per radian", "black"), ("of heading difference", "black")]))
holds.append(6)
for wrap in (False, True):
    best, log = runs[wrap]
    name = "with wrap-around" if wrap else "plain"
    for i, (cell, kind, b, p, d) in enumerate(log, 1):
        if kind == "leaf":
            msg = [(f"visit the cell of {p[2]}: {d:.3f} m away", GREEN), (f"best so far: {b[0][2]}, {b[1]:.3f} m", "black")]
        else:
            msg = [(f"cell at least {d:.3f} m away,", RED), (f"more than the best, {b[1]:.3f} m: prune", RED)]
        if not wrap and i == 3:
            msg += [("", "black"), ("plain: 350° − 175° = 175°, that is 0.764 m", "black")]
        if wrap and i == 3:
            msg += [("", "black"), ("round the circle: 360° − 350° = 10°,", "black"), ("that is 0.044 m: visit it", "black")]
        figs.append(frame(f"{name} search, step {i}", wrap, i, msg))
        holds.append(6 if i == 3 else 3)
    figs.append(frame(f"{name} search returns {best[0][2]} at {best[1]:.3f} m", wrap, len(log),
                      [(f"nearest: {best[0][2]}, {best[1]:.3f} m", ORANGE),
                       ("wrong: E at 15° is nearer, 0.120 m" if not wrap else "right: 25° round the circle", RED if not wrap else GREEN)]))
    holds.append(10 if not wrap else 14)
make_gif(figs, here / "kd_wrap", fps=2, holds=holds, keys=[3, 7, 10, len(figs) - 1], cols=2, width=1000)
