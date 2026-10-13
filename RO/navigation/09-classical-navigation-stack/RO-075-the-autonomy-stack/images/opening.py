"""Animation for the Overview: the same robot, the same person, two ways to run the software. Left: one
sense-plan-act loop that looks at the world once a second (at 0, 1, 2, 3 s ...); between looks it drives the plan it
made from the map. The person steps in at 2.4 s; the loop first sees them at 3.0 s, 0.113 m away at 0.591 m/s, and
brakes at 0.5 m/s^2, but touches them at 3.22 s. Right: RO-058's layered stack, whose local planner looks every 0.1 s:
it bends round the person in the cycle at 2.4 s and reaches the door at 8.0 s. One frame per 0.2 s.
Run -> opening.gif, opening_frames.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import stackkit as sk
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
R = bk.results()
L, F = R["loop"], R["free"]
S = sk.spa(1.0)
k_touch = int(np.argmax(S["gap"] < 0))
assert round(S["t_look"], 2) == 3.0 and round(S["gap_look"], 3) == 0.113 and round(S["v_look"], 3) == 0.591
assert round(S["t"][k_touch], 2) == 3.22 and round(L[-1]["t"], 1) == 8.0
plan = np.array([o["x"][:2] for o in F])
xs_L = np.array([o["x"] for o in L])


def spa_pose(t):
    """The loop's robot at time t, drawn where it first touches the person from then on (the run does not model
    what happens after contact)."""
    k = min(int(round(t / sk.DT)), len(S["t"]) - 1, k_touch)
    p = S["x"][k]
    q = S["x"][min(k + 1, len(S["x"]) - 1)] if k + 1 < len(S["x"]) else p
    r = S["x"][max(k - 1, 0)]
    d = q - r if np.hypot(*(q - r)) > 1e-6 else S["x"][k] - S["x"][max(k - 5, 0)]
    return p, float(np.arctan2(d[1], d[0])), float(S["v"][k]), k


def frame(t):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.03,
                        subplot_titles=["one loop, a look every 1 s", "layered stack, local planner every 0.1 s"])
    fig.update_annotations(font_size=23)
    seen = t >= bk.T_PERSON - 1e-9
    # left: sense-plan-act at 1 Hz
    rc = (1, 1)
    rd.room(fig, rc=rc)
    rd.robot(fig, *bk.GOAL[:3], "#BBBBBB", rc=rc, width=2, fill="rgba(0,0,0,0)")
    fig.add_trace(go.Scatter(x=plan[:, 0], y=plan[:, 1], mode="lines", line=dict(color=GREY, width=2.5, dash="dot")),
                  row=1, col=1)
    if seen:
        rd.person(fig, bk.PERSON, bk.PERSON_R, rc=rc)
    p, th, v, k = spa_pose(t)
    trail = S["x"][:k + 1]
    fig.add_trace(go.Scatter(x=trail[:, 0], y=trail[:, 1], mode="lines", line=dict(color=BLUE, width=5)), row=1, col=1)
    touched = k >= k_touch
    rd.robot(fig, p[0], p[1], th, RED if touched else BLUE, rc=rc)
    stamp = f"{t:.2f}" if abs(t * 10 - round(t * 10)) > 1e-6 else f"{t:.1f}"
    touched = k >= k_touch
    lines = [f"<b>t = {stamp} s</b>", (f"speed at contact {v:.2f} m/s" if touched else f"speed {v:.2f} m/s"),
             "looks once a second"]
    if t >= S["t_look"] - 1e-9:
        lines.append(f"<span style='color:{ORANGE}'>3.0 s: sees the person, brakes</span>")
    if touched:
        lines.append(f"<span style='color:{RED}'>touches them at {S['t'][k_touch]:.2f} s</span>")
    elif seen:
        lines.append("<span style='color:#C2185B'>person stepped in at 2.4 s</span>")
    fig.add_annotation(x=1.35, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=20), bgcolor="rgba(255,255,255,0.9)", row=1, col=1)
    # right: the layered stack of RO-058
    rc = (1, 2)
    rd.room(fig, rc=rc)
    rd.route(fig, bk.ROUTE, rc=rc)
    if seen:
        rd.person(fig, bk.PERSON, bk.PERSON_R, rc=rc)
    j = min(int(round(t / bk.CYCLE)), len(L) - 1)
    o = L[j]
    fig.add_trace(go.Scatter(x=xs_L[:j + 1, 0], y=xs_L[:j + 1, 1], mode="lines", line=dict(color=BLUE, width=5)),
                  row=1, col=2)
    if j < len(L) - 1:
        rd.band(fig, o["P"], ORANGE, rc=rc, size=7)
    rd.robot(fig, *bk.GOAL[:3], "#BBBBBB", rc=rc, width=2, fill="rgba(0,0,0,0)")
    rd.robot(fig, o["x"][0], o["x"][1], o["x"][2], BLUE, rc=rc)
    done = j == len(L) - 1
    lines = [f"<b>t = {min(t, o['t']):.1f} s</b>" + (", at the door" if done else ""), f"speed {o['v']:.2f} m/s",
             f"<span style='color:{ORANGE}'>local plan: every 0.1 s</span>"]
    if seen:
        lines.append("<span style='color:#C2185B'>person seen at 2.4 s</span>")
    fig.add_annotation(x=1.35, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=20), bgcolor="rgba(255,255,255,0.9)", row=1, col=2)
    rd.axes(fig, rc=(1, 1))
    rd.axes(fig, rc=(1, 2))
    fig.update_layout(template="simple_white", font=FONT, width=1300, height=900, showlegend=False,
                      margin=dict(l=10, r=10, t=50, b=10))
    return fig


ts = [round(0.2 * i, 1) for i in range(41)]
for extra in (3.0, 3.2, 3.22):
    if extra not in ts:
        ts.append(extra)
ts = sorted(ts)
figs = [frame(t) for t in ts]
holds = [5] + [1] * (len(ts) - 2) + [16]
for t_hold, h in ((2.4, 5), (3.0, 5), (3.22, 8)):
    holds[ts.index(t_hold)] = h
make_gif(figs, here / "opening", fps=5, holds=holds,
         keys=[ts.index(2.4), ts.index(3.0), ts.index(3.22), len(ts) - 1], cols=2, width=900)
