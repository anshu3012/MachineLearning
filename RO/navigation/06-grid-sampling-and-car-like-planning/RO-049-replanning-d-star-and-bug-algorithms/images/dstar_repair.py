"""D* Lite repairing the door's numbers after the robot sees the box, on the room grid, one cell per frame. Every free
cell shows its number g, its cost-to-go to the door as the robot knew it (RO-048); the robot stands at (5, 3), the
box's two cells are brown. Orange outline: a cell whose number disagrees with its lookahead, the smallest move plus
neighbour's number, waiting in the queue. Each frame takes the queued cell with the smallest key off
the queue: if its number must rise, it is first set to infinity (red) and its neighbours are rechecked; if it can
fall to its lookahead, it takes that value (green). After 12 steps the robot's cell holds 4.414, equal to its lookahead;
8 cells are still queued and 68 numbers were never touched. Run -> dstar_repair.gif, dstar_repair_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, centre, layout, numbers, outline, robot, room, route, sg
from gifkit import BLUE, GREEN, ORANGE, RED, make_gif
from replan import INF, GOAL, DStarLite, Grid, dijkstra_from_goal

here = Path(__file__).parent
GR = Grid(1)
V0 = dijkstra_from_goal(GR)
POS = (5, 3)
BOX = sorted(GR.box_cells())
D = DStarLite(GR, POS, GOAL, g=V0)
GR.seen.update(BOX)
D.blocked(BOX)
first_queue = set(D.inU)
n = D.compute(trace=True)
LOG, SN = D.log, D.snaps
assert n == 12 and len(SN) == 13 and BOX == [(4, 4), (5, 4)]
assert first_queue == {(5, 4), (5, 3), (4, 4), (4, 3), (3, 4)}
assert [(c, k) for c, k, *_ in LOG] == [((5, 4), "raise"), ((5, 3), "raise"), ((4, 4), "raise"), ((4, 3), "raise"),
                                        ((5, 2), "raise"), ((3, 4), "raise"), ((3, 4), "lower"), ((3, 3), "raise"),
                                        ((4, 2), "raise"), ((3, 3), "lower"), ((4, 3), "lower"), ((5, 3), "lower")]
assert round(D.G(POS), 3) == 4.414 and len(SN[-1][2]) == 8
touched = {c for c, *_ in LOG}
assert len(touched) == 8 and len(V0) - len(touched) == 68
PATH = [POS]
while PATH[-1] != GOAL:
    PATH.append(min([ns for ns in GR.nbrs(PATH[-1]) if ns[1] < INF],
                    key=lambda ns: (round(ns[1] + D.G(ns[0]), 9), D.G(ns[0]), ns[0]))[0])
assert round(sum(0.5 * ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 for a, b in zip(PATH, PATH[1:])), 3) == 4.414
NAME = {(5, 4): "the box's right cell", (4, 4): "the box's left cell", (5, 3): "the robot's cell",
        (4, 3): "the cell left of the robot", (5, 2): "the cell below the robot", (3, 4): "the cell left of the box",
        (3, 3): "the cell below-left of the box", (4, 2): "S"}


def fmt(v):
    return "∞" if v == INF else f"{v:.2f}"


def frame(k):
    g, rhs, queued = SN[k]
    fig = go.Figure()
    room(fig, None, {c: "box" for c in BOX}, labels=False)
    last = k == len(SN) - 1
    if last:
        route(fig, PATH, BLUE, width=5)
    vals = {c: fmt(g.get(c, INF)) for c in V0 if c not in BOX}
    bx = "white" if last else None
    numbers(fig, {c: v for c, v in vals.items() if c not in touched or k == 0}, size=15, dy=0.08, color="#777777",
            box=bx)
    numbers(fig, {c: v for c, v in vals.items() if c in touched and k > 0}, size=17, dy=0.08, box=bx)
    numbers(fig, {c: fmt(g.get(c, INF)) for c in BOX}, size=17, dy=0.08, color="white")
    for c in queued:
        outline(fig, c, colour=ORANGE, width=4)
    if k > 0:
        c, kind, old, new, _ = LOG[k - 1]
        outline(fig, c, colour=RED if kind == "raise" else GREEN, width=7)
    robot(fig, (centre(POS)[0], centre(POS)[1] - 0.15), size=14)
    sg(fig, dy=-0.15, size=16)
    axes(fig)
    if k == 0:
        t = "box seen: 5 cells disagree with their lookahead (orange)"
    elif k == len(SN) - 1:
        t = f"12. {NAME[c]} falls to {fmt(new)}, its lookahead: stop; 8 still queued"
    else:
        verb = f"rises: {fmt(old)} to ∞" if kind == "raise" else f"falls: ∞ to {fmt(new)}"
        t = f"{k}. {NAME[c]} {verb}"
    return layout(fig, t, width=900, height=620)


figs = [frame(k) for k in range(len(SN))]
holds = [14] + [7] * (len(SN) - 2) + [30]
make_gif(figs, here / "dstar_repair", fps=4, holds=holds, keys=[0, 4, 7, len(SN) - 1], cols=2, width=760)
