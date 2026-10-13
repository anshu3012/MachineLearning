"""Animation: the whole goal in the room, one frame every 0.25 s of the main run (our Python version of Nav2's
servers, written from their code and the bring-up parameters; not Nav2 running). Black disk: the robot where it
truly is; blue ring: where AMCL says it is; blue line: the global plan from NavFn (replaced at 3.0 s); orange: the
DWB rollout chosen in that controller cycle; pink: the person, from 2.4 s. Events: 2.4 s the laser sees the person; 2.55 s the collision monitor slows the command by 0.917;
3.0 s the tree's path check fails and NavFn replans (2.986 m); 11.50 s the goal checker accepts.
Run -> drive.gif, drive_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import navdraw as nd
import nav2sim as N
import roomdraw as rd
from gifkit import BLUE, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
R = N.results()
m = R["main"]
L = m["log"]
assert round(m["t_final"], 2) == 11.51 and m["plans"][1][0] == 3.0
EVENTS = {2.4: "the laser sees the person", 2.55: "the collision monitor scales the command by 0.917",
          3.0: "the path check fails: NavFn replans, 2.986 m"}
mon = [x for x in L if x["zone"]][0]
assert round(mon["t"], 2) == 2.55 and round(mon["tc"] / 1.2, 4) == 0.9167


def to_map(m2o, P):
    c, s = math.cos(m2o[2]), math.sin(m2o[2])
    return np.column_stack([m2o[0] + c * P[:, 0] - s * P[:, 1], m2o[1] + s * P[:, 0] + c * P[:, 1]])


def frame(k, title):
    x = L[k]
    t = x["t"]
    fig = go.Figure()
    rd.room(fig)
    plan = [p for (tp, p) in m["plans"] if tp <= t + 1e-9][-1]
    nd.plan(fig, plan, BLUE, 3)
    if x["person"] is not None:
        nd.person(fig)
    trail = np.array([y["true"][:2] for y in L[:k + 1]])
    fig.add_trace(go.Scatter(x=trail[:, 0], y=trail[:, 1], mode="lines", line=dict(color="black", width=2),
                             hoverinfo="skip"))
    if x["best"] is not None:
        b = to_map(x["m2o"], x["best"][:, :2])
        fig.add_trace(go.Scatter(x=b[:, 0], y=b[:, 1], mode="lines", line=dict(color=ORANGE, width=4),
                                 hoverinfo="skip"))
    rd.robot(fig, *x["true"], "black")
    a = np.linspace(0, 2 * math.pi, 40)
    fig.add_trace(go.Scatter(x=x["map"][0] + 0.25 * np.cos(a), y=x["map"][1] + 0.25 * np.sin(a), mode="lines",
                             line=dict(color=BLUE, width=2), hoverinfo="skip"))
    nd.goal(fig)
    fig.add_annotation(x=0.02, y=0.02, xref="paper", yref="paper", xanchor="left", yanchor="bottom",
                       text=f"t = {t:.2f} s<br>v = {x['v']:.2f} m/s<br>w = {x['w']:.2f} rad/s", showarrow=False,
                       align="left", font=dict(size=18), bgcolor="rgba(255,255,255,0.8)")
    nd.view(fig, xr=(1.3, 4.6), yr=(0.45, 4.25))
    fig.update_yaxes(scaleanchor="x")
    nd.layout(fig, 820, 900, title, margin=dict(l=10, r=10, t=70, b=10))
    return fig


figs, holds, keys = [], [], []
times = [round(x["t"], 2) for x in L]
pick = [i for i, t in enumerate(times) if abs(t / 0.25 - round(t / 0.25)) < 1e-6 or t in EVENTS]
for i in pick:
    t = times[i]
    title = f"{t:.2f} s: {EVENTS[t]}" if t in EVENTS else f"one goal through Nav2 (our Python version), {t:.2f} s"
    figs.append(frame(i, title))
    holds.append(8 if t in EVENTS else 1)
    if t in (0.0, 2.55, 3.0, 6.0):
        keys.append(len(figs) - 1)
assert round(L[-1]["t"], 2) == 11.50
figs.append(frame(len(L) - 1, f"{L[-1]['t']:.2f} s: the goal checker accepts; the robot stops"))
holds.append(20)
keys.append(len(figs) - 1)
holds[0] = 6
make_gif(figs, here / "drive", fps=6, holds=holds, keys=keys, cols=3, width=700)
