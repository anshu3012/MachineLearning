"""The opening problem: A* on the 1 m grid (RO-034) gives a 33.31 m route from the start (2, 3) to the target bay,
through cell centres, with 8 corners, ending nose first (heading 90 deg) although the car must back in (-90 deg). The
car drives at 1 m/s and steers towards the route point 2 m ahead, never tighter than its 5 m circle. After 4.05 m its
body hits the third parked car of the middle row. Run -> opening_anim.gif, opening_anim_frames.png"""
import math
from pathlib import Path

import numpy as np
from carkit import GOAL, START, follow_route, grid_astar
from gifkit import BLUE, RED, make_gif
from lotdraw import axes, car, label, layout, lot, path
from plotly.subplots import make_subplots

here = Path(__file__).parent
G = grid_astar()
TR, HIT = follow_route(G["path"])
P = np.array(G["path"], dtype=float)
d = np.diff(P, axis=0)
ang = np.degrees(np.arctan2(d[:, 1], d[:, 0]))
CORNERS = int(np.sum(np.abs(np.diff(ang)) > 1e-9))
DRIVEN = (len(TR) - 1) * 0.05
assert round(G["cost"], 2) == 33.31 and CORNERS == 8 and ang[-1] == 90.0
assert HIT and round(DRIVEN, 2) == 4.05


def frame(k, crash=False):
    fig = make_subplots(rows=1, cols=1)
    lot(fig, (1, 1), grid=True)
    path(fig, P, (1, 1), colour=BLUE, width=3, mode="lines+markers", size=6)
    seen = TR[:k + 1]
    path(fig, seen[:, :2], (1, 1), colour="#2E7D32", width=3)
    pose = tuple(TR[k])
    if crash:
        car(fig, pose, (1, 1), colour=RED, fill="rgba(228,87,86,0.45)")
        label(fig, 7.0, 13.8, "<b>body hits a parked car</b>", (1, 1), size=19, colour=RED)
    else:
        car(fig, pose, (1, 1))
    car(fig, GOAL, (1, 1), colour="#F58518", fill="rgba(0,0,0,0)", width=2, arrow=True)
    label(fig, 12.5, 18.2, "goal: backed in", (1, 1), size=16, colour="#F58518", anchor="left")
    axes(fig, (1, 1))
    if k == 0:
        t = f"A* on the 1 m grid: route {G['cost']:.2f} m, {CORNERS} corners"
        sub = "the route (blue) joins cell centres and ends facing up, nose first"
    elif crash:
        t = f"after {DRIVEN:.2f} m the car's body hits the middle row"
        sub = "the route was planned for a point that turns on the spot"
    else:
        t = f"the car follows the route: {k * 0.05:.2f} m driven"
        sub = "it turns no tighter than its 5 m circle; its 4 m body cannot keep to the route"
    return layout(fig, t, width=820, height=860, subtitle=sub)


n = len(TR) - 1
ks = list(range(0, n, 5)) + [n]
figs = [frame(k) for k in ks] + [frame(n, crash=True)]
holds = [10] + [2] * (len(ks) - 1) + [30]
make_gif(figs, here / "opening_anim", fps=6, holds=holds, keys=[0, len(figs) // 3, 2 * len(figs) // 3, len(figs) - 1],
         cols=2, width=700)
