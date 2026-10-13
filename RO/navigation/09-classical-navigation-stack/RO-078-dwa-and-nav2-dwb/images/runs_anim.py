"""Two runs of our Python version of DWB's algorithm in the same room, one frame per 0.25 s. Purple: the global plan
made once from the map, as in RO-058 (purple dashed); the robot brakes for the person, stops 0.07 m from them at
6.75 s and is aborted at 12.45 s (the progress checker: no 0.5 m of movement in 10 s). Blue: the plan remade every
second (grey dashed, Nav2's default behaviour tree); it goes round and the goal checker accepts it at 13.3 s.
Run -> runs_anim.gif, runs_anim_frames.png"""
import dwbkit as d
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, GREY, PURPLE, make_gif

R = d.results()
A, B = R["once"], R["replan"]
CA, CB = A["cycles"], B["cycles"]
xa = np.array([c["x"] for c in CA])
xb = np.array([c["x"] for c in CB])
assert A["reason"] == "failed to make progress" and round(CA[-1]["t"], 2) == 12.45
assert round(B["t_arrive"], 2) == 13.3
plan_once = A["plans"][0][1]
dt = 0.05


def state(C, t):
    k = min(int(round(t / dt)), len(C) - 1)
    return k, C[k]


def frame(t):
    fig = go.Figure()
    rd.room(fig)
    if t >= d.T_PERSON - 1e-9:
        rd.person(fig, d.PERSON, d.PERSON_R)
    rd.plan(fig, plan_once, color=PURPLE)
    planb = [p for tp, p in B["plans"] if tp <= t + 1e-9][-1]
    rd.plan(fig, planb, color=GREY)
    ka, oa = state(CA, t)
    kb, ob = state(CB, t)
    fig.add_trace(go.Scatter(x=xa[:ka + 1, 0], y=xa[:ka + 1, 1], mode="lines", line=dict(color=PURPLE, width=5)))
    fig.add_trace(go.Scatter(x=xb[:kb + 1, 0], y=xb[:kb + 1, 1], mode="lines", line=dict(color=BLUE, width=5)))
    rd.robot(fig, *d.GOAL, "#BBBBBB", width=2, fill="rgba(0,0,0,0)")
    rd.robot(fig, oa["x"][0], oa["x"][1], oa["x"][2], PURPLE)
    rd.robot(fig, ob["x"][0], ob["x"][1], ob["x"][2], BLUE)
    if t >= CA[-1]["t"] - 1e-9:
        sa = "<b>aborted at 12.45 s</b>:<br>no 0.5 m of progress in 10 s"
    elif t >= 6.75 - 1e-9:
        sa = "stopped 0.07 m from the person"
    else:
        sa = f"speed {oa['v']:.2f} m/s"
    sb = "<b>arrived at 13.3 s</b>" if t >= B["t_arrive"] - 1e-9 else f"speed {ob['v']:.2f} m/s"
    lines = [f"<b>t = {t:.2f} s</b>", "",
             f"<span style='color:{PURPLE}'><b>plan made once</b></span>", f"<span style='color:{PURPLE}'>{sa}</span>",
             "", f"<span style='color:{BLUE}'><b>plan remade every 1 s</b></span>",
             f"<span style='color:{BLUE}'>{sb}</span>", "",
             f"<span style='color:{GREY}'>our Python version<br>of DWB's algorithm</span>"]
    fig.add_annotation(x=0.5, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.9)")
    rd.zoom(fig, (0.45, 4.6), (0.45, 4.25))
    fig.update_layout(template="simple_white", font=FONT, width=900, height=830, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


ts = list(np.round(np.arange(0, 13.3 + 1e-9, 0.25), 2))
if ts[-1] != 13.3:
    ts.append(13.3)
for extra in (6.75, 12.45):
    if extra not in ts:
        ts.append(extra)
ts = sorted(ts)
figs = [frame(t) for t in ts]
holds = [3] + [1] * (len(ts) - 2) + [14]
holds[ts.index(6.75)] = 5
holds[ts.index(12.45)] = 8
make_gif(figs, "runs_anim", fps=5, holds=holds, keys=[ts.index(3.0), ts.index(6.75), ts.index(12.45),
                                                      len(ts) - 1], cols=2)
