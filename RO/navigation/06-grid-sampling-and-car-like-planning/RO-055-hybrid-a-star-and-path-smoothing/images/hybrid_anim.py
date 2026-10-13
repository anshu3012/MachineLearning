"""Hybrid A* on the parking lot, with the larger of the two guesses and the Reeds-Shepp shot. One frame per expansion
for the first ten, then several per frame. Each expansion drives the six arcs from the pose taken off the open list
(orange arrow): kept arcs blue (forward) or purple (reverse), arcs into an occupied cell-and-heading slot grey, arcs
that hit something red. Every few expansions the Reeds-Shepp path to the goal is tried (red dashed when it hits a
parked car). Expansion 312: the shot is free (green) and the search stops; last frame: the whole path.
Run -> hybrid_anim.gif, hybrid_anim_frames.png"""
import math
from pathlib import Path

import numpy as np
from carkit import GOAL, START, hybrid_astar, sample
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from lotdraw import axes, car, label, layout, lot, path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
R = hybrid_astar("max", shot=True, trace=True)
LOG = R["log"]
N = len(LOG)
SHOTS = [k for k, e in enumerate(LOG) if "shot" in e]
assert N == 312 and R["expanded"] == 312 and LOG[-1]["shot"]["ok"]
assert round(R["length"], 2) == 39.42 and R["cusps"] == 1


def lines(trajs):
    xs, ys = [], []
    for t in trajs:
        xs += list(t[:, 0]) + [None]
        ys += list(t[:, 1]) + [None]
    return xs, ys


def frame(k, final=False):
    """State after expansion k (1-based): the tree so far; the arcs of expansion k drawn by status."""
    fig = make_subplots(rows=1, cols=1)
    lot(fig, (1, 1), grid=True)
    fwd, rev = [], []
    for e in LOG[:k]:
        for c in e["children"]:
            if c["status"] == "added":
                (fwd if c["d"] > 0 else rev).append(c["traj"])
    for trajs, col in ((fwd, BLUE), (rev, PURPLE)):
        if trajs:
            xs, ys = lines(trajs)
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=1.6), hoverinfo="skip"),
                          row=1, col=1)
    if k and not final:
        e = LOG[k - 1]
        for c in e["children"]:
            if c["status"] == "dropped":
                path(fig, c["traj"][:, :2], (1, 1), colour=GREY, width=2.5, dash="dot")
            elif c["status"] == "blocked":
                path(fig, c["traj"][:, :2], (1, 1), colour=RED, width=2.5)
        last = next((LOG[j] for j in range(k - 1, -1, -1) if "shot" in LOG[j]), None)
        if last is not None and k - 1 - LOG.index(last) < 12:
            ok = last["shot"]["ok"]
            path(fig, last["shot"]["pts"][:, :2], (1, 1), colour=GREEN if ok else RED, width=3,
                 dash=None if ok else "dash")
        x, y, th = e["pose"]
        fig.add_trace(go.Scatter(x=[x, x + 1.6 * math.cos(th)], y=[y, y + 1.6 * math.sin(th)], mode="lines+markers",
                                 line=dict(color=ORANGE, width=4), marker=dict(size=[9, 0], color=ORANGE),
                                 hoverinfo="skip"), row=1, col=1)
    if final:
        path(fig, R["poses"][:, :2], (1, 1), colour=GREEN, width=5)
        car(fig, GOAL, (1, 1))
    car(fig, START, (1, 1), colour="#2E7D32", fill="rgba(84,162,75,0.25)", width=2)
    axes(fig, (1, 1))
    if k == 0:
        t, sub = "Hybrid A*: start pose (2, 3) facing 0 deg", "each expansion drives six arcs of 1.5 m"
    elif final:
        t = f"path found: {R['length']:.2f} m, one switch to reverse"
        sub = f"{N} expansions; the last piece is the Reeds-Shepp shot"
    else:
        t = f"Hybrid A*: expansion {k} of {N}"
        sub = "blue forward, purple reverse; grey: slot taken; red: collides"
        if k == N:
            sub = "the Reeds-Shepp shot to the goal is free (green)"
    return layout(fig, t, width=820, height=860, subtitle=sub)


ks = list(range(0, 11)) + list(range(20, N, 15)) + [N]
figs = [frame(k) for k in ks] + [frame(N, final=True)]
holds = [8] + [5] * 10 + [3] * (len(ks) - 12) + [12, 30]
make_gif(figs, here / "hybrid_anim", fps=5, holds=holds, keys=[0, 3, 10, len(ks) // 2, len(ks) - 1, len(figs) - 1],
         cols=2, width=700)
