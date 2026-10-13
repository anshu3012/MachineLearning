"""Animation: the task planner's two-action plan checked against the table. Action 1, pick up the cup: the arm's
motion from home to the cup's lid is found (a transit of 154.6 degrees, PRM of RO-052, seed 0). Action 2, put the cup
down at B: the cup at B would overlap the bottle standing there by 4 cm, so no placement exists and the plan fails.
Run -> fail_plan.gif, fail_plan_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import tabledraw as td
import tampkit as t
from gifkit import GREEN, GREY, RED, make_gif

here = Path(__file__).parent
w0 = t.World({"cup": t.A_X, "bottle": t.B_X})
start, goal = {"cup": "A", "bottle": "start"}, {"cup": "B"}
plan = next(t.task_plans(start, goal, set()))
assert plan == [("pick", "cup", "A"), ("place", "cup", "B")]
log = []
steps, fail = t.solve_values(w0, start, plan, np.random.default_rng(0), log=log)
assert steps is None and fail == ("cfree", "cup", "B", "bottle", "start")
pick = log[0]
assert pick["test"] == "motion" and round(pick["length"], 1) == 154.6
g = t.grasp_conf(w0, "cup", t.A_X)
path, L = t.motion(w0, t.HOME, g)
assert round(L, 1) == 154.6
D = t.densify(path, 1.0)
cup_b, bot_b = (t.B_X - 0.03, t.B_X + 0.03), (t.B_X - 0.02, t.B_X + 0.02)
overlap = min(cup_b[1], bot_b[1]) - max(cup_b[0], bot_b[0])
assert abs(overlap - 0.04) < 1e-9

LINES = ["the task planner's plan", "1. pick up the cup at A", "2. put the cup down at B"]


def frame(k, held, status, title, ghost=False):
    fig = go.Figure()
    w = t.World({"bottle": t.B_X} if held else {"cup": t.A_X, "bottle": t.B_X}, held="cup" if held else None)
    td.scene(fig, w)
    td.hand_trace(fig, D[:k + 1])
    td.arm(fig, D[k], held="cup" if held else None)
    if ghost:
        td.standing_bad(fig, "cup", t.B_X)
        fig.add_annotation(x=t.B_X, y=0.08, text="overlap 4 cm", showarrow=False, font=dict(size=18, color=RED))
    td.axes(fig)
    fig.update_xaxes(domain=[0, 0.6])
    fig.update_yaxes(scaleanchor="x")
    ys = [0.86, 0.66, 0.40]
    for y, s, (txt, c) in zip(ys, LINES, [("", "black")] + status):
        fig.add_annotation(x=0.64, y=y, xref="paper", yref="paper", text=s, showarrow=False, xanchor="left",
                           font=dict(size=22, color="black"))
        if txt:
            fig.add_annotation(x=0.67, y=y - 0.09, xref="paper", yref="paper", text=txt, showarrow=False,
                               xanchor="left", font=dict(size=20, color=c))
    td.layout(fig, 1350, 620, title, margin=dict(l=80, r=20, t=90, b=70))
    return fig


figs, holds = [], []
pending = [("not yet tested", GREY), ("not yet tested", GREY)]
figs.append(frame(0, False, pending, "the plan from the facts alone: 2 actions"))
holds.append(8)
idx = np.linspace(0, len(D) - 1, 11).round().astype(int)
for n, k in enumerate(idx[1:]):
    figs.append(frame(k, False, [("testing: a motion to the lid?", GREY), ("not yet tested", GREY)],
                      "action 1: search for the arm's motion to the cup's lid"))
    holds.append(1)
ok1 = (f"motion found: {L:.1f} degrees", GREEN)
figs.append(frame(len(D) - 1, True, [ok1, ("testing: is spot B free?", GREY)], "the cup is held"))
holds.append(6)
figs.append(frame(len(D) - 1, True, [ok1, ("no free placement: fails", RED)],
                  "action 2: the cup at B would overlap the bottle", ghost=True))
holds.append(20)
make_gif(figs, here / "fail_plan", fps=4, holds=holds, keys=[0, 6, len(figs) - 2, len(figs) - 1], cols=2, width=1000)
