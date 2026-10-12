"""Figure: the room in C-space (obstacles grown by the robot's 0.25 m radius, orange) and the robot's four trips of
the day: 1 dock to door, 2 door to cabinet, 3 cabinet to corner, 4 corner to dock, drawn as numbered arrows from
start to end (not routes). Run -> trips.png"""
from pathlib import Path

import numpy as np

import drawkit as dk
import prm
import prmdraw as pd
from gifkit import GREY

here = Path(__file__).parent
w = prm.World()
assert all(w.free(q, False) for _, s, _, g in prm.TRIPS for q in (s, g))
fig = pd.base(w)
dk.disk(fig, *prm.START, np.radians(30))
names = {"dock": (prm.START, "bottom left"), "door": (prm.DOOR, "middle right"),
         "cabinet": (prm.CABINET, "middle left"), "corner": (prm.CORNER, "bottom center")}
for i, (a, s, b, g) in enumerate(prm.TRIPS):
    sx, sy = s
    gx, gy = g
    fig.add_annotation(x=gx, y=gy, ax=sx, ay=sy, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=3, arrowsize=1.6, arrowwidth=2.5, arrowcolor=GREY, standoff=9, startstandoff=9)
    mx, my = (sx + gx) / 2, (sy + gy) / 2
    off = {0: (-0.22, 0.0), 1: (0.18, 0.18), 2: (0.25, 0.1), 3: (0.0, -0.22)}[i]
    fig.add_annotation(x=mx + off[0], y=my + off[1], text=f"<b>{i + 1}</b>", showarrow=False,
                       font=dict(size=22, color="black"), bgcolor="white")
for name, (q, pos) in names.items():
    pd.place(fig, q, name, pos=pos)
pd.panel(fig, [("four trips a day", "black"), ("in one unchanged room:", "black"), ("", "black"),
               ("1  dock to door", "black"), ("2  door to cabinet", "black"), ("3  cabinet to corner", "black"),
               ("4  corner to dock", "black"), ("", "black"), ("orange: obstacles grown", "#C46A10"),
               ("by the robot's 0.25 m radius", "#C46A10"), ("arrows: start to end, not routes", GREY)])
pd.finish(fig, "Four trips in one room")
fig.write_image(here / "trips.png", scale=1)
