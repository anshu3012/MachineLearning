"""Animation: the task and motion planner of this Note on the table, one test per frame (seed 0, as the notebook).
Skeleton 1 (pick up the cup, put it down at B) fails its free-placement test at B; the failure becomes a fact; skeleton
2 moves the bottle first. Its placement x is sampled: 0.395 m passes until the cup at B overlaps it (backtrack),
0.208 m overlaps the cup at A, 0.091 m and 0.078 m are nearer to the shoulder than the folded arm reaches (0.1 m),
0.485 m works; the cup then reaches B.
Run -> tamp_search.gif, tamp_search_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import tabledraw as td
import tampkit as t
from gifkit import GREEN, GREY, RED, make_gif

here = Path(__file__).parent
w0 = t.World({"cup": t.A_X, "bottle": t.B_X})
steps, history, log = t.tamp(w0, {"cup": "A", "bottle": "start"}, {"cup": "B"}, seed=0)
xs = [e["x"] for e in log if e.get("sampled") and e["test"] != "backtrack"]
assert [round(x, 3) for x in xs] == [0.395, 0.208, 0.091, 0.078, 0.485]
assert [round(e["length"], 1) for e in log if e["test"] == "motion"] == [154.6, 88.7, 11.1, 87.0, 42.1, 139.1, 104.6]
X1, X2, X3, X4, X5 = xs

SK1 = ["1. pick up the cup at A", "2. put the cup down at B"]
SK2 = ["1. pick up the bottle", "2. put the bottle down at x", "3. pick up the cup at A", "4. put the cup down at B"]


def conf_path(world, q, o, x):
    """The configuration with the hand on o's top at x (o standing there in the world after), and the motion."""
    after = world.copy()
    if world.held == o:
        after.held, after.at[o] = None, x
    g = t.grasp_conf(after, o, x)
    path, L = t.motion(world, q, g)
    return g, path, L


def frame(title, world, q, held, status, samples=(), path=None, ghost=None, reach=False, heading="skeleton 1"):
    fig = go.Figure()
    td.scene(fig, world)
    if path is not None:
        td.hand_trace(fig, path)
    if ghost:
        td.standing_bad(fig, *ghost[:2])
        fig.add_annotation(x=ghost[1], y=ghost[3] if len(ghost) > 3 else 0.1, text=ghost[2], showarrow=False,
                           font=dict(size=17, color=RED))
    if reach:
        a = np.linspace(-0.6, 1.6, 60)
        fig.add_trace(go.Scatter(x=0.1 * np.cos(a), y=0.1 * np.sin(a), mode="lines",
                                 line=dict(color=RED, width=2, dash="dash"), hoverinfo="skip"))
    td.arm(fig, q, held=held)
    td.axes(fig, xr=(-0.2, 0.62), yr=(-0.17, 0.52))
    fig.update_xaxes(domain=[0, 0.56])
    fig.update_yaxes(scaleanchor="x")
    lines = SK1 if heading == "skeleton 1" else SK2
    fig.add_annotation(x=0.6, y=0.97, xref="paper", yref="paper", text=heading, showarrow=False, xanchor="left",
                       font=dict(size=22))
    y = 0.88
    for s, (txt, c) in zip(lines, status):
        fig.add_annotation(x=0.6, y=y, xref="paper", yref="paper", text=s, showarrow=False, xanchor="left",
                           font=dict(size=19))
        fig.add_annotation(x=0.63, y=y - 0.065, xref="paper", yref="paper", text=txt, showarrow=False,
                           xanchor="left", font=dict(size=17, color=c))
        y -= 0.15
    if samples:
        fig.add_annotation(x=0.6, y=y - 0.01, xref="paper", yref="paper", text="samples of x (m):", showarrow=False,
                           xanchor="left", font=dict(size=19))
        for k, (txt, c) in enumerate(samples):
            fig.add_annotation(x=0.63, y=y - 0.075 - 0.06 * k, xref="paper", yref="paper", text=txt,
                               showarrow=False, xanchor="left", font=dict(size=17, color=c))
    td.layout(fig, 1400, 700, title, margin=dict(l=80, r=20, t=80, b=70))
    return fig


P = ("not tested", GREY)
figs, holds = [], []
# ---- skeleton 1 ----
g1, path1, L1 = conf_path(w0, t.HOME, "cup", t.A_X)
figs.append(frame("the task planner's first skeleton", w0, t.HOME, None, [P, P]))
holds.append(8)
held_cup = t.World({"bottle": t.B_X}, held="cup")
figs.append(frame("action 1: a motion to the cup's lid exists", held_cup, g1, "cup",
                  [(f"motion found: {L1:.1f} degrees", GREEN), P], path=path1))
holds.append(6)
figs.append(frame("action 2: the cup at B would overlap the bottle by 4 cm", held_cup, g1, "cup",
                  [(f"motion found: {L1:.1f} degrees", GREEN), ("no free placement: skeleton fails", RED)],
                  ghost=("cup", t.B_X, "overlap 4 cm")))
holds.append(10)
# ---- skeleton 2 ----
figs.append(frame("new fact: the cup at B collides with the bottle where it stands", w0, t.HOME, None, [P] * 4,
                  heading="skeleton 2: move the bottle first"))
holds.append(10)
H2 = "skeleton 2: move the bottle first"
gb, pathb, Lb = conf_path(w0, t.HOME, "bottle", t.B_X)
held_b = t.World({"cup": t.A_X}, held="bottle")
ok1 = (f"motion found: {Lb:.1f} degrees", GREEN)
figs.append(frame("action 1: a motion to the bottle's cap exists", held_b, gb, "bottle", [ok1, P, P, P],
                  path=pathb, heading=H2))
