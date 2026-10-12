"""Figure: a distance query. Left, the room: the robot at the start (2, 1) is 0.75 m from the table (nearest point:
the table's corner (3.0, 1.0)) and 0.75 m from the bottom wall. Right: the same answer from the Minkowski difference
robot minus table, every robot point minus every table point. It does not contain the origin, so the two do not
touch, and its nearest point to the origin, (-0.75, 0), gives the distance 0.75 m. That point is the robot's farthest
point in the direction v = (1, 0) minus the table's farthest point in the direction -v. Run -> distance.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from shapely.geometry import Point, Polygon

import collide as k
import cspace as c
import drawkit as dk
from gifkit import BLUE, GREEN, ORANGE, RED

here = Path(__file__).parent
T = Polygon(c.TABLE)
s = np.array(c.START[:2])
assert round(k.clearance(s), 3) == 0.75 and round(T.distance(Point(*s)) - c.R, 3) == 0.75
Dm = Polygon([tuple(s - np.array(p)) for p in c.TABLE]).buffer(c.R, quad_segs=64)      # robot minus table
assert round(Dm.distance(Point(0, 0)), 3) == 0.75 and not Dm.contains(Point(0, 0))
sup_r = s + c.R * np.array([1.0, 0.0])                                                  # robot's support in d
sup_t = np.array(max(c.TABLE, key=lambda p: -p[0]))                                     # table's support in -d
assert tuple(sup_t) == (3.0, 1.0)
fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.08,
                    subplot_titles=["the room: how far is the robot from the table?",
                                    "robot minus table: how far from the origin?"])
dk.room(fig, 1, 1)
dk.disk(fig, *c.START, row=1, col=1)
fig.add_trace(go.Scatter(x=[sup_r[0], 3.0], y=[1.0, 1.0], mode="lines+markers", line=dict(color=RED, width=4),
                         marker=dict(size=9, color=RED)), row=1, col=1)
fig.add_annotation(x=2.62, y=1.22, text="0.75 m", showarrow=False, font=dict(size=18, color=RED), row=1, col=1)
fig.add_trace(go.Scatter(x=[2.0, 2.0], y=[0.75, 0.0], mode="lines", line=dict(color=RED, width=4)), row=1, col=1)
fig.add_annotation(x=2.08, y=0.38, text="0.75 m", xanchor="left", showarrow=False, font=dict(size=18, color=RED),
                   row=1, col=1)
fig.add_trace(dk.geom_trace(Dm, "rgba(245,133,24,0.25)", ORANGE, 3), row=1, col=2)
dk.point(fig, 0, 0, "black", None, size=12, row=1, col=2)
fig.add_annotation(x=0.08, y=0.22, text="origin", xanchor="left", showarrow=False, font=dict(size=18), row=1, col=2)
fig.add_trace(go.Scatter(x=[-0.75, 0], y=[0, 0], mode="lines", line=dict(color=RED, width=4)), row=1, col=2)
dk.point(fig, -0.75, 0, RED, None, size=12, row=1, col=2)
fig.add_annotation(x=-0.3, y=0.6, text="(−0.75, 0) = (2.25, 1) − (3.0, 1.0)", xanchor="right", showarrow=False,
                   font=dict(size=17, color=RED), bgcolor="white", row=1, col=2)
fig.add_annotation(x=0.6, y=-0.6, ax=0.0, ay=-0.6, xref="x2", yref="y2", axref="x2", ayref="y2", text="",
                   arrowhead=2, arrowwidth=3, arrowcolor=GREEN)
fig.add_annotation(x=0.32, y=-0.85, text="v = (1, 0)", showarrow=False, font=dict(size=17, color=GREEN), row=1, col=2)
fig.add_annotation(x=-2.2, y=-0.9, text="every robot point<br>minus every table point", showarrow=False,
                   font=dict(size=17, color=ORANGE), row=1, col=2)
fig.update_xaxes(range=[-0.2, 7.2], dtick=1, title="x (m)", row=1, col=1)
fig.update_yaxes(range=[-0.2, 4.3], dtick=1, title="y (m)", scaleanchor="x", row=1, col=1)
fig.update_xaxes(range=[-4.0, 1.0], dtick=1, title="x (m)", zeroline=True, row=1, col=2)
fig.update_yaxes(range=[-2.5, 1.0], dtick=1, scaleanchor="x2", zeroline=True, row=1, col=2)
dk.layout(fig, 1350, 560, margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(font_size=20, selector=dict(text="the room: how far is the robot from the table?"))
fig.update_annotations(font_size=20, selector=dict(text="robot minus table: how far from the origin?"))
fig.write_image(here / "distance.png")
