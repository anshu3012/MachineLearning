"""Animation: the room robot's layered stack at work. Left: the layers, each with its rate; a layer's dot lights in
the frames where it runs. Right: the room. At 0 s the mission (the door pose) is given once and the global planner
makes the A* route once. From 2.30 s, one frame per 0.05 s: the controller runs every frame (20 times a second), the
local planner and the behaviour layer every other frame (10 times a second). At 2.40 s the scan that first shows the
person (0.72 m ahead of the robot's centre) flows up to the local planner, which bends its band 0.146 m clear of
them; the new plan flows down to the controller, which keeps the right wheel at its 0.60 m/s limit and slows the
left wheel (0.58, 0.53, 0.48, 0.43 m/s at 2.40, 2.45, 2.50, 2.55 s), so the robot turns left as it slows. Neither the
mission nor the global plan runs again. Last frame: 8.0 s, the behaviour layer sees the door pose reached and stops
the robot. Run -> stack.gif, stack_frames.png"""
import math
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import stackkit as sk
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from trajkit import A_MAX, L_AXLE, V_WHEEL

here = Path(__file__).parent
R = bk.results()
L = R["loop"]
assert round(L[-1]["t"], 1) == 8.0


def wheels(k, j):
    """Wheel speeds the robot drove j sub-steps (of 0.005 s) into cycle k (bandkit's drive, replayed)."""
    o = L[k]
    P, DT, v = o["P"], o["DT"], o["v"]
    vv, ww, _, _, _ = bk.band_terms(P, DT, v, o["final"])
    Tb = np.concatenate([[0], np.cumsum(DT)])
    hh = bk.CYCLE / 20
    for i in range(j + 1):
        tm = (i + 0.5) * hh
        n = min(np.searchsorted(Tb, tm, side="right") - 1, len(DT) - 1)
        v = float(np.clip(v + np.clip(vv[n] - v, -A_MAX * hh, A_MAX * hh), 0, V_WHEEL))
        w = float(np.clip(ww[n], -(V_WHEEL - v) / (L_AXLE / 2), (V_WHEEL - v) / (L_AXLE / 2)))
    return v + w * L_AXLE / 2, v - w * L_AXLE / 2


WH = {2.40: wheels(24, 0), 2.45: wheels(24, 10), 2.50: wheels(25, 0), 2.55: wheels(25, 10),
      2.30: wheels(23, 0), 2.35: wheels(23, 10), 2.60: wheels(26, 0)}
assert [round(WH[t][1], 2) for t in (2.40, 2.45, 2.50, 2.55)] == [0.58, 0.53, 0.48, 0.43]
assert all(round(WH[t][0], 2) == 0.60 for t in (2.40, 2.45, 2.50, 2.55))


def closest(P):
    seg = np.concatenate([np.linspace(P[k, :2], P[k + 1, :2], 20) for k in range(len(P) - 1)])
    return float(bk.gap(seg[:, 0], seg[:, 1], bk.PERSON).min())


assert round(closest(L[24]["P"]), 3) == 0.146
b, rr = sk.ranges(tuple(L[24]["x"][:3]), bk.PERSON, n=360, rmax=5.6, origin=0.0)
ahead = float(np.min(np.where(np.abs(np.degrees(b)) < 30, rr, 99)))
assert round(ahead, 2) == 0.72

ROWS = [("mission", "go to the door pose (3.6, 3.5), 90°", "once, when the goal is given", 0.905),
        ("behaviour", "task: follow the route to the door", "every 0.1 s", 0.75),
        ("global planner", "A* route over the map, 3.414 m", "once", 0.595),
        ("local planner", "band over the next 1.5 m of route", "every 0.1 s", 0.44),
        ("controller", "wheel speeds within the limits", "every 0.05 s", 0.285),
        ("sensors", "scan every 0.1 s, wheels every 0.05 s", "", 0.10)]
COL = {"mission": GREY, "behaviour": GREY, "global planner": GREY, "local planner": ORANGE, "controller": BLUE,
       "sensors": GREEN}
FILL = {GREY: "rgba(107,107,107,0.22)", ORANGE: "rgba(245,133,24,0.28)", BLUE: "rgba(76,120,168,0.28)",
        GREEN: "rgba(84,162,75,0.28)"}


