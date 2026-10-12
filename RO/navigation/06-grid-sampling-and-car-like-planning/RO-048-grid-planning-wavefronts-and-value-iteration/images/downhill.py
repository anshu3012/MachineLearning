"""Following the door's numbers downhill from four starts at once, one move per frame. Each free cell is coloured by its
distance to the door (as in the valley figure) and carries an arrow to its next cell: the neighbour with the smallest
move + distance. The four robots start at S, at the cell below the route's first cell (where a slip leaves the
robot), at the bottom-left corner and at the bottom-right corner; each follows the arrows and arrives at G having
driven exactly its starting number: 3.414, 3.207, 5.243 and 7.914 m. Run -> downhill.gif, downhill_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import VSCALE, arrows, axes, centre, heat, layout, robot, route, sg
from gifkit import BLUE, GREEN, ORANGE, PURPLE, make_gif
from gridplan import CELLS, GOAL, START, cost_to_go, downhill, path_cost

here = Path(__file__).parent
V = cost_to_go()
STARTS = [(START, BLUE, "S"), ((5, 2), ORANGE, "slip"), ((0, 0), GREEN, "corner"), ((13, 0), PURPLE, "far corner")]
ROUTES = [downhill(c, V) for c, _, _ in STARTS]
for (c, _, _), p in zip(STARTS, ROUTES):
    assert abs(path_cost(p) - V[c]) < 1e-9          # each walk is exactly as long as its starting number
assert [round(V[c], 3) for c, _, _ in STARTS] == [3.414, 3.207, 5.243, 7.914]
NEXT = {c: downhill(c, V)[1] for c in CELLS if c != GOAL}
assert all(V[n] < V[c] for c, n in NEXT.items())   # every cell but G has a lower neighbour: no other minimum
OFF = [(-0.09, -0.04), (-0.03, -0.01), (0.03, 0.01), (0.09, 0.04)]    # small offsets so that shared moves show
NAMES = ["from S", "from the slip cell", "from the bottom-left corner", "from the bottom-right corner"]
PLAN = [(r, k) for r, p in enumerate(ROUTES) for k in range(len(p))]   # robot r after k moves, one robot at a time


def pts(p, off):
    return [(centre(c)[0] + off[0], centre(c)[1] + off[1]) for c in p]


def frame(step):
    r, k = PLAN[step] if step >= 0 else (-1, 0)
    fig = go.Figure()
    heat(fig, V, VSCALE, max(V.values()))
    arrows(fig, [(centre(c), centre(n)) for c, n in NEXT.items()], colour="#555555", width=1.6, size=0.9)
    for q in range(len(STARTS)):
        if q < r:
            route(fig, ROUTES[q], STARTS[q][1], width=6, points=pts(ROUTES[q], OFF[q]))
        elif q == r and k > 0:
            route(fig, ROUTES[q][:k + 1], STARTS[q][1], width=6, points=pts(ROUTES[q][:k + 1], OFF[q]))
    for q, (c, col, _) in enumerate(STARTS):
        if q > r:
            robot(fig, centre(c), colour=col, size=18)
    if r >= 0:
        robot(fig, pts(ROUTES[r][k:k + 1], OFF[r])[0], colour=STARTS[r][1], size=20)
    sg(fig, dy=-0.15, size=16)
    axes(fig)
    if r < 0:
        t = "an arrow in every cell: towards the neighbour with the smallest move + number"
    elif k == len(ROUTES[r]) - 1:
        t = f"{NAMES[r]}: at the door after {V[ROUTES[r][0]]:.3f} m, the start cell's number"
    else:
        t = f"{NAMES[r]}, move {k}: step where the arrow points"
    return layout(fig, t, width=900, height=620)


steps = list(range(-1, len(PLAN)))
figs = [frame(st) for st in steps]
ends = {i for i, st in enumerate(steps) if st >= 0 and PLAN[st][1] == len(ROUTES[PLAN[st][0]]) - 1}
holds = [14] + [8 if i in ends else 2 for i in range(1, len(steps) - 1)] + [30]
keys = [0] + sorted(ends)[:2] + [len(steps) - 1]
make_gif(figs, here / "downhill", fps=4, holds=holds, keys=keys, cols=2, width=760)
