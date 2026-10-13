"""Animation for the Overview: the main run of our Python version of DWB's algorithm in the room, one frame per
0.2 s. The robot starts at rest at (2.0, 1.0) facing 30 degrees; the door pose is (3.6, 3.5) facing 90 degrees. Grey
dashed: the global plan, A* on 0.5 m cells, remade once a second (Nav2's default behaviour tree). Orange: the
rollout DWB chose in this cycle (1.7 s ahead). Blue line: where the robot has driven. At 2.4 s a person steps onto
the plan; the robot brakes, the plan made at 3.0 s goes left of them, the robot passes them, turns on the spot
from 9.7 s and is accepted by the goal checker at 13.3 s, 0.23 m from the door pose.
Run -> overview.gif, overview_frames.png"""
import math

import dwbkit as d
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

R = d.results()
run = R["replan"]
C = run["cycles"]
plans = run["plans"]
xs = np.array([c["x"] for c in C])
assert round(run["t_arrive"], 2) == 13.3
assert round(float(np.hypot(*(C[-1]["x"][:2] - d.GOAL[:2]))), 2) == 0.23


def note(t):
    if t < 2.4 - 1e-9:
        return "drives along the plan"
    if t < 3.0 - 1e-9:
        return "person seen: brakes"
    if t < 4.45:
        return "new plan (3.0 s) goes<br>left of the person"
    if t < 5.05:
        return "passes the person"
    if t < 9.7 - 1e-9:
        return "follows the new plan"
    if t < run["t_arrive"] - 1e-9:
        return "within 0.25 m: turns on the spot"
    return "<b>goal checker: arrived</b><br>0.23 m from the door pose"


def frame(k):
    o = C[k]
    fig = go.Figure()
    rd.room(fig)
    plan = [p for t, p in plans if t <= o["t"] + 1e-9][-1]
    rd.plan(fig, plan)
    if o["person"] is not None:
        rd.person(fig, d.PERSON, d.PERSON_R)
    fig.add_trace(go.Scatter(x=xs[:k + 1, 0], y=xs[:k + 1, 1], mode="lines", line=dict(color=BLUE, width=5)))
    if o["rec"] is not None and o["rec"].get("traj") is not None:
        rd.arcs(fig, [o["rec"]["traj"]], ORANGE, width=4)
    rd.robot(fig, *d.GOAL, "#BBBBBB", width=2, fill="rgba(0,0,0,0)")
    rd.robot(fig, o["x"][0], o["x"][1], o["x"][2], BLUE)
    lines = [f"<b>t = {o['t']:.1f} s</b>", f"speed {o['v']:.2f} m/s", note(o["t"]), "",
             f"<span style='color:{GREY}'>dashed: global plan,<br>remade every 1 s</span>",
             f"<span style='color:{ORANGE}'>orange: chosen rollout,<br>1.7 s ahead</span>",
             f"<span style='color:{GREY}'>our Python version<br>of DWB's algorithm</span>"]
    fig.add_annotation(x=0.5, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.9)")
    fig.add_annotation(x=2.0, y=0.65, text="start", showarrow=False, font=dict(size=17, color="#555555"))
    rd.zoom(fig, (0.45, 4.6), (0.45, 4.25))
    fig.update_layout(template="simple_white", font=FONT, width=900, height=830, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


ks = list(range(0, len(C), 4))
if ks[-1] != len(C) - 1:
    ks.append(len(C) - 1)
figs = [frame(k) for k in ks]
holds = [4] + [1] * (len(figs) - 2) + [14]
k24 = ks.index(48)
holds[k24] = 6
keys = [ks.index(k) for k in (48, 60, 96)] + [len(figs) - 1]
make_gif(figs, "overview", fps=5, holds=holds, keys=keys, cols=2)