def frame(t, step, runs, notes, arrows):
    """runs: layers that run in this frame; notes: {layer: text}; arrows: list of (from, to, colour): data going up
    is drawn in the gutter left of the boxes, commands going down in the gutter right of them."""
    fig = go.Figure()
    for name, what, rate, yc in ROWS:
        on = name in runs
        c = COL[name]
        fig.add_shape(type="rect", opacity=1, xref="paper", yref="paper", x0=0.05, x1=0.43, y0=yc - 0.065, y1=yc + 0.065,
                      line=dict(color=c, width=5 if on else 2), fillcolor=FILL[c] if on else "white")
        fig.add_shape(type="circle", opacity=1, xref="paper", yref="paper", x0=0.062, x1=0.084, y0=yc + 0.022, y1=yc + 0.048,
                      line=dict(color=c, width=2), fillcolor=c if on else "white")
        head = f"<b>{name}</b>" + (f" <span style='color:{c}'>({rate})</span>" if rate else "")
        fig.add_annotation(x=0.25, y=yc, xref="paper", yref="paper", showarrow=False, xanchor="center",
                           text=f"{head}<br>{notes.get(name, what)}", font=dict(size=19))
    ypos = {r[0]: r[3] for r in ROWS}
    for a, bto, c in arrows:
        y0, y1 = ypos[a], ypos[bto]
        up = y1 > y0
        x = 0.025 if up else 0.455
        dy = (abs(y1 - y0)) * 980
        fig.add_annotation(x=x, y=y1, xref="paper", yref="paper", ax=0, ay=dy if up else -dy, showarrow=True,
                           arrowhead=2, arrowsize=1.3, arrowwidth=5, arrowcolor=c, text="")
    # the room
    k = min(int(round(t / bk.CYCLE)), len(L) - 1)
    o = L[k]
    rd.room(fig)
    rd.route(fig, bk.ROUTE)
    if t >= bk.T_PERSON - 1e-9:
        rd.person(fig, bk.PERSON, bk.PERSON_R)
    xs = np.array([q["x"] for q in L[:k + 1]])
    fig.add_trace(go.Scatter(x=xs[:, 0], y=xs[:, 1], mode="lines", line=dict(color=BLUE, width=4)))
    show_new = step != "scan"
    P = o["P"] if (show_new or k != 24) else L[24]["warm"][0]
    if k < len(L) - 1:
        rd.band(fig, P, ORANGE, size=7)
    rd.robot(fig, *bk.GOAL[:3], "#BBBBBB", width=2, fill="rgba(0,0,0,0)")
    rd.robot(fig, o["x"][0], o["x"][1], o["x"][2], BLUE)
    fig.add_annotation(x=1.35, y=0.62, text=f"<b>t = {t:.2f} s</b>", showarrow=False, xanchor="left",
                       font=dict(size=24))
    rd.axes(fig)
    fig.update_xaxes(domain=[0.5, 1.0])
    fig.update_layout(template="simple_white", font=FONT, width=1300, height=1000, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


def wh(t):
    r, l = WH[round(t, 2)]
    return f"wheels: right {r:.2f}, left {l:.2f} m/s"


F = []
F.append(frame(0.0, "", {"mission", "global planner"},
               {"mission": "goal given: door pose (3.6, 3.5), 90°",
                "global planner": "A* route made once: 3.414 m"},
               [("mission", "global planner", GREY)]))
for t in (2.30, 2.35):
    runs = {"controller", "sensors"} | ({"local planner", "behaviour"} if round(t * 20) % 2 == 0 else set())
    F.append(frame(t, "", runs, {"controller": wh(t)}, []))
F.append(frame(2.40, "scan", {"sensors"}, {"sensors": "scan at 2.40 s: person 0.72 m ahead"},
               [("sensors", "local planner", RED)]))
F.append(frame(2.40, "plan", {"local planner", "behaviour"},
               {"sensors": "scan at 2.40 s: person 0.72 m ahead",
                "local planner": "band bends left, 0.146 m clear",
                "behaviour": "task unchanged: follow the route"}, []))
F.append(frame(2.40, "cmd", {"controller"},
               {"local planner": "band bends left, 0.146 m clear", "controller": wh(2.40)},
               [("local planner", "controller", ORANGE)]))
for t in (2.45, 2.50, 2.55, 2.60):
    runs = {"controller", "sensors"} | ({"local planner", "behaviour"} if round(t * 20) % 2 == 0 else set())
    F.append(frame(t, "", runs, {"controller": wh(t), "local planner": "band bends left, 0.146 m clear"}, []))
F.append(frame(8.0, "", {"behaviour", "controller"},
               {"behaviour": "door pose reached: stop", "controller": "wheels: right 0.00, left 0.00 m/s"},
               [("behaviour", "controller", GREY)]))
holds = [10, 4, 4, 10, 10, 12, 5, 5, 5, 5, 18]
make_gif(F, here / "stack", fps=4, holds=holds, keys=[0, 3, 4, 5, 7, 10], cols=2, width=900)