holds.append(6)
# sample 1: passes its own tests, fails at action 4
g2, path2, L2 = conf_path(held_b, gb, "bottle", X1)
w_b1 = t.World({"cup": t.A_X, "bottle": X1})
s1 = [(f"{X1:.3f}: testing", GREY)]
figs.append(frame(f"action 2: sample x = {X1:.3f} m; free, reachable, motion {L2:.1f} degrees", w_b1, g2, None,
                  [ok1, (f"x = {X1:.3f}: motion {L2:.1f} degrees", GREEN), P, P], s1, path=path2, heading=H2))
holds.append(6)
g3, path3, L3 = conf_path(w_b1, g2, "cup", t.A_X)
held_c1 = t.World({"bottle": X1}, held="cup")
figs.append(frame(f"action 3: a motion to the cup's lid exists ({L3:.1f} degrees)", held_c1, g3, "cup",
                  [ok1, (f"x = {X1:.3f}: motion {L2:.1f} degrees", GREEN), (f"motion {L3:.1f} degrees", GREEN), P],
                  s1, path=path3, heading=H2))
holds.append(6)
ov1 = min(t.B_X + 0.03, X1 + 0.02) - max(t.B_X - 0.03, X1 - 0.02)
assert round(ov1, 4) == 0.0249
figs.append(frame("action 4: the cup at B would overlap the bottle by 2.5 cm", held_c1, g3, "cup",
                  [ok1, (f"x = {X1:.3f}: motion {L2:.1f} degrees", GREEN), (f"motion {L3:.1f} degrees", GREEN),
                   ("no free placement", RED)], s1, ghost=("cup", t.B_X, "overlap 2.5 cm"), heading=H2))
holds.append(8)
s1 = [(f"{X1:.3f}: blocks B later, back up", RED)]
figs.append(frame("backtrack: drop the last two motions and sample x again", held_b, gb, "bottle",
                  [ok1, ("sample again", GREY), P, P], s1, heading=H2))
holds.append(8)
# sample 2: overlaps the cup at A
ov2 = min(t.A_X + 0.03, X2 + 0.02) - max(t.A_X - 0.03, X2 - 0.02)
assert round(ov2, 4) == 0.0224
s2 = s1 + [(f"{X2:.3f}: overlaps the cup at A", RED)]
figs.append(frame(f"sample x = {X2:.3f} m: the bottle would overlap the cup by 2.2 cm", held_b, gb, "bottle",
                  [ok1, ("sample again", GREY), P, P], s2, ghost=("bottle", X2, "overlap 2.2 cm"), heading=H2))
holds.append(7)
# samples 3, 4: out of reach
d3, d4 = math.hypot(*t.top("bottle", X3)), math.hypot(*t.top("bottle", X4))
assert (round(d3, 4), round(d4, 4)) == (0.0993, 0.088)
s3 = s2 + [(f"{X3:.3f}: cap {d3:.3f} m from the shoulder", RED)]
figs.append(frame(f"sample x = {X3:.3f} m: the cap is {d3:.3f} m from the shoulder, the arm reaches no nearer than 0.1 m",
                  held_b, gb, "bottle", [ok1, ("sample again", GREY), P, P], s3,
                  ghost=("bottle", X3, "too near", 0.2), reach=True, heading=H2))
holds.append(7)
s4 = s3 + [(f"{X4:.3f}: cap {d4:.3f} m from the shoulder", RED)]
figs.append(frame(f"sample x = {X4:.3f} m: the cap is {d4:.3f} m from the shoulder, again too near", held_b, gb,
                  "bottle", [ok1, ("sample again", GREY), P, P], s4, ghost=("bottle", X4, "too near", 0.2), reach=True,
                  heading=H2))
holds.append(7)
# sample 5: the plan completes
g5, path5, L5 = conf_path(held_b, gb, "bottle", X5)
w_b5 = t.World({"cup": t.A_X, "bottle": X5})
s5 = s4 + [(f"{X5:.3f}: works", GREEN)]
ok2 = (f"x = {X5:.3f}: motion {L5:.1f} degrees", GREEN)
figs.append(frame(f"sample x = {X5:.3f} m: free, reachable, motion {L5:.1f} degrees", w_b5, g5, None,
                  [ok1, ok2, P, P], s5, path=path5, heading=H2))
holds.append(6)
g6, path6, L6 = conf_path(w_b5, g5, "cup", t.A_X)
held_c5 = t.World({"bottle": X5}, held="cup")
ok3 = (f"motion found: {L6:.1f} degrees", GREEN)
figs.append(frame("action 3: a motion to the cup's lid exists", held_c5, g6, "cup", [ok1, ok2, ok3, P], s5,
                  path=path6, heading=H2))
holds.append(6)
g7, path7, L7 = conf_path(held_c5, g6, "cup", t.B_X)
w_end = t.World({"cup": t.B_X, "bottle": X5})
figs.append(frame("action 4: spot B is free; the plan is found: 4 actions", w_end, g7, None,
                  [ok1, ok2, ok3, (f"motion found: {L7:.1f} degrees", GREEN)], s5, path=path7, heading=H2))
holds.append(22)
assert [round(v, 1) for v in (L1, Lb, L2, L3, L5, L6, L7)] == [154.6, 88.7, 11.1, 87.0, 42.1, 139.1, 104.6]
make_gif(figs, here / "tamp_search", fps=3, holds=holds, keys=[2, 7, 10, len(figs) - 1], cols=2, width=1000)
