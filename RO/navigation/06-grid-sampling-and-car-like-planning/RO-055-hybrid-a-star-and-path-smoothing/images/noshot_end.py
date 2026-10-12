"""Hybrid A* without the shot stops at the first pose that lands in the goal's cell with its heading within 10 deg:
here (11.684, 22.562) facing 275 deg, 0.54 m and 5 deg from the goal (12, 23, 270 deg). Zoom on the target bay.
Run -> noshot_end.png"""
import math
from pathlib import Path

from carkit import GOAL, hybrid_astar
from gifkit import BLUE
from lotdraw import axes, car, label, layout, lot, path
from plotly.subplots import make_subplots

here = Path(__file__).parent
R = hybrid_astar("max", shot=False)
end = R["poses"][-1]
miss = math.hypot(end[0] - GOAL[0], end[1] - GOAL[1])
turn = math.degrees(abs(math.remainder(end[2] - GOAL[2], 2 * math.pi)))
assert R["expanded"] == 1949 and round(miss, 2) == 0.54 and round(turn) == 5
fig = make_subplots(rows=1, cols=1)
lot(fig, (1, 1), grid=True, cells={(12, 23): "rgba(245,133,24,0.25)"}, xr=(7, 17), yr=(14, 24))
path(fig, R["poses"][:, :2], (1, 1), colour=BLUE, width=3)
car(fig, GOAL, (1, 1), colour="#F58518", fill="rgba(0,0,0,0)", width=2.5)
car(fig, tuple(end), (1, 1))
label(fig, 15.2, 18.2, f"stops {miss:.2f} m and {turn:.0f} deg<br>from the goal (orange)", (1, 1), size=17)
axes(fig, (1, 1), xr=(7, 17), yr=(14, 24))
layout(fig, f"without the shot: {R['expanded']} expansions", width=820, height=820,
       subtitle="the search stops in the goal's cell, heading within 10 deg")
fig.write_image(here / "noshot_end.png", scale=1)
