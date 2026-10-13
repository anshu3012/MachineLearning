"""Animation: one service call. The localizer starts and needs the room's map once. It sends a request on the map
server's service map_server/map (type nav_msgs/srv/GetMap: an empty request, a reply holding an occupancy grid) and
waits; the map server answers with the map, 140 x 80 cells of 0.05 m, 11,200 numbers; the localizer has the map.
Right: the reply's map, black where a cell holds a wall, the table, the cabinet or a pole.
Run -> service.gif, service_frames.png"""
from pathlib import Path

import bandkit as bk
import netdraw as nd
import numpy as np
import plotly.graph_objects as go
import roskit as rk
from gifkit import BLUE, GREY, PURPLE, make_gif

here = Path(__file__).parent
nx, ny = rk.MAP_CELLS
assert (nx, ny) == (140, 80) and nx * ny == 11200
xc = (np.arange(nx) + 0.5) * rk.MAP_RES
yc = (np.arange(ny) + 0.5) * rk.MAP_RES
X, Y = np.meshgrid(xc, yc)
D = np.min([o(X, Y) for o in bk.obstacles(None)], axis=0)
GRID = (D <= rk.MAP_RES / 2 + 1e-9).astype(int)            # 1 = occupied: the cell's centre is within half a cell of an obstacle
CLIENT, SERVER = (0.16, 0.62), (0.50, 0.62)
REQ = ((0.26, 0.655), (0.40, 0.655))
REP = ((0.40, 0.585), (0.26, 0.585))
STEPS = [
    ("the localizer starts and needs the map once", "client", None, False),
    ("request on map_server/map (nothing in it); the localizer waits", "client", "req", False),
    ("the map server handles the request", "server", None, False),
    ("reply: the map, 140 x 80 cells of 0.05 m", "server", "rep", False),
    ("the localizer has the map and continues its work", "client", None, True),
]


def frame(i):
    what, who, msg, done = STEPS[i]
    fig = nd.blank()
    nd.box(fig, *CLIENT, "localizer", BLUE, lit=who == "client", w=0.19, h=0.1, size=22,
           sub="waiting for the reply" if i in (1, 2, 3) else ("has the map" if done else "service client"))
    nd.box(fig, *SERVER, "map server", BLUE, lit=who == "server", w=0.19, h=0.1, size=22, sub="service server")
    nd.arrow(fig, *REQ, PURPLE if msg == "req" else "#BBBBBB", width=5 if msg == "req" else 2)
    nd.arrow(fig, *REP, PURPLE if msg == "rep" else "#BBBBBB", width=5 if msg == "rep" else 2)
    nd.text(fig, 0.33, 0.70, "request", size=19, color=PURPLE, anchor="center", valign="bottom")
    nd.text(fig, 0.33, 0.54, "reply", size=19, color=PURPLE, anchor="center", valign="top")
    if msg == "req":
        nd.dot(fig, nd.lerp(*REQ, 0.5), PURPLE)
    if msg == "rep":
        nd.dot(fig, nd.lerp(*REP, 0.5), PURPLE)
    nd.text(fig, 0.02, 0.97, f"<b>step {i + 1} of 5</b><br>{what}", size=22)
    nd.text(fig, 0.02, 0.36, "<b>nav_msgs/srv/GetMap</b><br># request: nothing<br>---<br># reply:<br>"
            "OccupancyGrid map", size=19, color=GREY)
    if done or msg == "rep":
        fig.add_trace(go.Heatmap(z=GRID, x=xc, y=yc, colorscale=[[0, "white"], [1, "black"]], showscale=False,
                                 xaxis="x2", yaxis="y2"))
        fig.update_layout(xaxis2=dict(domain=[0.64, 0.99], anchor="y2", range=[0, 7], visible=False,
                                      constrain="domain"),
                          yaxis2=dict(domain=[0.33, 0.621], anchor="x2", range=[0, 4], visible=False))
        nd.text(fig, 0.815, 0.30, "the reply's map: 11,200 cells", size=19, anchor="center")
    return fig


figs = [frame(i) for i in range(len(STEPS))]
make_gif(figs, here / "service", fps=1, holds=[3, 3, 3, 3, 6], keys=[1, 2, 3, 4], cols=2, width=900)
