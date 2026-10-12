"""The lattice path (blue, 42.93 m, 629 expansions) and Hybrid A*'s path of RO-055 (green, 39.42 m, 312 expansions
with the Reeds-Shepp shot) on the same lot, from the same start to the same goal. Run -> compare.png"""
import math
from pathlib import Path

from carkit import GOAL, START, hybrid_astar
from gifkit import BLUE, GREEN
from latticekit import lattice_astar
from lotdraw import axes, car, label, layout, lot, path
from plotly.subplots import make_subplots

here = Path(__file__).parent
L = lattice_astar()
H = hybrid_astar("max", shot=True)
assert round(L["length"], 2) == 42.93 and L["expanded"] == 629 and round(H["length"], 2) == 39.42 and H["expanded"] == 312
fig = make_subplots(rows=1, cols=1)
lot(fig, (1, 1))
path(fig, H["poses"][:, :2], (1, 1), colour=GREEN, width=4)
path(fig, L["poses"][:, :2], (1, 1), colour=BLUE, width=4)
car(fig, START, (1, 1), colour="#2E7D32", width=2)
car(fig, GOAL, (1, 1), colour="#F58518", fill="rgba(0,0,0,0)", width=2)
label(fig, 20.6, 4.0, "lattice<br>42.93 m", (1, 1), size=17, colour=BLUE)
label(fig, 9.0, 13.8, "Hybrid A*<br>39.42 m", (1, 1), size=17, colour=GREEN)
axes(fig, (1, 1))
layout(fig, "the lattice path and Hybrid A*'s path", width=820, height=860,
       subtitle="same lot, same start, same goal")
fig.write_image(here / "compare.png")
