"""Weighted and anytime A* on the long trip (S in the bottom-left corner cell, G at the right wall), as ARA* runs it:
weighted A* with f = g + eps h, eps = 2.5, then 1.2, then 1.0, each run reusing the g values of the run before.
One expansion per frame; red: taken off the open list in this run, grey: in earlier runs; blue: the best route so
far. Run 1 (eps 2.5): 22 cells, route 9.243 m. Run 2 (eps 1.2): 31 more cells, 8.414 m. Run 3 (eps 1.0): 16 more
cells, 8.000 m, the shortest. 69 cells in all; three fresh weighted A* runs would take 22 + 38 + 43 = 103.
Run -> weighted_anim.gif, weighted_anim_frames.png"""
from pathlib import Path

from drawkit import axes, layout, outline, room, route, sg, title_at
from gifkit import make_gif
from plotly.subplots import make_subplots
from searchkit import ara_star, astar

here = Path(__file__).parent
LS, LG = (0, 0), (13, 3)
EPS = (2.5, 1.2, 1.0)
RUNS = ara_star(EPS, start=LS, goal=LG)
FRESH = [astar(start=LS, goal=LG, eps=e) for e in EPS]
assert [len(r["order"]) for r in RUNS] == [22, 31, 16] and [round(r["cost"], 3) for r in RUNS] == [9.243, 8.414, 8.0]
assert [len(r["order"]) for r in FRESH] == [22, 38, 43] and [round(r["cost"], 3) for r in FRESH] == [9.243, 8.414, 8.0]
assert round(9.243 / 8.0, 3) == 1.155 and round(8.414 / 8.0, 3) == 1.052


def frame(run, k, title=None, sub=None):
    fig = make_subplots(rows=1, cols=1)
    st = {c: "pale" for r in RUNS[:run] for c in r["order"]}
    st.update({c: "closed" for c in RUNS[run]["order"][:k]})
    room(fig, (1, 1), st, labels=False)
    if 0 < k <= len(RUNS[run]["order"]):
        outline(fig, RUNS[run]["order"][k - 1], rc=(1, 1))
    done = k == len(RUNS[run]["order"])
    best = RUNS[run] if done else (RUNS[run - 1] if run else None)
    if best:
        route(fig, best["path"], rc=(1, 1))
    sg(fig, (1, 1), goal=LG, start=LS)
    axes(fig, (1, 1))
    e = EPS[run]
    title = title or f"run {run + 1}, ε = {e}: cell {k} of this run"
    sub = sub or ("best route so far: " + (f"{best['cost']:.3f} m" if best else "none yet") +
                  f"; this run sorts by f = g + {e} h")
    title_at(fig, sub, 1.0, size=19)
    return layout(fig, title, width=900, height=600, margin=dict(l=30, r=30, t=110, b=30))


figs, holds, keys = [], [], []
for run, e in enumerate(EPS):
    n = len(RUNS[run]["order"])
    for k in range(1, n + 1):
        figs.append(frame(run, k))
        holds.append(1)
    r = RUNS[run]
    figs.append(frame(run, n, f"run {run + 1} done, ε = {e}: route {r['cost']:.3f} m",
                      f"{n} cells in this run; the route is at most {e} times the shortest"))
    holds.append(10 if run < 2 else 4)
    keys.append(len(figs) - 1)
figs.append(frame(2, len(RUNS[2]["order"]), "anytime: 9.243 m at once, then 8.414 m, then 8.000 m",
                  "69 cells in all; three fresh runs would take 22 + 38 + 43 = 103"))
holds.append(24)
keys.append(len(figs) - 1)
make_gif(figs, here / "weighted_anim", fps=5, holds=holds, keys=keys, cols=2, width=760)
