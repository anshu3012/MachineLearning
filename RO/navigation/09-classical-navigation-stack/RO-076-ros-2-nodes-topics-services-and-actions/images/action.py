"""Animation: one action, navigate to the door pose. The mission node (action client) sends the goal, the door pose
(3.6, 3.5) facing 90 degrees; the navigator (action server) accepts it and drives the room drive of RO-058. While it
runs, the navigator sends feedback: the time so far, the distance left along the plan (3.698 m at the start), and the
estimated time left, distance over speed; Nav2 sends one every 0.01 s, the animation shows one a second, plus the
moment the person steps in (2.4 s), when the goal does not change. At 8.0 s the result comes back: succeeded.
Right: the room, the plan (grey dashed) and the robot. Run -> action.gif, action_frames.png"""
from pathlib import Path

import bandkit as bk
import netdraw as nd
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import roskit as rk
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
assert round(rk.PLAN_LENGTH, 3) == 3.698 and round(rk.T_ARRIVE, 1) == 8.0
assert round(rk.feedback(1.0)["distance_remaining"], 3) == 3.454
CLIENT, SERVER = (0.13, 0.62), (0.43, 0.62)
GOAL = ((0.23, 0.70), (0.33, 0.70))
FEED = ((0.33, 0.62), (0.23, 0.62))
RES = ((0.33, 0.54), (0.23, 0.54))
xs = np.array([o["x"] for o in rk.L])


def frame(t, kind):
    fig = nd.blank()
    nd.box(fig, *CLIENT, "mission", BLUE, lit=kind in ("goal", "result"), w=0.17, h=0.22, size=22, sub="action client")
    nd.box(fig, *SERVER, "navigator", BLUE, lit=kind in ("accepted", "feedback"), w=0.17, h=0.22, size=22,
           sub="action server")
    for (p0, p1), on, col, lab, y in ((GOAL, kind == "goal", PURPLE, "goal", 0.715),
                                      (FEED, kind == "feedback", GREEN, "feedback", 0.635),
                                      (RES, kind == "result", ORANGE, "result", 0.525)):
        nd.arrow(fig, p0, p1, col if on else "#BBBBBB", width=5 if on else 2)
        nd.text(fig, 0.28, y, lab, size=19, color=col, anchor="center",
                valign="bottom" if lab != "result" else "top")
        if on:
            nd.dot(fig, nd.lerp(p0, p1, 0.5), col)
    if kind == "goal":
        msg = "<b>goal</b><br>pose: (3.6, 3.5), facing 90°"
        head = "the mission sends the goal"
    elif kind == "accepted":
        msg = "<b>goal accepted</b><br>the navigator starts driving"
        head = "the navigator accepts the goal"
    elif kind == "result":
        msg = "<b>result</b><br>succeeded, error_code 0<br>after 8.0 s"
        head = "the navigator reports the result"
    else:
        f = rk.feedback(t)
        msg = (f"<b>feedback</b><br>navigation_time: {f['t']:.1f} s<br>distance_remaining: "
               f"{f['distance_remaining']:.3f} m<br>estimated_time_remaining: {f['estimated_time_remaining']:.2f} s"
               f"<br>number_of_recoveries: 0")
        head = "feedback while the robot drives" + ("; the person steps in, the goal stays" if t == 2.4 else "")
    nd.text(fig, 0.02, 0.40, msg, size=20)
    nd.text(fig, 0.02, 0.97, f"<b>t = {t:.1f} s</b><br>{head}", size=22)
    k = min(int(round(t / bk.CYCLE)), len(rk.L) - 1)
    o = rk.L[k]
    rd.room(fig)
    fig.add_trace(go.Scatter(x=rk.ROUTE_PTS[:, 0], y=rk.ROUTE_PTS[:, 1], mode="lines",
                             line=dict(color=GREY, width=2.5, dash="dash")))
    if t >= bk.T_PERSON - 1e-9:
        rd.person(fig, bk.PERSON, bk.PERSON_R)
    fig.add_trace(go.Scatter(x=xs[:k + 1, 0], y=xs[:k + 1, 1], mode="lines", line=dict(color=BLUE, width=4)))
    rd.robot(fig, *bk.GOAL[:3], "#BBBBBB", width=2, fill="rgba(0,0,0,0)")
    rd.robot(fig, o["x"][0], o["x"][1], o["x"][2], BLUE)
    rd.axes(fig)
    fig.update_xaxes(domain=[0.55, 1.0])
    return fig


frames = [(0.0, "goal"), (0.0, "accepted")] + [(float(t), "feedback") for t in (1, 2)] + [(2.4, "feedback")] + \
         [(float(t), "feedback") for t in (3, 4, 5, 6, 7)] + [(8.0, "result")]
figs = [frame(t, k) for t, k in frames]
holds = [5, 4] + [3] * (len(figs) - 3) + [14]
holds[4] = 6
make_gif(figs, here / "action", fps=2, holds=holds, keys=[0, 2, 4, 8, 9, len(figs) - 1], cols=2, width=900)
