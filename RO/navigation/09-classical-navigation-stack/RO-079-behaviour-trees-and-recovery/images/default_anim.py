"""Nav2's default behaviour tree (our Python version, btkit.py) ticking on the room of RO-058: the robot starts at
(2.0, 1.0), the person steps onto the route at 2.4 s. Top: the room at that tick (blue: the path on the blackboard;
pink: the person; dotted: the robot's track). Bottom: the tree; each box is coloured by what the node returned in
that tick (amber running, green success, red failure; white: not ticked). The recovery half of the tree is never
ticked in this run and is drawn as one row. Run -> default_anim.gif, default_anim_frames.png"""
from pathlib import Path

import btkit as bt
import navdraw as nd
import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
R = bt.results()["person"]
recs = R["records"]
rows = nd.tree_rows(bt.default_tree(), nd.NAV2)
REC = 21                                                 # uid of the recovery subtree's root
rows = [r for r in rows if r[0] < REC] + [(REC, 1, 0, "Sequence: recovery (never ticked in this run, 13 nodes)")]
plans = [t for t, code in R["planned"]]
assert plans == [0.01, 3.02] and R["status"] == bt.SUCCESS and round(R["t"], 2) == 9.77
checks = [r["t"] for r in recs if any(u == 11 for _, _, u in r["log"])]
assert checks[:4] == [1.01, 2.01, 3.01, 4.02]
assert [s for lab, s, u in nd.at(recs, 3.01)["log"] if u == 11] == [bt.FAILURE]


def caption(t):
    rec = nd.at(recs, t)
    lit, _ = nd.lit_of(rec)
    if t == 0.0:
        return "t = 0.00 s: no path yet, so IsGoalNearby? fails and ComputePathToPose is sent"
    if t == 0.01:
        return "t = 0.01 s: the path arrives; FollowPath is sent and runs"
    if lit.get(11) == bt.SUCCESS:
        return f"t = {t:.2f} s: the 1 Hz check: same goal, under 4 m left, path valid: keep it, no new plan"
    if lit.get(11) == bt.FAILURE:
        return f"t = {t:.2f} s: the 1 Hz check: the person is on the path: ValidatePath? fails, a new plan is asked"
    if lit.get(12) == bt.SUCCESS:
        return f"t = {t:.2f} s: the new path arrives; FollowPath follows it"
    if rec["tree_status"] == bt.SUCCESS:
        return f"t = {t:.2f} s: the goal checker accepts: FollowPath and the whole tree succeed"
    if t == 2.4:
        return "t = 2.40 s: the person steps in; between checks only FollowPath is ticked"
    return f"t = {t:.2f} s: between checks: the tree ticks FollowPath only (every 10 ms)"


def frame(t):
    rec = nd.at(recs, t)
    lit, count = nd.lit_of(rec)
    fig = make_subplots(rows=2, cols=1, row_heights=[0.33, 0.67], vertical_spacing=0.035)
    nd.room(fig, 1, 1, person=rec["person"])
    nd.goal(fig, bt.GOAL, 1, 1)
    nd.track(fig, recs, t, row=1, col=1)
    nd.path(fig, rec["path"], row=1, col=1)
    nd.robot(fig, *rec["robot"], row=1, col=1)
    n = nd.draw_tree(fig, rows, lit, count, row=2, col=1)
    fig.add_annotation(x=0.0, y=1.0, xref="paper", yref="paper", text=caption(t), showarrow=False, xanchor="left",
                       yanchor="bottom", font=dict(size=19))
    fig.update_xaxes(range=[-0.05, 7.05], visible=False, row=1, col=1)
    fig.update_yaxes(range=[-0.05, 4.3], visible=False, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[-0.1, 9.6], visible=False, row=2, col=1)
    fig.update_yaxes(range=[-n + 0.4, 0.6], visible=False, row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=820, height=1240, showlegend=False,
                      margin=dict(l=8, r=8, t=40, b=8))
    return fig


T = [0.0, 0.01, 0.5, 1.01, 1.5, 2.01, 2.4, 2.7, 3.01, 3.02, 3.5, 4.02, 5.0, 6.0, 7.0, 8.0, 9.0, 9.77]
holds = [6, 6, 2, 6, 2, 4, 5, 2, 7, 6, 2, 4, 2, 2, 2, 2, 2, 14]
figs = [frame(t) for t in T]
make_gif(figs, here / "default_anim", fps=3, holds=holds, keys=[1, 3, 8, len(T) - 1], cols=2, width=760)
print("plans at", plans, "; 1 Hz checks at", checks[:6], "; accepted at", R["t"])
