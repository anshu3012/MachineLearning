"""The guess of the distance left, h, in every free cell of the left part of the room: the octile distance to the goal
cell G, the length of the shortest 8-connected route if there were no obstacles (diagonal moves first, then straight
ones). From the start cell S it is 3.121 m: the dotted route, 3 diagonal moves and 2 straight moves, which runs
through the table's cells. The dashed line is the straight-line distance, 2.915 m. The true shortest route is
3.414 m. Run -> heuristic.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, centre, layout, room, route, sg
from gifkit import GREEN, ORANGE, PURPLE
from searchkit import BLOCKED, GOAL, START, dist_from, octile, straight

here = Path(__file__).parent
XR, YR = (0, 11), (0, 8)
assert round(octile(START), 3) == 3.121 and round(straight(START), 3) == 2.915
assert round(dist_from(GOAL)[START], 3) == 3.414
assert round(3 * 0.707 + 2 * 0.5, 3) == 3.121
fig = go.Figure()
room(fig, None, {}, xr=XR, yr=YR, labels=False)
for j in range(*YR):
    for i in range(*XR):
        if not BLOCKED[j, i] and (i, j) not in (START, GOAL):
            x, y = centre((i, j))
            fig.add_annotation(x=x, y=y, text=f"{octile((i, j)):.3f}", showarrow=False, bgcolor="white",
                               font=dict(size=17, color="#1F3F66"))
octile_route = [START, (5, 3), (6, 4), (7, 5), (7, 6), GOAL]
route(fig, octile_route, colour=PURPLE, width=4, dash="dot")
route(fig, [START, GOAL], colour=ORANGE, width=4, dash="dash")
sg(fig, xr=XR, yr=YR)
x, y = centre((6, 4))
fig.add_annotation(x=x + 0.05, y=y - 0.12, text="octile route: 3.121 m,<br>through the table's cells", showarrow=False,
                   xanchor="left", font=dict(size=17, color=PURPLE), bgcolor="white")
axes(fig, None, XR, YR)
layout(fig, "the heuristic h in each free cell: octile distance to G, in m<br><span style='font-size:18px'>"
       "<span style='color:#B279A2'>dotted: the octile route from S, 3.121 m</span>; "
       "<span style='color:#F58518'>dashed: the straight line, 2.915 m</span></span>", width=1000, height=820,
       margin=dict(l=30, r=30, t=95, b=30))
fig.write_image(here / "heuristic.png")
