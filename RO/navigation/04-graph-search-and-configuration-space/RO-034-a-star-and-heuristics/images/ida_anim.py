"""IDA* on the room grid from S to G, on the part of the room it touches (x 1.0-4.5 m, y 0-4 m). Each round is a
depth-first search that drops a branch as soon as f = g + h passes the round's limit. The only thing kept in memory
is the route from S to the cell being visited (blue). Cells visited in this round are light orange, the cell being
visited is outlined in orange. Round 1, limit 3.121 m (h at S): 9 visits, no route; the smallest f that passed the
limit was 3.414 m, the next limit. Round 2, limit 3.414 m: G is reached at the 8th visit, route 3.414 m. 17 visits in
all, never more than 7 cells in memory. Run -> ida_anim.gif, ida_anim_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import axes, layout, outline, room, route, sg, title_at
from gifkit import make_gif
from searchkit import GOAL, START, ida_star, octile, path_cost

here = Path(__file__).parent
XR, YR = (2, 9), (0, 8)
R = ida_star()
assert [round(r["limit"], 3) for r in R] == [3.121, 3.414] and [len(r["visits"]) for r in R] == [9, 8]
assert round(R[0]["next"], 3) == 3.414 and R[1]["found"] and round(R[1]["found"][1], 3) == 3.414
assert max(len(p) for r in R for p in r["paths"]) == 7


def frame(rn, k, title=None, sub=None, final=False):
    r = R[rn]
    fig = go.Figure()
    seen = {c: "seen" for c in r["visits"][:k]}
    room(fig, None, seen, xr=XR, yr=YR, labels=False)
    if k:
        p = r["paths"][k - 1]
        if len(p) > 1:
            route(fig, p)
        outline(fig, p[-1])
        g = path_cost(p)
        f = g + octile(p[-1])
        title = title or f"round {rn + 1}, limit {r['limit']:.3f} m: visit {k} of {len(r['visits'])}"
        sub = sub or f"in memory: the route from S, {len(p)} cells; here f = {g:.3f} + {octile(p[-1]):.3f} = {f:.3f}"
    sg(fig, None, XR, YR)
    axes(fig, None, XR, YR)
    title_at(fig, sub, 1.0, size=19)
    return layout(fig, title, width=900, height=1080, margin=dict(l=30, r=30, t=115, b=30))


figs, holds = [], []
figs.append(frame(0, 0, "IDA*: depth-first search with a limit on f = g + h",
                  f"round 1: the limit is h at S, {octile(START):.3f} m")); holds.append(5)
for k in range(1, len(R[0]["visits"]) + 1):
    figs.append(frame(0, k)); holds.append(3)
figs.append(frame(0, len(R[0]["visits"]), "round 1 ends: no route with f up to 3.121 m",
                  "the smallest f that passed the limit was 3.414 m: the next limit")); holds.append(6)
for k in range(1, len(R[1]["visits"]) + 1):
    figs.append(frame(1, k)); holds.append(3)
figs.append(frame(1, len(R[1]["visits"]), "round 2 reaches G: route 3.414 m",
                  "17 visits in all; never more than 7 cells in memory")); holds.append(16)
assert path_cost(R[1]["found"][0]) == R[1]["found"][1] and R[1]["found"][0][-1] == GOAL
make_gif(figs, here / "ida_anim", fps=2, holds=holds, keys=[4, 10, 15, 19], cols=2, width=720)
