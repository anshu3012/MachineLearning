"""Animation: the two subsumption levels of Figure 7 drive the room robot, with the person stepping in at 2.4 s.
Left: the room; the robot's 36 range readings out to 1.0 m from its rim (red where a reading is under 0.5 m and
pushes), the lamp at the door pose. Right: the three modules, lit when their command reaches the wheels. Level 1
(go to the light) drives until 3.2 s, when the person is 0.411 m ahead and collide halts the robot; from 3.91 s it
stands still, 0.283 m from the person and 1.748 m from the lamp, because the lamp turns it towards the person and the
push turns it away by the same amount. The last frame is at 20 s: nothing has changed. One frame per 0.2 s to 6 s.
Run -> subsume.gif, subsume_frames.png"""
import math
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import stackkit as sk
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from trajkit import R_BODY

here = Path(__file__).parent
REC = sk.run_subsumption(t_end=20)
first_halt = next(o for o in REC if o["who"] == "collide: halt")
end = REC[-1]
assert round(first_halt["t"], 2) == 3.2 and round(float(sk.person_gap(first_halt["x"][:2])[0]), 3) == 0.411
assert round(float(sk.person_gap(end["x"][:2])[0]), 3) == 0.283
assert round(float(np.hypot(*(end["x"][:2] - sk.LAMP))), 3) == 1.748 and not any(o["hit"] for o in REC)
LAMP_C = "#E8B400"
BOXES = [("go to the light", "level 1", ORANGE, 0.78), ("runaway", "level 0", GREY, 0.50),
         ("collide: halt", "level 0", RED, 0.22)]


def frame(t):
    k = min(int(round(t / sk.DT)), len(REC) - 1)
    o = REC[k]
    xs = np.array([q["x"] for q in REC[:k + 1]])
    fig = go.Figure()
    rd.room(fig)
    if o["person"] is not None:
        rd.person(fig, bk.PERSON, bk.PERSON_R)
    th = np.linspace(0, 2 * math.pi, 40)
    for rad, op in ((0.5, 0.10), (0.3, 0.18)):
        fig.add_trace(go.Scatter(x=sk.LAMP[0] + rad * np.cos(th), y=sk.LAMP[1] + rad * np.sin(th), fill="toself",
                                 fillcolor=f"rgba(232,180,0,{op})", line=dict(width=0), mode="lines"))
    fig.add_trace(go.Scatter(x=[sk.LAMP[0]], y=[sk.LAMP[1]], mode="markers",
                             marker=dict(symbol="star", size=26, color=LAMP_C, line=dict(color="#8A6A00", width=1))))
    fig.add_trace(go.Scatter(x=xs[:, 0], y=xs[:, 1], mode="lines", line=dict(color=BLUE, width=5)))
    x, y, h, v = o["x"]
    for bi, ri in zip(o["b"], o["r"]):
        a = h + bi
        c = RED if ri < sk.FORCE_DIST else "#BBBBBB"
        fig.add_trace(go.Scatter(x=[x + R_BODY * math.cos(a), x + (R_BODY + ri) * math.cos(a)],
                                 y=[y + R_BODY * math.sin(a), y + (R_BODY + ri) * math.sin(a)], mode="lines",
                                 line=dict(color=c, width=1.5)))
    rd.robot(fig, x, y, h, BLUE)
    who = o["who"]
    lines = [f"<b>t = {t:.1f} s</b>", f"speed {v:.2f} m/s", f"gap to the {'person' if o['person'] is not None else 'nearest obstacle'}: "
             f"{float(sk.person_gap(o['x'][:2])[0]) if o['person'] is not None else float(bk.gap(np.array([x]), np.array([y]))[0]):.2f} m",
             f"lamp {math.hypot(x - sk.LAMP[0], y - sk.LAMP[1]):.2f} m away"]
    fig.add_annotation(x=1.35, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.9)")
    # the modules, right
    for name, lev, col, yc in BOXES:
        on = (name == who) or (name == "go to the light" and who == "collide: halt")
        fill = {ORANGE: "rgba(245,133,24,0.30)", GREY: "rgba(107,107,107,0.25)", RED: "rgba(228,87,86,0.30)"}[col]
        fig.add_shape(type="rect", opacity=1, xref="paper", yref="paper", x0=0.64, x1=0.99, y0=yc - 0.09, y1=yc + 0.09,
                      line=dict(color=col, width=4 if on else 1.5), fillcolor=fill if on else "rgba(255,255,255,1)")
        state = {"go to the light": "steers to the lamp" + (": turn only" if who == "collide: halt" else ""),
                 "runaway": "command replaced (S)",
                 "collide: halt": "halt: forward speed 0" if who == "collide: halt" else "nothing ahead within 0.42 m"}[name]
        fig.add_annotation(x=0.815, y=yc, xref="paper", yref="paper", showarrow=False, xanchor="center",
                           text=f"<b>{name}</b> ({lev})<br>{state}", font=dict(size=18, color="black" if on else GREY))
    fig.add_annotation(x=0.815, y=0.97, xref="paper", yref="paper", showarrow=False, xanchor="center", text="<b>reaching the wheels</b>",
                       font=dict(size=19))
    rd.axes(fig)
    fig.update_xaxes(domain=[0, 0.6])
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=1000, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


ts = [round(0.2 * i, 1) for i in range(31)] + [20.0]
figs = [frame(t) for t in ts]
holds = [5] + [1] * (len(ts) - 2) + [16]
holds[ts.index(2.4)] = 4
holds[ts.index(3.2)] = 5
make_gif(figs, here / "subsume", fps=6, holds=holds, keys=[ts.index(2.4), ts.index(3.2), ts.index(4.0), len(ts) - 1],
         cols=2, width=800)
