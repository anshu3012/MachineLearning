"""Figure: connected components of free space in two slices of C-space for the robot carrying the board. Each
coloured area is one piece of free centres: within a piece the centre can move anywhere without leaving free space,
between pieces it cannot. Heading 0: 2 pieces. Heading 90: 3 pieces (one a 0.004 m2 sliver); the start (2, 1) and the
doorway centre (3.6, 4.0) share the large piece, the point (6.6, 1.3) is in another. Run -> components.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import ndimage

import cspace as c
import drawkit as k
from gifkit import GREEN, PURPLE, RED

here = Path(__file__).parent
h = 0.01
COLS = ["rgba(245,133,24,0.28)", "#CFE8C9", "#C9D7EA", "#F2D7A8", "#E6CFE0"]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.05,
                    subplot_titles=["heading 0°: 2 pieces", "heading 90°: 3 pieces"])
for col, d in [(1, 0), (2, 90)]:
    xs, ys, F = c.free_grid(c.cobs_board(np.radians(d)), h=h)
    lab, n = ndimage.label(F)
    assert n == {0: 2, 90: 3}[d]
    sizes = np.bincount(lab.ravel())[1:]
    order = np.argsort(-sizes) + 1                            # colour pieces by size: largest first
    z = np.zeros_like(lab)
    for rank, piece in enumerate(order, 1):
        z[lab == piece] = rank
    scale = [[i / 4, COLS[i]] for i in range(5)]
    fig.add_trace(go.Heatmap(z=z, x=xs, y=ys, zmin=0, zmax=4, colorscale=[[v, col_] for v, col_ in
                  [(0, COLS[0]), (0.124, COLS[0]), (0.125, COLS[1]), (0.374, COLS[1]), (0.375, COLS[2]),
                   (0.624, COLS[2]), (0.625, COLS[3]), (0.874, COLS[3]), (0.875, COLS[4]), (1, COLS[4])]],
                  showscale=False, hoverinfo="skip"), row=1, col=col)
    k.room(fig, 1, col, walls=False)
    if d == 90:
        pick = lambda p: lab[int(round(p[1] / h)), int(round(p[0] / h))]
        assert pick(c.START[:2]) == pick(c.GOAL) != pick((6.6, 1.3))
        k.point(fig, *c.START[:2], GREEN, "start (2, 1)", "bottom center", row=1, col=col)
        k.point(fig, *c.GOAL, GREEN, None, row=1, col=col)
        fig.add_annotation(x=2.2, y=3.75, text="doorway (3.6, 4.0)", showarrow=False, font=dict(size=17, color=GREEN),
                           bgcolor="white", row=1, col=col)
        k.point(fig, 6.6, 1.3, RED, None, row=1, col=col)
        fig.add_annotation(x=6.6, y=0.35, text="(6.6, 1.3)", showarrow=False, font=dict(size=17, color=RED),
                           bgcolor="white", row=1, col=col)
        fig.add_annotation(x=5.39, y=3.28, ax=4.6, ay=3.75, xref="x2", yref="y2", axref="x2", ayref="y2",
                           text="sliver, 0.004 m²", font=dict(size=16), arrowhead=2, bgcolor="white")
    fig.update_xaxes(range=[-0.1, 7.1], dtick=1, title="x (m)", constrain="domain", row=1, col=col)
fig.update_yaxes(range=[-0.1, 4.1], dtick=1, title="y (m)", scaleanchor="x", constrain="domain", row=1, col=1)
fig.update_yaxes(range=[-0.1, 4.1], dtick=1, scaleanchor="x2", constrain="domain", row=1, col=2)
k.layout(fig, 1400, 560, margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(font_size=21, selector=dict(text="heading 0°: 2 pieces"))
fig.update_annotations(font_size=21, selector=dict(text="heading 90°: 3 pieces"))
fig.write_image(here / "components.png")
