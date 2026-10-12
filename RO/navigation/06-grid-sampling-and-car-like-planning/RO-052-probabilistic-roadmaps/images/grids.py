"""Figure: two grids of configurations in the room's C-space, the robot's centre at the middle of each cell, a point
kept if the disk is free there, neighbours (8 directions) joined by free straight edges, each end of a trip joined to
the grid points it sees within 1.5 cells. Left, 0.5 m cells: 44 of 112 points free, none near the corner behind the
green pole, so trip 3 (cabinet to corner) gets "no path". Right, 0.25 m cells: 244 of 448 points free, route 1.903 m.
Run -> grids.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.spatial import cKDTree

import cspace as c
import drawkit as dk
import prm
import prmdraw as pd
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE, RED

here = Path(__file__).parent
w = prm.World()
_, S, _, G = prm.TRIPS[2]


def grid_plan(h):
    xs, ys = np.arange(h / 2, c.W, h), np.arange(h / 2, c.H, h)
    P = np.array([(x, y) for y in ys for x in xs])
    total = len(P)
    P = P[w.free_xy(P[:, 0], P[:, 1])]
    idx = {tuple(np.round(p, 6)): i for i, p in enumerate(P)}
    E = []
    for i, p in enumerate(P):
        for dx, dy in ((h, 0), (0, h), (h, h), (h, -h)):
            q = tuple(np.round(p + np.array([dx, dy]), 6))
            if q in idx and w.seg_free_exact(p, q):
                E.append((i, idx[q]))
    V = [tuple(p) for p in P] + [S, G]
    tree = cKDTree(P)
    for qi, q in ((len(P), S), (len(P) + 1, G)):
        for j in tree.query_ball_point(q, h * 1.5):
            if w.seg_free_exact(q, P[j]):
                E.append((qi, j))
    path, L, _ = prm.astar(V, E, len(P), len(P) + 1)
    return total, P, V, E, ([V[i] for i in path] if path else None), L


fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06,
                    subplot_titles=["0.5 m cells: 44 points, no path to the corner",
                                    "0.25 m cells: 244 points, route 1.903 m"])
for col, h in ((1, 0.5), (2, 0.25)):
    total, P, V, E, path, L = grid_plan(h)
    assert (total, len(P)) == {0.5: (112, 44), 0.25: (448, 244)}[h]
    assert (path is None) if h == 0.5 else round(L, 3) == 1.903
    fig.add_trace(dk.geom_trace(w.cobs.intersection(pd.VIEW).difference(c.obstacles()), dk.COBS_FILL, ORANGE, 1.5),
                  row=1, col=col)
    dk.room(fig, row=1, col=col)
    xs, ys = [], []
    for i, j in E:
        xs += [V[i][0], V[j][0], None]
        ys += [V[i][1], V[j][1], None]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="rgba(76,120,168,0.5)", width=1.3)),
                  row=1, col=col)
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers", marker=dict(color=BLUE, size=6 if h < 0.5 else 9)),
                  row=1, col=col)
    if path:
        Q = np.asarray(path)
        fig.add_trace(go.Scatter(x=Q[:, 0], y=Q[:, 1], mode="lines", line=dict(color=GREEN, width=5)), row=1, col=col)
    for q, t, pos in ((S, "cabinet", "middle left"), (G, "corner", "bottom center")):
        dk.point(fig, q[0], q[1], PURPLE, t, pos=pos, row=1, col=col, tsize=18)
    fig.update_xaxes(range=[-0.2, 7.2], dtick=1, title="x (m)", showgrid=False, row=1, col=col)
    fig.update_yaxes(range=[-0.2, 4.3], dtick=1, title="y (m)" if col == 1 else None, showgrid=False,
                     scaleanchor="x" if col == 1 else "x2", row=1, col=col)
fig.update_layout(template="simple_white", width=1500, height=520, font=FONT, showlegend=False,
                  margin=dict(l=70, r=20, t=70, b=60))
fig.update_annotations(font=dict(size=21))
fig.write_image(here / "grids.png")
