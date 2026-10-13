"""A* on the state lattice. Grey dots: the lattice points (whole metres). Each expansion takes the state with the
smallest f (orange arrow) and copies the control set there: moves whose swept cells touch a parked car or a wall red,
moves to a state already reached more cheaply grey dotted, kept moves blue (forward) or purple (reverse). One frame
per expansion for the first eight, then several per frame. Expansion 629 takes off the goal state, exactly the goal
pose; last frame: the path, 42.93 m with one switch to reverse. Run -> lattice_anim.gif, lattice_anim_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from latticekit import CONTROL, lattice_astar, move_poses
from lotdraw import axes, car, layout, lot, path
from plotly.subplots import make_subplots

here = Path(__file__).parent
R = lattice_astar(trace=True)
LOG = R["log"]
N = len(LOG)
assert N == 629 and R["expanded"] == 629 and round(R["length"], 2) == 42.93 and R["cusps"] == 1
GX, GY = np.meshgrid(np.arange(0, 25), np.arange(0, 25))


def mpts(s, k):
    return move_poses(s[0], s[1], s[2], CONTROL[s[2]][k], ds=0.25)


def lines(items):
    xs, ys = [], []
    for p in items:
        xs += list(p[:, 0]) + [None]
        ys += list(p[:, 1]) + [None]
    return xs, ys


def frame(k, final=False):
    fig = make_subplots(rows=1, cols=1)
    lot(fig, (1, 1))
    fig.add_trace(go.Scatter(x=GX.ravel(), y=GY.ravel(), mode="markers", marker=dict(color="#CFCFCF", size=3),
                             hoverinfo="skip"), row=1, col=1)
    fwd, rev = [], []
    for e in LOG[:k]:
        for kk, st in e["kids"]:
            if st == "added":
                (fwd if CONTROL[e["state"][2]][kk]["d"] > 0 else rev).append(mpts(e["state"], kk))
    for items, col in ((fwd, BLUE), (rev, PURPLE)):
        if items:
            xs, ys = lines(items)
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=1.4), hoverinfo="skip"),
                          row=1, col=1)
    if k and not final:
        e = LOG[k - 1]
        for kk, st in e["kids"]:
            p = mpts(e["state"], kk)
            if st == "blocked":
                path(fig, p[:, :2], (1, 1), colour=RED, width=2.5)
            elif st == "dropped":
                path(fig, p[:, :2], (1, 1), colour=GREY, width=2.5, dash="dot")
            else:
                path(fig, p[:, :2], (1, 1), colour=BLUE if CONTROL[e["state"][2]][kk]["d"] > 0 else PURPLE, width=3.5)
        x, y, h, _ = e["state"]
        th = h * math.pi / 4
        fig.add_trace(go.Scatter(x=[x, x + 1.6 * math.cos(th)], y=[y, y + 1.6 * math.sin(th)], mode="lines+markers",
                                 line=dict(color=ORANGE, width=4), marker=dict(size=[10, 0], color=ORANGE),
                                 hoverinfo="skip"), row=1, col=1)
    if final:
        path(fig, R["poses"][:, :2], (1, 1), colour=GREEN, width=5)
        car(fig, (12.0, 23.0, -math.pi / 2), (1, 1))
    car(fig, (2.0, 3.0, 0.0), (1, 1), colour="#2E7D32", fill="rgba(84,162,75,0.25)", width=2)
    axes(fig, (1, 1))
    if k == 0:
        t, sub = "A* on the state lattice: start (2, 3) facing 0 deg", "every state is a lattice point and a heading"
    elif final:
        t, sub = f"path found: {R['length']:.2f} m, one switch to reverse", f"{N} expansions; it ends exactly on the goal"
    else:
        t = f"lattice search: expansion {k} of {N}"
        sub = "the control set copied at the state; red: collides; grey: reached already"
    return layout(fig, t, width=820, height=860, subtitle=sub)


ks = list(range(0, 9)) + list(range(30, N, 30)) + [N]
figs = [frame(k) for k in ks] + [frame(N, final=True)]
holds = [8] + [5] * 8 + [3] * (len(ks) - 10) + [10, 30]
make_gif(figs, here / "lattice_anim", fps=5, holds=holds, keys=[0, 2, 8, len(ks) // 2, len(ks) - 1, len(figs) - 1],
         cols=2, width=700)
