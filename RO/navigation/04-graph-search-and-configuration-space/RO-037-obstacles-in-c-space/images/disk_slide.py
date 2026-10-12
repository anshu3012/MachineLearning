"""Animation: the robot's 0.25 m disk footprint slides round the table, always touching it, counter-clockwise from
under the bottom edge. Its centre traces the boundary of the grown table: straight lines 0.25 m out from each edge
and arcs of radius 0.25 m round each corner. Last frames: the grown table filled (the table's obstacle region) and
the centre (3.5, 3.2) inside it, 0.2 m from the corner. Run -> disk_slide.gif, disk_slide_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from shapely.geometry import Point, Polygon

import cspace as c
import drawkit as k
from gifkit import BLUE, ORANGE, RED, make_gif

here = Path(__file__).parent
T = Polygon(c.TABLE)
G = T.buffer(c.R, quad_segs=64)
P = np.array(c.TABLE)
assert abs(T.distance(Point(*c.TEST)) - 0.2) < 1e-9 and abs(G.area - 5.747) < 1e-3


def normal(i):
    d = P[(i + 1) % 4] - P[i]
    return np.array([d[1], -d[0]]) / np.hypot(*d)


# (centre, contact point, kind) along the boundary: edge 0 from its middle, then corner 1, edge 1, ... corner 0, edge 0
steps = []
dense = []
for j in range(5):
    i = j % 4
    a, b = P[i], P[(i + 1) % 4]
    t0, t1 = (0.5, 1.0) if j == 0 else ((0.0, 0.5) if j == 4 else (0.0, 1.0))
    ne = 2 if j in (0, 4) else 4
    for t in np.linspace(t0, t1, ne + 1)[(0 if j == 0 else 1):]:
        steps.append((a + t * (b - a) + c.R * normal(i), a + t * (b - a), "edge"))
    dense += [a + t * (b - a) + c.R * normal(i) for t in np.linspace(t0, t1, 30)]
    if j == 4:
        break
    n0, n1 = normal(i), normal((i + 1) % 4)
    g0, g1 = np.arctan2(n0[1], n0[0]), np.arctan2(n1[1], n1[0])
    g1 = g1 + 2 * np.pi if g1 < g0 else g1
    for g in np.linspace(g0, g1, 4)[1:-1]:
        steps.append((b + c.R * np.array([np.cos(g), np.sin(g)]), b, "corner"))
    dense += [b + c.R * np.array([np.cos(g), np.sin(g)]) for g in np.linspace(g0, g1, 30)]
dense = np.array(dense)


idx, last = [], 0
for p, _, _ in steps:                                  # the dense trace grows in order: nearest point from last on
    last += int(np.argmin(np.hypot(*(dense[last:] - p).T)))
    idx.append(last)


def frame(i, fill=False, test=False):
    fig = go.Figure()
    tx, ty = zip(*(c.TABLE + [c.TABLE[0]]))
    if fill:
        fig.add_trace(k.geom_trace(G.difference(T), k.COBS_FILL, ORANGE, 0))
    fig.add_trace(k.poly_trace(tx, ty, "rgba(76,120,168,0.35)", BLUE, 2))
    tr = dense if fill else dense[: idx[i] + 1]
    fig.add_trace(go.Scatter(x=tr[:, 0], y=tr[:, 1], mode="lines", line=dict(color=ORANGE, width=4),
                             hoverinfo="skip"))
    title = "the grown table: every centre that puts the disk on the table"
    if not fill:
        p, q, kind = steps[i]
        k.disk(fig, p[0], p[1], 0, body=False)
        fig.add_trace(go.Scatter(x=[p[0], q[0]], y=[p[1], q[1]], mode="lines", line=dict(color="black", width=2),
                                 hoverinfo="skip"))
        k.point(fig, p[0], p[1], ORANGE, size=11)
        k.point(fig, q[0], q[1], "black", size=8)
        title = ("at a corner: the centre swings round it on an arc of radius 0.25 m" if kind == "corner" else
                 "along an edge: the centre runs parallel to it, 0.25 m out")
    if test:
        k.point(fig, *c.TEST, RED, None, size=14)
        fig.add_trace(go.Scatter(x=[3.5, 3.5], y=[3.0, 3.2], mode="lines", line=dict(color=RED, width=3),
                                 hoverinfo="skip"))
        fig.add_annotation(x=3.3, y=3.45, text="centre (3.5, 3.2): 0.2 m from the corner,<br>less than 0.25 m: in collision",
                           xanchor="left", align="left", showarrow=False, font=dict(size=18, color=RED), bgcolor="white")
        title = "the centre (3.5, 3.2) lies inside the grown table"
    fig.add_annotation(x=4.25, y=2.0, text="table", showarrow=False, font=dict(size=20, color=BLUE))
    k.axes(fig, [2.4, 6.2], [0.35, 3.75], dtick=0.5)
    k.layout(fig, 900, 840, title)
    return fig


n = len(steps)
figs = [frame(i) for i in range(n)] + [frame(n - 1, fill=True), frame(n - 1, fill=True, test=True)]
holds = [4] + [2 if s[2] == "corner" else 1 for s in steps[1:]] + [5, 14]
corner = [i for i, s in enumerate(steps) if s[2] == "corner"]
make_gif(figs, here / "disk_slide", fps=4, holds=holds, keys=[1, corner[4], n - 2, n + 1], cols=2, width=760)
