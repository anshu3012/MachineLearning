"""Why Hybrid A* keeps one pose per cell and heading range: three ways of driving two arcs from the start, left then
right, right then left, straight then straight, all end facing 0 deg in the cell centred on (5, 3), at three
different points. Hybrid A* keeps only one of them. Run -> merge.png"""
from pathlib import Path

from carkit import START, arc, key_of
from gifkit import BLUE, ORANGE, PURPLE
from lotdraw import axes, label, layout, lot, path
from plotly.subplots import make_subplots

here = Path(__file__).parent
fig = make_subplots(rows=1, cols=1)
runs = {}
for a, b, col in (("L", "R", BLUE), ("R", "L", PURPLE), ("S", "S", ORANGE)):
    t1 = arc(START, 1, a)
    t2 = arc(tuple(t1[-1]), 1, b)
    runs[a + b] = (t1, t2, col)
keys = {key_of(tuple(t2[-1])) for t1, t2, _ in runs.values()}
assert keys == {(5, 3, 0)}
lot(fig, (1, 1), grid=True, cells={(5, 3): "rgba(245,133,24,0.22)"}, xr=(1, 7), yr=(1.5, 5))
names = {"LR": "left, then right", "RL": "right, then left", "SS": "straight, then straight"}
for k, (t1, t2, col) in runs.items():
    path(fig, t1[:, :2], (1, 1), colour=col, width=4)
    path(fig, t2[:, :2], (1, 1), colour=col, width=4)
    x, y = t2[-1][:2]
    path(fig, [(x, y)], (1, 1), colour=col, mode="markers", size=13)
    label(fig, x + 0.6, y + {"LR": 0.35, "RL": -0.35, "SS": 0.0}[k], f"({x:.3f}, {y:.3f})", (1, 1), size=15,
          colour=col, anchor="right")
    label(fig, 1.3, {"LR": 4.75, "SS": 4.4, "RL": 4.05}[k], names[k], (1, 1), size=16, colour=col, anchor="right")
label(fig, 2.0, 3.0, "start", (1, 1), size=15)
axes(fig, (1, 1), xr=(1, 7), yr=(1.5, 5))
layout(fig, "three poses, one cell, one heading range", width=820, height=640,
       subtitle="all end in the cell centred on (5, 3) facing 0 deg; Hybrid A* keeps one")
fig.write_image(here / "merge.png", scale=1)
