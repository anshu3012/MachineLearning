"""Figure 1: the opening problem. The robot at (2 m, 1 m) facing 30 degrees drives straight ahead and its centre meets
the table's left edge after 1.35 m. Then the room's 0.5 m grid appears: 36 blocked cells (grey), 76 free, the start
cell S and the door's cell G. Run: python opening.py -> opening.gif, opening_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import GREY, ORANGE, RED, make_gif
from griddraw import axes, grid_lines, grid_trace, layout, lines_below, room_lines, start_goal
from robotdraw import robot
from roommap import POLE_R, POLES, ROBOT, TABLE_F
from roomsearch import BLOCKED, FREE

here = Path(__file__).parent
X, Y, TH = ROBOT
a, b, c = TABLE_F[3]                                   # the table's left edge: -4x + y + 11 = 0
HIT = -(a * X + b * Y + c) / (a * math.cos(TH) + b * math.sin(TH))
HX, HY = X + HIT * math.cos(TH), Y + HIT * math.sin(TH)
assert round(HIT, 2) == 1.35 and 1.0 <= HY <= 3.0
assert BLOCKED.sum() == 36 and len(FREE) == 76
PINK, GREENP = "#E377C2", "#54A24B"


def poles():
    out = []
    for name, (px, py) in POLES.items():
        t = np.linspace(0, 2 * np.pi, 40)
        out.append(go.Scatter(x=px + POLE_R * np.cos(t), y=py + POLE_R * np.sin(t), mode="lines", fill="toself",
                              line=dict(color=PINK if name == "pink" else GREENP, width=1), hoverinfo="skip"))
    return out


def frame(d, title, lines, grid=False, hit=False):
    fig = go.Figure()
    if grid:
        fig.add_trace(grid_trace())
        fig.add_trace(grid_lines())
    for t in room_lines() + poles():
        fig.add_trace(t)
    if d > 0:
        fig.add_trace(go.Scatter(x=[X, X + d * math.cos(TH)], y=[Y, Y + d * math.sin(TH)], mode="lines",
                                 line=dict(color=ORANGE, width=4, dash="dash"), hoverinfo="skip"))
    if not grid:
        for t in robot((X + d * math.cos(TH), Y + d * math.sin(TH), TH), scale=1.6):
            fig.add_trace(t)
    else:
        fig.add_trace(go.Scatter(x=[X], y=[Y], mode="markers", marker=dict(size=12, color="#4C78A8"),
                                 hoverinfo="skip"))
    if hit:
        fig.add_trace(go.Scatter(x=[HX], y=[HY], mode="markers", marker=dict(symbol="x", size=22, color=RED)))
    if grid:
        start_goal(fig)
    axes(fig)
    layout(fig, height=760, title=title, b=170, grid=grid)
    lines_below(fig, lines, y0=-0.14)
    return fig


figs, holds = [], []
figs.append(frame(0, "the robot at (2 m, 1 m), facing 30°; the goal: the door",
                  [("one idea: drive straight ahead", "black"), ("dashed orange: the path driven so far", ORANGE),
                   ("the robot is drawn 1.6 times its real size so that it shows", GREY)]))
holds.append(10)
for d in np.linspace(0.2, HIT, 7):
    figs.append(frame(d, f"driving straight ahead: {d:.2f} m", [("one idea: drive straight ahead", "black")],
                      hit=abs(d - HIT) < 1e-9))
    holds.append(2)
figs.append(frame(HIT, f"after {HIT:.2f} m its centre meets the table's edge",
                  [("driving where it faces does not reach the door", RED),
                   ("the map knows where the table is, but gives no route", "black")], hit=True))
holds.append(14)
figs.append(frame(0, "the map as a grid: 112 cells of 0.5 m",
                  [("grey: 36 blocked cells (some furniture or a pole inside); white: 76 free cells", GREY),
                   ("S: the start cell, with the robot (blue dot) on its corner; G: the cell under the door", "black"),
                   ("which free cells, in which order, lead from S to G?", "black")], grid=True))
holds.append(30)
make_gif(figs, here / "opening.gif", fps=5, holds=holds, keys=[0, 8, 9], cols=3, width=900)
print(f"hit after {HIT:.3f} m at ({HX:.3f}, {HY:.3f})")
