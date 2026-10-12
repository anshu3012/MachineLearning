"""Figure 1: the opening problem. Left: the room with the robot's 0.25 m disk footprint at the start (2, 1) facing 30
degrees and a second placement with its centre at (3.5, 3.2), outside the table but with the disk overlapping it.
Right: zoom on the table's top-left corner (3.5, 3.0): the centre is 0.2 m away, so the disk overlaps by 0.05 m.
Run -> problem.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from shapely.geometry import Point, Polygon

import cspace as c
import drawkit as k
from gifkit import GREEN, RED

here = Path(__file__).parent
T = Polygon(c.TABLE)
d = T.distance(Point(*c.TEST))
assert round(d, 3) == 0.2 and round(c.R - d, 3) == 0.05

fig = make_subplots(rows=1, cols=2, column_widths=[0.64, 0.36], horizontal_spacing=0.07,
                    subplot_titles=["the room: is each placement free?", "zoom at the table's corner"])
for col in (1, 2):
    k.room(fig, 1, col)
    k.disk(fig, *c.START, row=1, col=col)
    k.disk(fig, *c.TEST, np.radians(30), row=1, col=col, color=RED)
overlap = c.circle(*c.TEST, c.R).intersection(T)
fig.add_trace(k.geom_trace(overlap, "rgba(228,87,86,0.8)", RED, 1), row=1, col=2)
k.point(fig, *c.START[:2], GREEN, None, row=1, col=1, size=10)
fig.add_annotation(x=2.0, y=0.55, text="start (2, 1)", showarrow=False, font=dict(size=18, color=GREEN), row=1, col=1)
k.point(fig, *c.TEST, RED, None, row=1, col=1, size=10)
fig.add_annotation(x=3.15, y=3.2, text="centre (3.5, 3.2)", xanchor="right", showarrow=False, font=dict(size=18, color=RED), row=1, col=1)
fig.add_annotation(x=3.6, y=4.45, text="doorway 1.2 m", showarrow=False, font=dict(size=18), row=1, col=1)
fig.add_annotation(x=3.0, y=4.25, ax=4.2, ay=4.25, xref="x", yref="y", axref="x", ayref="y", text="",
                   arrowhead=2, arrowside="end+start", arrowwidth=2)
# zoom labels
k.point(fig, *c.TEST, RED, None, row=1, col=2, size=10)
k.point(fig, 3.5, 3.0, "black", None, row=1, col=2, size=9)
fig.add_trace(go.Scatter(x=[3.5, 3.5], y=[3.0, 3.2], mode="lines", line=dict(color="black", width=3),
                         hoverinfo="skip"), row=1, col=2)
fig.add_annotation(x=3.47, y=3.1, text="0.2 m", xanchor="right", bgcolor="white", showarrow=False, font=dict(size=18), row=1, col=2)
fig.add_annotation(x=3.5, y=3.47, text="centre (3.5, 3.2): outside the table", showarrow=False,
                   font=dict(size=17, color=RED), row=1, col=2)
fig.add_annotation(x=3.5, y=2.62, text="disk reaches 0.25 m:<br>overlaps the table by 0.05 m", showarrow=False, bgcolor="white",
                   font=dict(size=17, color=RED), row=1, col=2)
fig.add_annotation(x=3.32, y=2.86, text="corner (3.5, 3.0)", showarrow=False, xanchor="right",
                   font=dict(size=16), row=1, col=2)
fig.update_xaxes(range=[-0.2, 7.2], dtick=1, title="x (m)", row=1, col=1)
fig.update_yaxes(range=[-0.2, 4.7], dtick=1, title="y (m)", scaleanchor="x", row=1, col=1)
fig.update_xaxes(range=[3.0, 4.0], dtick=0.25, title="x (m)", row=1, col=2)
fig.update_yaxes(range=[2.45, 3.6], dtick=0.25, scaleanchor="x2", row=1, col=2)
k.layout(fig, 1350, 560, margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(selector=dict(text="the room: is each placement free?"), font_size=21)
fig.update_annotations(selector=dict(text="zoom at the table's corner"), font_size=21)
fig.write_image(here / "problem.png", scale=1)
