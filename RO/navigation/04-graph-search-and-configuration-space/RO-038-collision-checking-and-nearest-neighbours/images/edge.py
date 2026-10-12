"""Animation: checking the segment from a = (2, 2) to b = (4, 3.6), 2.561 m long, in C-space (the obstacles grown by
0.25 m, orange). Its centres between t = 0.620 and 0.777 of the way, 0.403 m of it, are in collision. Part 1: 5 even
steps of 0.512 m; the checks at t = 0.6 and 0.8 straddle the colliding stretch and the segment wrongly passes.
Part 2: 32 steps of 0.080 m, checked from a towards b; the 21st check (t = 0.625) is the first hit. Part 3: the same
33 points in halving order (ends, middle, quarter points, ...); the 5th check, t = 0.75, the point (3.5, 3.2), hits.
Run -> edge.gif, edge_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from shapely.geometry import box

import collide as k
import cspace as c
import drawkit as dk
from gifkit import GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
a, b = np.array([2.0, 2.0]), np.array([4.0, 3.6])
L = float(np.linalg.norm(b - a))
D = c.cobs_disk()
P = lambda t: a + t * (b - a)
even5 = [i / 5 for i in range(6)]
even32 = [i / 32 for i in range(33)]
halving = k.halving_order(5)
first_even = next(i for i, t in enumerate(even32) if not k.free(P(t)))
first_half = next(i for i, t in enumerate(halving) if not k.free(P(t)))
assert all(k.free(P(t)) for t in even5) and first_even == 20 and first_half == 4 and halving[4] == 0.75
assert round(L, 3) == 2.561 and round(L / 5, 3) == 0.512 and round(L / 32, 3) == 0.080
VIEW = box(-0.2, -0.2, 7.2, 4.12)


def frame(title, checks, lines):
    fig = go.Figure()
    fig.add_trace(dk.geom_trace(D.intersection(VIEW).difference(c.obstacles()), dk.COBS_FILL, ORANGE, 2))
    dk.room(fig)
    fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color="black", width=3)))
    for t in checks:
        p = P(t)
        dk.point(fig, p[0], p[1], GREEN if k.free(p) else RED, None, size=12)
    fig.add_annotation(x=a[0] - 0.08, y=a[1], text="a", xanchor="right", showarrow=False, font=dict(size=20))
    fig.add_annotation(x=b[0] + 0.08, y=b[1], text="b", xanchor="left", showarrow=False, font=dict(size=20))
    for i, (s, col) in enumerate(lines):
        fig.add_annotation(x=0.66, y=0.95 - 0.08 * i, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           text=s, showarrow=False, font=dict(size=18, color=col))
    fig.update_xaxes(range=[1.5, 4.7], dtick=0.5, title="x (m)", domain=[0, 0.62], constrain="domain")
    fig.update_yaxes(range=[1.4, 4.3], dtick=0.5, title="y (m)", scaleanchor="x", constrain="domain")
    dk.layout(fig, 1300, 640, title, margin=dict(l=70, r=20, t=80, b=60))
    return fig


figs, holds = [], []
for n in range(1, 7):
    figs.append(frame("5 even steps of 0.512 m", even5[:n],
                      [(f"checks: {n} of 6", "black"), ("all free so far", GREEN)]))
    holds.append(2)
figs.append(frame("5 even steps: every check is free, yet the segment is not", even5,
                  [("6 checks, all free", GREEN), ("the checks at 0.6 and 0.8 of the way", "black"),
                   ("land either side of the 0.403 m", "black"), ("colliding stretch: missed", RED)]))
holds.append(8)
for n in range(1, first_even + 2):
    hit = n == first_even + 1
    figs.append(frame("32 steps of 0.080 m, checked from a towards b" + (": hit" if hit else ""), even32[:n],
                      [(f"checks: {n} of 33", "black"), ("collision at t = 0.625: stop" if hit else "all free so far",
                                                         RED if hit else GREEN)]))
    holds.append(6 if hit else 1)
for n in range(1, first_half + 2):
    hit = n == first_half + 1
    figs.append(frame("the same 33 points in halving order" + (": hit" if hit else ""), halving[:n],
                      [(f"checks: {n}", "black"), ("next: " + ", ".join(f"{t:g}" for t in halving[n:n + 3]) if not hit
                                                    else "collision at t = 0.75, the point (3.5, 3.2)",
                                                    RED if hit else "black")]))
    holds.append(3)
figs.append(frame("halving order: 5 checks find the collision; from a: 21", halving[:first_half + 1],
                  [("from a towards b: 21 checks", "black"), ("halving order: 5 checks", RED),
                   ("if the segment were free, both", "black"), ("would check all 33 points", "black")]))
holds.append(14)
make_gif(figs, here / "edge", fps=3, holds=holds, keys=[6, 6 + first_even + 1, len(figs) - 2, len(figs) - 1], cols=2,
         width=1000)
