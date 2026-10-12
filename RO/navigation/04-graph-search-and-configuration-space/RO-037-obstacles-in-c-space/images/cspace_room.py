"""Figure: the obstacle region of the whole room for the disk robot. Every obstacle grown by 0.25 m (orange); the
walls move 0.25 m into the room and the door jambs grow into quarter-disks, leaving 0.7 m of the 1.2 m doorway for
the centre. White is the free space. Run -> cspace_room.png"""
from pathlib import Path

import plotly.graph_objects as go
from shapely.geometry import box

import cspace as c
import drawkit as k
from gifkit import GREEN, ORANGE, RED

here = Path(__file__).parent
D = c.cobs_disk()
assert abs(c.door_gap(D) - 0.7) < 1e-3 and D.intersects(c.Point(*c.TEST)) and not D.intersects(c.Point(*c.GOAL))
fig = go.Figure()
k.room(fig)
ring = D.intersection(box(0, 0, c.W, c.H)).difference(c.obstacles())
fig.add_trace(k.geom_trace(ring, k.COBS_FILL, ORANGE, 2))
k.point(fig, *c.START[:2], GREEN, "start (2, 1)", "bottom center")
k.point(fig, *c.TEST, RED, None)
fig.add_annotation(x=3.1, y=3.32, text="(3.5, 3.2)", xanchor="right", showarrow=False, font=dict(size=18, color=RED),
                   bgcolor="white")
k.point(fig, *c.GOAL, GREEN, None)
fig.add_annotation(x=3.25, y=4.42, ax=3.95, ay=4.42, xref="x", yref="y", axref="x", ayref="y", text="",
                   arrowhead=2, arrowside="end+start", arrowwidth=2, arrowcolor=GREEN)
fig.add_annotation(x=3.6, y=4.62, text="free for the centre: 0.7 m of 1.2 m", showarrow=False,
                   font=dict(size=18, color=GREEN))
fig.add_annotation(x=3.6, y=3.62, text="doorway centre (3.6, 4.0)", showarrow=False, font=dict(size=16, color=GREEN),
                   bgcolor="white")
fig.add_annotation(x=4.0, y=0.45, text="walls moved in by 0.25 m", showarrow=False, font=dict(size=17, color=ORANGE),
                   bgcolor="white")
k.axes(fig, [-0.2, 7.2], [-0.2, 4.8])
k.layout(fig, 1100, 720)
fig.write_image(here / "cspace_room.png")
