"""Greedy best-first search on the long trip, from S in the bottom-left corner cell (x 0-0.5 m, y 0-0.5 m) to G at
the right wall (x 6.5-7.0 m, y 1.5-2.0 m), one expansion per frame: it always takes off the open list the cell with
the smallest guess h (octile distance to G) and never looks at the distance already driven. It heads up and right,
towards G, runs into the table, and slides down its left side. Last frame: its route, 9.536 m after 21 cells, and the
shortest route, 8.000 m along the bottom wall (dashed). Run -> greedy_anim.gif, greedy_anim_frames.png"""
from pathlib import Path

from drawkit import axes, layout, outline, room, route, sg, title_at
from gifkit import GREEN, make_gif
from plotly.subplots import make_subplots
from searchkit import astar, greedy, octile

here = Path(__file__).parent
LS, LG = (0, 0), (13, 3)
GR, BEST = greedy(start=LS, goal=LG, trace=True), astar(start=LS, goal=LG)
assert len(GR["order"]) == 21 and round(GR["cost"], 3) == 9.536 and round(BEST["cost"], 3) == 8.0


def frame(k, last=False):
    fig = make_subplots(rows=1, cols=1)
    s = GR["snaps"][k - 1] if k else None
    status = {}
    if s:
        status.update({c: "open" for c in s["open"]})
        status.update({c: "closed" for c in s["closed"]})
    room(fig, (1, 1), status, labels=False)
    if s:
        outline(fig, s["cur"], rc=(1, 1))
    if last:
        route(fig, GR["path"], rc=(1, 1))
        route(fig, BEST["path"], colour=GREEN, width=4, dash="dash", rc=(1, 1))
    sg(fig, (1, 1), goal=LG, start=LS)
    axes(fig, (1, 1))
    if k == 0:
        t = "the long trip: S in the bottom-left corner, G at the right wall"
        sub = f"greedy best-first takes off the open cell with the smallest heuristic h; h at S is {octile(LS, LG):.3f} m"
    elif last:
        t = f"greedy: {len(GR['order'])} cells, route {GR['cost']:.3f} m (blue)"
        sub = f"shortest route: {BEST['cost']:.3f} m along the bottom wall (green, dashed)"
    else:
        c = s["cur"]
        t = f"greedy, cell {k}: took off the open cell with the smallest h, {octile(c, LG):.3f} m"
        sub = "it never counts the distance already driven"
    title_at(fig, sub, 1.0, size=19)
    return layout(fig, t, width=900, height=600, margin=dict(l=30, r=30, t=110, b=30))


n = len(GR["snaps"])
figs = [frame(k) for k in range(n + 1)] + [frame(n, last=True)]
holds = [8] + [3] * (n - 1) + [6, 30]
make_gif(figs, here / "greedy_anim", fps=5, holds=holds, keys=[0, 6, 14, n + 1], cols=2, width=760)
