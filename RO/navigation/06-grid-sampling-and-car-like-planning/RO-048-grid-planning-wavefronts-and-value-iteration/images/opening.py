"""The problem of the Note, on the room grid. A* plans one route from S to the door's cell G, 3.414 m. The robot sets off
along it, but its first diagonal move falls one cell short and it lands below the route: the route says nothing about
that cell, so A* must search again (7 cells, a 3.207 m route). The last frame shows the answer this Note builds: one
wavefront from the door gives every free cell an arrow towards the door, so no cell ever needs a new search.
Run -> opening.gif, opening_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import arrows, axes, centre, layout, robot, room, route, sg
from gifkit import BLUE, ORANGE, RED, make_gif
from gridplan import CELLS, GOAL, START, cost_to_go, downhill, path_cost
from searchkit import astar

here = Path(__file__).parent
A = astar()
SLIP = (5, 2)
B = astar(start=SLIP)
V = cost_to_go()
NEXT = {c: downhill(c, V)[1] for c in CELLS if c != GOAL}
assert A["path"] == downhill(START, V) and round(A["cost"], 3) == 3.414 and len(A["order"]) == 9
assert SLIP not in A["path"] and len(B["order"]) == 7 and round(B["cost"], 3) == 3.207
assert sum(len(astar(start=c)["order"]) for c in CELLS) == 902 and len(V) == 76
a, b = centre(START), centre(A["path"][1])
s = centre(SLIP)


def frame(k):
    fig = go.Figure()
    st = {c: "closed" for c in B["order"]} if k in (4, 5) else {}
    room(fig, None, st, labels=False)
    if k < 6:
        route(fig, A["path"], BLUE, width=6, dash="dot" if k >= 3 else None)
    if k == 0:
        robot(fig, a)
        t = "A* plans one route from S to the door: 3.414 m"
    elif k == 1:
        robot(fig, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 0.08))
        t = "the robot sets off along the route"
    elif k == 2:
        robot(fig, s)
        arrows(fig, [(b, s)], colour=ORANGE, width=3, size=1.4, frac=0.9)
        t = "a slip: it lands one cell lower, off the route"
    elif k == 3:
        robot(fig, s, colour=RED)
        t = "the route says nothing about this cell"
    elif k == 4:
        robot(fig, s, colour=RED)
        t = "so A* searches again from here: 7 cells"
    elif k == 5:
        route(fig, B["path"], BLUE, width=6)
        robot(fig, s)
        t = "a new route, 3.207 m; every slip means another search"
    else:
        arrows(fig, [(centre(c), centre(n)) for c, n in NEXT.items()], colour="#444444", width=1.8, size=0.9)
        robot(fig, s)
        t = "one wavefront from the door, 76 cells: an arrow in every cell"
    sg(fig, dy=-0.15, size=16)
    axes(fig)
    return layout(fig, t, width=900, height=620)


figs = [frame(k) for k in range(7)]
make_gif(figs, here / "opening", fps=4, holds=[12, 6, 10, 8, 10, 12, 30], keys=[0, 2, 4, 6], cols=2, width=760)
