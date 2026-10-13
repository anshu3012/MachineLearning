"""Animation: the plan the task and motion planner returned, run skill by skill (seed 0, as the notebook). 1. pick up
the bottle at B, 88.7 degrees of joint motion; 2. put it down at x = 0.485 m, 42.1 degrees; 3. pick up the cup at A,
139.1 degrees; 4. put it down at B, 104.6 degrees. The dotted line is the hand's track in the current skill.
Run -> final_plan.gif, final_plan_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import tabledraw as td
import tampkit as t
from gifkit import make_gif

here = Path(__file__).parent
w0 = t.World({"cup": t.A_X, "bottle": t.B_X})
steps, _, _ = t.tamp(w0, {"cup": "A", "bottle": "start"}, {"cup": "B"}, seed=0)
LEN = [round(s["length"], 1) for s in steps]
assert LEN == [88.7, 42.1, 139.1, 104.6] and round(sum(s["length"] for s in steps), 1) == 374.5
NAMES = ["1. pick up the bottle", f"2. put the bottle down at x = {steps[1]['x']:.3f} m", "3. pick up the cup at A",
         "4. put the cup down at B"]


def frame(i, q, title):
    s = steps[i]
    fig = go.Figure()
    td.scene(fig, s["world"])
    D = t.densify(s["path"], 1.0)
    k = int(np.argmin([t.dist(p, q) for p in D]))
    td.hand_trace(fig, D[:k + 1])
    td.arm(fig, q, held=s["world"].held)
    td.axes(fig, xr=(-0.2, 0.62), yr=(-0.17, 0.52))
    fig.update_yaxes(scaleanchor="x")
    td.layout(fig, 1000, 640, title)
    return fig


figs, holds = [], []
for i, s in enumerate(steps):
    D = t.densify(s["path"], 1.0)
    idx = np.linspace(0, len(D) - 1, 9).round().astype(int)
    for n, k in enumerate(idx):
        figs.append(frame(i, D[k], f"{NAMES[i]}: {LEN[i]} degrees of joint motion"))
        holds.append(4 if n == 0 else 1)
    holds[-1] = 5
end = t.World({"cup": t.B_X, "bottle": steps[1]["x"]})
fig = go.Figure()
td.scene(fig, end)
td.arm(fig, steps[-1]["q"])
td.axes(fig, xr=(-0.2, 0.62), yr=(-0.17, 0.52))
fig.update_yaxes(scaleanchor="x")
td.layout(fig, 1000, 640, "done: the cup stands at B, the bottle at 0.485 m; 374.5 degrees in all")
figs.append(fig)
holds.append(18)
make_gif(figs, here / "final_plan", fps=5, holds=holds, keys=[8, 17, 26, len(figs) - 1], cols=2, width=900)
