"""Animation: lattice search on the straight drive to the closed door (LaValle 14.4.1). Every 0.5 s the robot
accelerates (+0.5 m/s^2), coasts or brakes (-0.5 m/s^2). Speeds land on multiples of 0.25 m/s and positions on
multiples of 0.0625 m, so every reachable state is a point of a lattice (faint grey dots). Breadth-first search
from rest at s = 0 adds one layer of states per 0.5 s (newest layer outlined); the curves are the true motions between
them. States beyond the door (s > 3.117 m) or faster than 0.6 m/s are never added. After 14 layers (7.0 s) the search
reaches the goal, at rest at s = 3.0 m; the last frame shows that plan: speed up for 1 s, cruise at 0.5 m/s for 5 s,
brake for 1 s. Run -> lattice_anim.gif, lattice_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import drawkit as k
import motionkit as m
from gifkit import BLUE, GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
DT = 0.5
R = m.lattice_search(DT, trace=True)
LEVELS = R["levels"]
assert R["steps"] == 14 and R["time"] == 7.0 and R["n_states"] == 73
assert R["q"] == 0.0625 and R["dv"] == 0.25
PATH = R["path"]
assert PATH[1] == (0.0625, 0.25) and PATH[2] == (0.25, 0.5) and PATH[-2] == (2.9375, 0.25) and PATH[-1] == (3.0, 0.0)
q, dv = R["q"], R["dv"]


def motion(s, v, u, n=12):
    t = np.linspace(0, DT, n)
    return s + v * t + 0.5 * u * t * t, v + u * t


# every edge of the search, by the layer of its child: rebuild the parents as the search found them
seen = {LEVELS[0][0]}
EDGES = []
for lv in range(1, len(LEVELS)):
    layer = []
    for child in LEVELS[lv]:
        for par in LEVELS[lv - 1]:
            for u in (m.A_MAX, 0.0, -m.A_MAX):
                s1, v1 = motion(par[0], par[1], u, 2)
                if abs(s1[-1] - child[0]) < 1e-9 and abs(v1[-1] - child[1]) < 1e-9:
                    layer.append((par, u))
                    break
            else:
                continue
            break
    EDGES.append(layer)
assert all(len(e) == len(LEVELS[i + 1]) for i, e in enumerate(EDGES))


def frame(n, final=False):
    fig = go.Figure()
    k.phase_regions(fig)
    gs, gv = [], []
    for j in range(0, 3):
        for i in range(0, int(m.S_DOOR / q) + 1):
            gs.append(i * q)
            gv.append(j * dv)
    k.line(fig, gs, gv, color="#BBBBBB", mode="markers", width=1)
    fig.data[-1].marker = dict(size=4, color="#BBBBBB")
    xs, ys = [], []
    for lv in range(min(n, len(EDGES))):
        for par, u in EDGES[lv]:
            s, v = motion(par[0], par[1], u)
            xs += list(s) + [None]
            ys += list(v) + [None]
    k.line(fig, xs, ys, color=BLUE, width=1.5)
    pts = [p for lv in LEVELS[:n + 1] for p in lv]
    k.line(fig, [p[0] for p in pts], [p[1] for p in pts], color=BLUE, mode="markers", width=1)
    fig.data[-1].marker = dict(size=8, color=BLUE)
    if not final and n < len(LEVELS):
        new = LEVELS[n]
        k.line(fig, [p[0] for p in new], [p[1] for p in new], color=ORANGE, mode="markers", width=1)
        fig.data[-1].marker = dict(size=13, color="rgba(0,0,0,0)", line=dict(color=ORANGE, width=3))
    if final:
        xs, ys = [], []
        for a, b in zip(PATH, PATH[1:]):
            u = (b[1] - a[1]) / DT
            s, v = motion(a[0], a[1], u)
            xs += list(s)
            ys += list(v)
        k.line(fig, xs, ys, color=GREEN, width=6)
        k.text(fig, 0.2, 0.36, "speed up 1 s", color=GREEN, size=18, xanchor="left", bg="rgba(255,255,255,0.85)")
        k.text(fig, 1.6, 0.56, "cruise at 0.5 m/s for 5 s", color=GREEN, size=18, bg="rgba(255,255,255,0.8)")
        k.text(fig, 2.62, 0.13, "brake 1 s", color=GREEN, size=18, bg="rgba(255,255,255,0.8)")
    k.point(fig, 0, 0, "black", size=12)
    k.point(fig, m.S_GOAL, 0, RED, size=16, symbol="star")
    k.text(fig, m.S_GOAL - 0.18, 0.04, "goal", color=RED, size=17, bg="rgba(0,0,0,0)")
    k.text(fig, 3.26, 0.35, "door", color=k.DOOR, size=17)
    k.phase_axes(fig, xr=(-0.05, k.S_MAX))
    fig.update_yaxes(range=[-0.04, 0.7])
    title = ("goal reached after 14 layers: the fastest drive on this lattice takes 7.0 s" if final else
             f"breadth-first search, layer {n}: every state reachable in {n * DT:.1f} s ({len(LEVELS[n])} new)")
    return k.layout(fig, 1200, 620, title, margin=dict(l=80, r=30, t=70, b=70), size=21)


n_lv = len(LEVELS) - 1
figs = [frame(n) for n in range(n_lv + 1)] + [frame(n_lv, final=True)]
holds = [6] + [4] * n_lv + [28]
make_gif(figs, here / "lattice_anim", fps=5, holds=holds, keys=[1, 3, 8, len(figs) - 1], cols=2, width=1000)
