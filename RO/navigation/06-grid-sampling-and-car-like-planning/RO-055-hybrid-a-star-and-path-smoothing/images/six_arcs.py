"""The first expansion of Hybrid A*: the six arcs of 1.5 m from the start pose (2, 3) facing 0 deg. Forward: left,
straight, right (blue), each turning 17.2 deg on the 5 m circle or not at all; their end poses and 1 m cells. Reverse:
all three put the rear bumper through the left wall (red; the body at the end of the straight reverse arc is drawn).
Run -> six_arcs.png"""
import math
from pathlib import Path

from carkit import PRIMS, START, arc, collides, key_of
from gifkit import BLUE, RED
from lotdraw import axes, car, label, layout, lot, path
from plotly.subplots import make_subplots

here = Path(__file__).parent
fig = make_subplots(rows=1, cols=1)
ends = {}
for d, k in PRIMS:
    tr = arc(START, d, k)
    ends[(d, k)] = (tr, bool(collides(tr).any()))
cells = {key_of(tuple(tr[-1]))[:2]: "rgba(76,120,168,0.18)" for (d, k), (tr, hit) in ends.items() if not hit}
lot(fig, (1, 1), grid=True, cells=cells, xr=(0, 11), yr=(0, 6))
car(fig, START, (1, 1), colour="#2E7D32", fill="rgba(0,0,0,0)", width=1.5, arrow=False)
car(fig, tuple(ends[(-1, "S")][0][-1]), (1, 1), colour=RED, fill="rgba(0,0,0,0)", width=1.5, arrow=False)
names = {"L": "left", "S": "straight", "R": "right"}
for (d, k), (tr, hit) in ends.items():
    path(fig, tr[:, :2], (1, 1), colour=RED if hit else BLUE, width=4)
    x, y, th = tr[-1]
    if not hit:
        path(fig, [(x, y), (x + 0.7 * math.cos(th), y + 0.7 * math.sin(th))], (1, 1), colour=BLUE, width=3)
        cell = key_of(tuple(tr[-1]))
        yl = 3 + {"L": 1.0, "S": 0.0, "R": -1.0}[k]
        path(fig, [(x + 0.75, y), (6.3, yl)], (1, 1), colour=BLUE, width=1, dash="dot")
        label(fig, 6.4, yl, f"{names[k]}: ({x:.3f}, {y:.3f}), {math.degrees(th):+.1f} deg", (1, 1), size=15,
              colour=BLUE, anchor="right")
label(fig, 2.6, 5.2, "reverse arcs (red): the rear<br>bumper goes through the wall", (1, 1), size=16, colour=RED)
label(fig, 3.2, 1.5, "body at the start (green) and after<br>the straight reverse arc (red)", (1, 1), size=15)
assert all(hit for (d, k), (tr, hit) in ends.items() if d < 0) and not any(hit for (d, k), (tr, hit) in ends.items() if d > 0)
assert [round(v, 3) for v in ends[(1, "L")][0][-1][:2]] == [3.478, 3.223]
axes(fig, (1, 1), xr=(0, 11), yr=(0, 6))
layout(fig, "the six arcs of the first expansion", width=900, height=620,
       subtitle="each arc is 1.5 m long; a turning arc follows the 5 m circle")
fig.write_image(here / "six_arcs.png", scale=1)
