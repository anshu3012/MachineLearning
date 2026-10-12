"""What each guess of the cost left imagines from the start (2, 3, 0 deg) to the goal (12, 23, -90 deg): the straight
line, 22.36 m, through everything and ignoring the heading; the shortest Reeds-Shepp path, 27.31 m, which turns the
car correctly but drives through the middle row of parked cars; the shortest grid route, 33.31 m, around the middle
row but with corners and no heading. Run -> guesses.png"""
from pathlib import Path

import numpy as np
from carkit import GOAL, RHO, START, grid_astar, h_euclid, h_grid, reeds_shepp, rs_length, sample
from carpaths import length
from gifkit import BLUE, GREY, PURPLE
from lotdraw import axes, car, label, layout, lot, path
from plotly.subplots import make_subplots

here = Path(__file__).parent
rs = reeds_shepp(START, GOAL, RHO)
assert round(length(rs), 2) == round(rs_length(START), 2) == 27.31
assert round(h_euclid(START), 2) == 22.36 and round(h_grid(START), 2) == 33.31
fig = make_subplots(rows=1, cols=1)
lot(fig, (1, 1))
path(fig, [START[:2], GOAL[:2]], (1, 1), colour=GREY, width=3, dash="dot")
path(fig, sample(START, rs, RHO)[:, :2], (1, 1), colour=PURPLE, width=4)
path(fig, np.array(grid_astar()["path"], float), (1, 1), colour=BLUE, width=4)
car(fig, START, (1, 1), colour="#2E7D32", width=2)
car(fig, GOAL, (1, 1), colour="#F58518", fill="rgba(0,0,0,0)", width=2)
label(fig, 19.5, 5.2, "grid distance 33.31 m<br>(around the middle row)", (1, 1), size=16, colour=BLUE)
label(fig, 3.6, 17.0, "Reeds-Shepp<br>27.31 m<br>(through the<br>middle row)", (1, 1), size=16, colour=PURPLE)
label(fig, 10.6, 14.2, "straight line<br>22.36 m", (1, 1), size=16, colour=GREY)
axes(fig, (1, 1))
layout(fig, "three guesses of the distance left, from the start", width=820, height=860,
       subtitle="each guess ignores something: obstacles, the heading, or both")
fig.write_image(here / "guesses.png", scale=1)
