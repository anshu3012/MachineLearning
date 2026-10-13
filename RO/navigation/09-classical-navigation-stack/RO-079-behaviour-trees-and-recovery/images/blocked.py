"""The blocked door at 3.01 s (btkit.results()["blocked"]): the robot (black) on its way to the door pose (cross),
its path (blue) from 0.01 s, the person (pink) who stopped at 2.4 s in the gap between the table's corner and the
wall, and the trolley (brown) between the table and the cabinet. The four gaps, measured with shapely, are all
narrower than the robot (0.50 m). Run -> blocked.png"""
from pathlib import Path

import bandkit as bk
import btkit as bt
import navdraw as nd
import plotly.graph_objects as go
from gifkit import FONT, RED
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import nearest_points

here = Path(__file__).parent
R = bt.results()["blocked"]
rec = nd.at(R["records"], 3.01)
assert rec["person"] is not None and [c for t, c in R["planned"] if t == 3.02] == ["NO_VALID_PATH"]
P = Point(*bt.GAP_PERSON).buffer(bk.PERSON_R, 128)
pairs = [(LineString([(0, 4), (3.0, 4)]), P), (P, Polygon(bk.TABLE)), (Polygon(bt.TROLLEY), Polygon(bk.TABLE)),
         (Polygon(bt.TROLLEY), box(5.6, 3.4, 7.0, 4.0))]
gaps = [(a.distance(b), nearest_points(a, b)) for a, b in pairs]
assert [round(g, 2) for g, _ in gaps] == [0.30, 0.47, 0.11, 0.10]

fig = go.Figure()
nd.room(fig, trolley=True, person=rec["person"])
nd.goal(fig, bt.GOAL)
nd.track(fig, R["records"], 3.01)
nd.path(fig, rec["path"])
nd.robot(fig, *rec["robot"])
for (g, (p, q)), (dx, dy, anchor) in zip(gaps, [(-0.55, 0.05, "right"), (-0.05, -0.42, "right"),
                                                 (-0.3, -0.38, "right"), (0.35, 0.28, "left")]):
    fig.add_trace(go.Scatter(x=[p.x, q.x], y=[p.y, q.y], mode="lines+markers", line=dict(color=RED, width=3),
                             marker=dict(size=6, color=RED)))
    mx, my = (p.x + q.x) / 2, (p.y + q.y) / 2
    fig.add_annotation(x=mx, y=my, ax=mx + dx, ay=my + dy, axref="x", ayref="y", text=f"<b>{g:.2f} m</b>",
                       showarrow=True, arrowhead=0, arrowcolor=RED, xanchor=anchor, font=dict(size=19, color=RED))
fig.add_annotation(x=0.15, y=0.25, text="robot: 0.50 m wide; every gap is narrower", showarrow=False, xanchor="left",
                   font=dict(size=19, color=RED))
fig.add_annotation(x=bt.GAP_PERSON[0] - 0.25, y=bt.GAP_PERSON[1] - 0.05, text="person", showarrow=False,
                   xanchor="right", font=dict(size=17))
fig.add_annotation(x=6.08, y=2.97, text="trolley", showarrow=False, font=dict(size=17))
fig.update_xaxes(range=[-0.05, 7.05], visible=False)
fig.update_yaxes(range=[-0.05, 4.3], visible=False, scaleanchor="x", scaleratio=1)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=640, showlegend=False,
                  margin=dict(l=8, r=8, t=8, b=8))
fig.write_image(here / "blocked.png")
print("gaps", [round(g, 3) for g, _ in gaps], "; robot at 3.01 s", rec["robot"].round(2))
