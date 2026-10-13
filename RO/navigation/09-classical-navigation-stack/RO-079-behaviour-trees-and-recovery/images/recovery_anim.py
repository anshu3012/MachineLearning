"""The blocked door, ticked by Nav2's default tree (our Python version, btkit.py). At 2.4 s a person (pink) stops
in the gap between the table's corner and the wall, left of the door; a trolley (brown) stands in the only other
way, between the table and the cabinet; at 8.0 s the person walks away. Top: the room (blue: the path on the
blackboard; dotted: the robot's track). Bottom: the whole tree, each box coloured by what the node returned in that
tick (amber running, green success, red failure, white not ticked); a node ticked more than once in the tick lists
each answer. Run -> recovery_anim.gif, recovery_anim_frames.png"""
from pathlib import Path

import btkit as bt
import navdraw as nd
from gifkit import FONT, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
R = bt.results()["blocked"]
recs = R["records"]
rows = nd.tree_rows(bt.default_tree(), nd.NAV2)
codes = [(t, c) for t, c in R["planned"]]
assert codes[0] == (0.01, None) and codes[1] == (3.02, "NO_VALID_PATH") and codes[-1] == (9.79, None)
assert [t for t, c in codes if c] == [3.02, 3.03, 3.04, 3.05, 4.77, 4.78]
assert R["cleared"] == [(3.02, "global"), (3.03, "local"), (3.03, "global"), (3.04, "global"), (4.77, "global")]
assert R["status"] == bt.SUCCESS and round(R["t"], 2) == 15.6


def ran(uid, s):
    return [r["t"] for r in recs if (uid, s) in [(u, x) for _, x, u in r["log"]]]


assert ran(31, bt.RUNNING)[0] == 3.05 and ran(31, bt.SUCCESS) == [4.76]          # Spin
assert ran(32, bt.RUNNING)[0] == 4.78 and ran(32, bt.SUCCESS) == [9.78]          # Wait

CAP = {0.01: "t = 0.01 s: the path arrives; FollowPath runs",
       2.4: "t = 2.40 s: the person stops in the gap left of the door; the trolley blocks the other way",
       3.01: "t = 3.01 s: the 1 Hz check: the path is blocked; ComputePathToPose is sent",
       3.02: "t = 3.02 s: no path (NO_VALID_PATH): clear the global costmap, ask again",
       3.03: "t = 3.03 s: no path again: navigation fails; recovery 1: clear both costmaps; navigate again",
       3.04: "t = 3.04 s: no path: clear the global costmap, ask again",
       3.05: "t = 3.05 s: navigation fails again; recovery 2: Spin 1.57 rad",
       4.0: "t = 4.00 s: spinning in place",
       4.76: "t = 4.76 s: the spin is done; navigate again",
       4.78: "t = 4.78 s: still no path; recovery 3: Wait 5 s",
       6.5: "t = 6.50 s: waiting",
       8.0: "t = 8.00 s: the person walks away",
       9.78: "t = 9.78 s: the wait is over; navigate again",
       9.79: "t = 9.79 s: a path exists again; FollowPath runs",
       12.0: "t = 12.00 s: driving to the door",
       15.6: "t = 15.60 s: the goal checker accepts: the tree succeeds after 3 recoveries"}


def frame(t):
    rec = nd.at(recs, t)
    lit, seq = nd.lit_of(rec)
    fig = make_subplots(rows=2, cols=1, row_heights=[0.29, 0.71], vertical_spacing=0.03)
    nd.room(fig, 1, 1, trolley=True, person=rec["person"])
    nd.goal(fig, bt.GOAL, 1, 1)
    nd.track(fig, recs, t, row=1, col=1)
    nd.path(fig, rec["path"], row=1, col=1)
    nd.robot(fig, *rec["robot"], row=1, col=1)
    n = nd.draw_tree(fig, rows, lit, seq, row=2, col=1)
    fig.add_annotation(x=0.0, y=1.0, xref="paper", yref="paper", text=CAP[t], showarrow=False, xanchor="left",
                       yanchor="bottom", font=dict(size=19))
    fig.update_xaxes(range=[-0.05, 7.05], visible=False, row=1, col=1)
    fig.update_yaxes(range=[-0.05, 4.3], visible=False, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[-0.1, 9.6], visible=False, row=2, col=1)
    fig.update_yaxes(range=[-n + 0.4, 0.6], visible=False, row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=820, height=1480, showlegend=False,
                      margin=dict(l=8, r=8, t=40, b=8))
    return fig


T = list(CAP)
holds = [4, 5, 7, 7, 7, 6, 6, 2, 5, 6, 2, 5, 5, 6, 2, 14]
figs = [frame(t) for t in T]
make_gif(figs, here / "recovery_anim", fps=3, holds=holds, keys=[3, 6, 11, 15], cols=2, width=760)
print("planner answers", codes, "; costmaps cleared", R["cleared"], "; accepted at", R["t"])
