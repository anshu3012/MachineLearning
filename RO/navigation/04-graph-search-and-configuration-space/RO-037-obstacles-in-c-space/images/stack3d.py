"""Figure: slices stacked into C-space (x, y, heading). Left: the table's obstacle region for the board, one outline
every 10 degrees of heading from 0 to 360; the slices turn and change shape, so the region is a twisted column.
Right: the same for the disk robot; every slice is the table grown by 0.25 m, so the column is straight.
Run -> stack3d.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from shapely.geometry import Polygon

import cspace as c
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
T = Polygon(c.TABLE)
fig = make_subplots(rows=1, cols=2, specs=[[{"type": "scene"}, {"type": "scene"}]], horizontal_spacing=0.02,
                    subplot_titles=["board: the slices turn and change shape", "disk: every slice is the same"])
for col, slice_of in [(1, lambda th: c.cobs_board_piece(T, th)), (2, lambda th: T.buffer(c.R, quad_segs=32))]:
    for d in range(0, 361, 10):
        x, y = slice_of(np.radians(d)).exterior.xy
        fig.add_trace(go.Scatter3d(x=list(x), y=list(y), z=[d] * len(x), mode="lines",
                                   line=dict(color=ORANGE, width=4 if d % 90 else 9), hoverinfo="skip"),
                      row=1, col=col)
    tx, ty = zip(*(c.TABLE + [c.TABLE[0]]))
    for z in (0, 360):
        fig.add_trace(go.Scatter3d(x=tx, y=ty, z=[z] * 5, mode="lines", line=dict(color=BLUE, width=6),
                                   hoverinfo="skip"), row=1, col=col)
ax = dict(tickfont=dict(size=15), title_font=dict(size=18))
scene = dict(xaxis=dict(title="x (m)", range=[1.5, 7], dtick=1, **ax),
             yaxis=dict(title="y (m)", range=[-0.5, 4.5], dtick=1, **ax),
             zaxis=dict(title="heading θ (°)", range=[0, 360], tickvals=[0, 90, 180, 270, 360], **ax),
             aspectmode="manual", aspectratio=dict(x=1.1, y=0.9, z=1.2),
             camera=dict(eye=dict(x=1.5, y=-1.9, z=1.0)))
fig.update_layout(scene=scene, scene2=scene, template="simple_white", width=1300, height=760, font=FONT,
                  showlegend=False, margin=dict(l=10, r=10, t=60, b=10))
fig.update_annotations(font_size=21)
fig.write_image(here / "stack3d.png")
