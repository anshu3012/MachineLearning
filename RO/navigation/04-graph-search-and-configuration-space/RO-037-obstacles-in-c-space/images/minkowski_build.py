"""Animation: the board's obstacle region at heading 0 built as a Minkowski sum. First the board (1.4 m x 0.3 m) with
its front end on the table's corner (3.0, 1.0): its centre is at 3.0 - 0.7 = 2.3. Then copies of the reflected board
are centred on table points, corners first, then along the edges and inside; together they sweep out the table plus
the board. The last frame outlines their convex hull, the obstacle region of the table at heading 0: 7 corners, at
most 4 + 4 = 8. Run -> minkowski_build.gif, minkowski_build_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from shapely.geometry import Point, Polygon

import cspace as c
import drawkit as k
from gifkit import BLUE, GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
T = Polygon(c.TABLE)
S = c.cobs_board_piece(T, 0.0)
assert len(c.corners(S)) == 7 and S.boundary.distance(Point(2.3, 1.0)) < 1e-12
P = np.array(c.TABLE)
corner_pts = [tuple(p) for p in P]
edge_pts = [tuple(P[i] + t * (P[(i + 1) % 4] - P[i])) for i in range(4) for t in (0.25, 0.5, 0.75)]
inner = [p for p in [(x, y) for x in np.arange(3.2, 5.4, 0.35) for y in np.arange(1.25, 2.9, 0.35)]
         if T.contains(Point(p))]
BF = "rgba(140,86,75,0.30)"


def frame(copies, title, tip=False, hull=False):
    fig = go.Figure()
    if hull:
        fig.add_trace(k.geom_trace(S.difference(T), k.COBS_FILL, ORANGE, 0))
        sx, sy = c.outline(S)
        fig.add_trace(go.Scatter(x=sx, y=sy, mode="lines", line=dict(color=ORANGE, width=4), hoverinfo="skip"))
    tx, ty = zip(*(c.TABLE + [c.TABLE[0]]))
    fig.add_trace(k.poly_trace(tx, ty, "rgba(76,120,168,0.35)", BLUE, 2))
    for x, y in copies:
        fig.add_trace(k.board_trace(x, y, 0.0, color="rgba(140,86,75,0.9)", fill=BF, width=1))
        k.point(fig, x, y, "rgba(140,86,75,1)", size=6)
    if tip:
        fig.add_trace(k.board_trace(2.3, 1.0, 0.0))
        k.point(fig, 2.3, 1.0, GREEN, None, size=12)
        k.point(fig, 3.0, 1.0, "black", None, size=10)
        fig.add_annotation(x=2.3, y=1.42, text="centre q = (2.3, 1.0)", showarrow=False, font=dict(size=18, color=GREEN),
                           bgcolor="white")
        fig.add_annotation(x=3.05, y=0.62, text="front end a = (0.7, 0) from the centre<br>on the corner o = (3.0, 1.0)",
                           xanchor="left", align="left", showarrow=False, font=dict(size=17), bgcolor="white")
    if hull:
        k.point(fig, 2.3, 1.0, GREEN, None, size=12)
        cx, cy = zip(*c.corners(S))
        fig.add_trace(go.Scatter(x=cx, y=cy, mode="markers", marker=dict(size=11, color=ORANGE,
                                 line=dict(color="white", width=1)), hoverinfo="skip"))
    fig.add_annotation(x=4.25, y=2.0, text="table", showarrow=False, font=dict(size=20, color=BLUE))
    k.axes(fig, [1.7, 6.5], [0.3, 3.85], dtick=0.5)
    k.layout(fig, 980, 760, title)
    return fig


figs, holds = [frame([], "the board at heading 0: its front end touches the table's corner", tip=True)], [10]
for i in range(1, 5):
    figs.append(frame(corner_pts[:i], f"a reflected board centred on table corner {i} of 4"))
    holds.append(3)
figs.append(frame(corner_pts + edge_pts, "more copies along the edges"))
holds.append(4)
figs.append(frame(corner_pts + edge_pts + inner, "copies on every table point sweep out a region"))
holds.append(4)
figs.append(frame(corner_pts + edge_pts + inner, "the obstacle region at heading 0: their outline, 7 corners", hull=True))
holds.append(5)
figs.append(frame([], "the obstacle region at heading 0: (2.3, 1.0) lies on its edge", hull=True))
holds.append(14)
make_gif(figs, here / "minkowski_build", fps=3, holds=holds, keys=[0, 4, 6, 8], cols=2, width=820)
