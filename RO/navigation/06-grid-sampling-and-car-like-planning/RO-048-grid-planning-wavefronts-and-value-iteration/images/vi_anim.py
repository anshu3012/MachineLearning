"""Value iteration on the room grid, one frame per sweep. Every value starts unknown (infinite) except the door's cell
G, 0. A sweep visits the free cells row by row from the door's wall down, left to right, and gives each cell the
smallest move + value among its neighbours, using values already updated in the same sweep. Blue outline: the cell
got its first value in this sweep; orange outline: its value was lowered, because a shorter way round has just
reached a neighbour. Sweep 1 already gives 49 cells a value, S its final 3.414; sweeps 3 to 7 lower 14 values in all;
sweep 8 changes nothing, and the values equal Dijkstra's from the door. Run -> vi_anim.gif, vi_anim_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from drawkit import VSCALE, axes, heat, layout, numbers, outline, sg
from gifkit import BLUE, ORANGE, make_gif
from gridplan import CELLS, GOAL, INF, START, cost_to_go, value_iteration

here = Path(__file__).parent
SN = value_iteration()
D = cost_to_go()
VMAX = max(D.values())
assert len(SN) == 9                                         # the start and 8 sweeps
assert [(len(s["new"]), len(s["lowered"])) for s in SN[1:]] == [(49, 0), (11, 0), (3, 4), (6, 2), (3, 3), (2, 2),
                                                                  (1, 3), (0, 0)]
assert sum(len(s["lowered"]) for s in SN) == 14 and round(SN[1]["V"][START], 3) == 3.414
assert all(abs(SN[-1]["V"][c] - D[c]) < 1e-9 for c in CELLS)
assert [round(v, 3) for v in SN[3]["lowered"][(4, 7)]] == [1.914, 1.5]


def frame(k):
    s = SN[k]
    vals = {c: v for c, v in s["V"].items() if v < INF}
    fig = go.Figure()
    heat(fig, vals, VSCALE, VMAX)
    numbers(fig, vals, fmt="{:.2f}", size=15, dy=0.08)
    for c in s["new"]:
        outline(fig, c, colour=BLUE, width=4)
    for c in s["lowered"]:
        outline(fig, c, colour=ORANGE, width=5)
    sg(fig, dy=-0.15, size=16)
    axes(fig)
    nn, nl = len(s["new"]), len(s["lowered"])
    if k == 0:
        t = "before the first sweep: only the door's cell G has a value, 0"
    elif k == 1:
        t = f"sweep 1: {nn} cells get a value (blue), S already its 3.41"
    elif nn == nl == 0:
        t = f"sweep {k}: nothing changes, so every value is final"
    elif k == 3:
        t = f"sweep 3: {nn} new, {nl} lowered (orange), such as 1.91 to 1.50"
    else:
        t = f"sweep {k}: {nn} new (blue), {nl} lowered (orange)"
    return layout(fig, t, width=900, height=620)


figs = [frame(k) for k in range(len(SN))]
holds = [10, 14, 10, 14, 8, 8, 8, 8, 30]
make_gif(figs, here / "vi_anim", fps=4, holds=holds, keys=[1, 2, 3, 8], cols=2, width=760)
