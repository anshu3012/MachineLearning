"""Animation for the Overview: the robot drives from rest at (2.0, 1.0) facing 30 degrees to the door pose (3.6, 3.5)
facing 90 degrees. The global plan (grey dashed) is RO-034's A* route, made once from the map. At 2.4 s a person
(pink disk) steps onto the route, 0.6 m ahead; the map does not have them. Every 0.1 s the local planner takes the
next 1.5 m of the route and re-optimises its timed elastic band (orange: poses with headings) from the robot to the
local goal (orange cross), and the robot drives the band's first 0.1 s. One frame per 0.2 s; the last holds at the
arrival, 8.0 s. Run -> overview.gif, overview_frames.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
R = bk.results()
L = R["loop"]
T_end = L[-1]["t"]
xs = np.array([o["x"] for o in L])
assert round(T_end, 1) == 8.0 and round(R["free"][-1]["t"], 1) == 6.7
assert round(float(bk.gap(xs[:, 0], xs[:, 1], bk.PERSON).min()), 2) == 0.14


def frame(k):
    o = L[k]
    fig = go.Figure()
    rd.room(fig)
    rd.route(fig, bk.ROUTE)
    if o["person"] is not None:
        rd.person(fig, bk.PERSON, bk.PERSON_R)
    fig.add_trace(go.Scatter(x=xs[:k + 1, 0], y=xs[:k + 1, 1], mode="lines", line=dict(color=BLUE, width=5)))
    rd.band(fig, o["P"], ORANGE, size=8)
    g = o["goal"]
    fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=16, color=ORANGE,
                                                                             line=dict(width=1))))
    rd.robot(fig, *GOAL_POSE, "#BBBBBB", width=2, fill="rgba(0,0,0,0)")
    rd.robot(fig, o["x"][0], o["x"][1], o["x"][2], BLUE)
    done = k == len(L) - 1
    lines = [f"<b>t = {o['t']:.1f} s</b>" + (", arrived" if done else ""), f"speed {o['v']:.2f} m/s",
             f"<span style='color:{GREY}'>global plan: once, from the map</span>",
             f"<span style='color:{ORANGE}'>local plan: every 0.1 s, {len(o['P'])} poses</span>"]
    if o["person"] is not None:
        lines.append("<span style='color:#C2185B'>person seen at 2.4 s</span>")
    fig.add_annotation(x=1.35, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=20), bgcolor="rgba(255,255,255,0.9)")
    fig.add_annotation(x=2.0, y=0.62, text="start", showarrow=False, font=dict(size=18, color="#555555"))
    rd.axes(fig)
    fig.update_layout(template="simple_white", font=FONT, width=760, height=1000, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


GOAL_POSE = tuple(bk.GOAL[:3])
ks = list(range(0, len(L), 2))
if ks[-1] != len(L) - 1:
    ks.append(len(L) - 1)
k_person = ks.index(24)
figs = [frame(k) for k in ks]
holds = [4] + [1] * (len(figs) - 2) + [14]
holds[k_person] = 6
make_gif(figs, here / "overview", fps=5, holds=holds, keys=[0, k_person - 1, k_person, k_person + 3, 30,
                                                             len(figs) - 1], cols=3, width=560)
