"""Smoothing the grid route of the opening with Udacity CS373's smoother. First with data weight 0.5 and smoothing
weight 0.1: it settles after 20 sweeps, barely changed; its tightest turn is a circle of 0.69 m radius, the car needs
5 m. Then with data weight 0: after 11,292 sweeps the route is a straight line from the start to the bay, through
the middle row. Red dots: points where the car's body, facing along the route, overlaps a parked car or a wall.
Run -> grid_smooth_anim.gif, grid_smooth_anim_frames.png"""
from pathlib import Path

import numpy as np
from carkit import GOAL, START, collides, grid_astar, headings_along, smooth, turning
from gifkit import BLUE, GREY, ORANGE, RED, make_gif
from lotdraw import axes, car, layout, lot, path
from plotly.subplots import make_subplots

here = Path(__file__).parent
X = np.array(grid_astar()["path"], dtype=float)
K1 = [0, 1, 2, 3, 5, 10, 20]
Y1, IT1, REC1 = smooth(X, alpha=0.5, beta=0.1, keep=K1)
K2 = [1, 10, 100, 1000]
Y2, IT2, REC2 = smooth(X, alpha=0.0, beta=0.1, keep=K2)
REC2[IT2] = Y2
k0, _ = turning(X)
k1, _ = turning(Y1)


def hits(y):
    return collides(np.column_stack([y, headings_along(y, np.ones(len(y)))]), margin=0)


assert IT1 == 20 and IT2 == 11292
assert round(1 / k1.max(), 2) == 0.69 and int(hits(Y1).sum()) == 25 and int(hits(Y2).sum()) == 24


def frame(y, title, sub):
    fig = make_subplots(rows=1, cols=1)
    lot(fig, (1, 1))
    path(fig, X, (1, 1), colour=GREY, width=2, mode="lines+markers", size=5)
    path(fig, y, (1, 1), colour=BLUE, width=4, mode="lines+markers", size=7)
    h = hits(y)
    if h.any():
        path(fig, y[h], (1, 1), colour=RED, mode="markers", size=10)
    car(fig, START, (1, 1), colour="#2E7D32", width=2)
    car(fig, GOAL, (1, 1), colour=ORANGE, fill="rgba(0,0,0,0)", width=2)
    axes(fig, (1, 1))
    return layout(fig, title, width=820, height=860, subtitle=sub)


figs = []
for k in K1:
    t = "the grid route as found" if k == 0 else f"data weight 0.5, smoothing weight 0.1: sweep {k}"
    sub = "grey: the route; blue: after smoothing; red: the body hits something" if k < 20 else \
        f"settled after {IT1} sweeps; tightest turn: a {1 / k1.max():.2f} m circle"
    figs.append(frame(REC1[k], t, sub))
for k in K2 + [IT2]:
    sub = "no pull back to the route: the points slide towards a straight line" if k < IT2 else \
        f"after {IT2} sweeps: a straight line through the middle row"
    figs.append(frame(REC2[k], f"data weight 0: sweep {k}", sub))
holds = [8, 3, 3, 3, 3, 3, 20, 3, 3, 3, 3, 30]
make_gif(figs, here / "grid_smooth_anim", fps=4, holds=holds, keys=[0, 6, 9, len(figs) - 1], cols=2, width=700)
