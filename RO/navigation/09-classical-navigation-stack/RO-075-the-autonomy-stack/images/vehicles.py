"""Animation: Braitenberg's four two-sensor vehicles on an open floor with one lamp (yellow, at the origin), all
starting 1.62 m from it, at (-1.5, -0.6) facing along x, so the lamp is ahead and to the left. Each vehicle is our
disk robot with two light sensors at its front rim, 45 degrees either side of its heading; each wire multiplies its
sensor's reading by 2, and the wheels follow at once (no acceleration limit). 2a (same side, more light = faster)
turns away and slows; 2b (crossed, faster) turns to the lamp and reaches it at 2.85 s; 3a (same side, slower) turns
to it and stops 0.88 m away; 3b (crossed, slower) comes within 1.48 m and then turns away and leaves at full speed.
One frame per 0.1 s for 8 s; at 8 s 3a is 0.89 m from the lamp and nearly still. Run -> vehicles.gif, vehicles_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import stackkit as sk
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif
from plotly.subplots import make_subplots
from trajkit import R_BODY

here = Path(__file__).parent
NAMES = {"2a": "2a fear: same side, +", "2b": "2b aggression: crossed, +", "3a": "3a love: same side, −",
         "3b": "3b explorer: crossed, −"}
RUNS = {w: sk.run_open(w, t_end=15) for w in NAMES}
d_end = {w: float(np.hypot(*RUNS[w][-1]["x"][:2])) for w in NAMES}
assert round(RUNS["2b"][-1]["t"], 2) == 2.85 and round(d_end["3a"], 2) == 0.87
assert round(min(np.hypot(o["x"][0], o["x"][1]) for o in RUNS["3b"]), 2) == 1.48
XR, YR = (-2.9, 0.9), (-2.7, 0.9)
LAMP_C = "#E8B400"


def panel(fig, w, t, rc):
    rec = RUNS[w]
    k = min(int(round(t / sk.DT)), len(rec) - 1)
    o = rec[k]
    xs = np.array([q["x"] for q in rec[:k + 1]])
    th = np.linspace(0, 2 * math.pi, 40)
    for rad, op in ((0.5, 0.10), (0.3, 0.18)):
        fig.add_trace(go.Scatter(x=rad * np.cos(th), y=rad * np.sin(th), fill="toself", fillcolor=f"rgba(232,180,0,{op})",
                                 line=dict(width=0), mode="lines", hoverinfo="skip"), row=rc[0], col=rc[1])
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(symbol="star", size=24, color=LAMP_C,
                                                                     line=dict(color="#8A6A00", width=1))),
                  row=rc[0], col=rc[1])
    fig.add_trace(go.Scatter(x=xs[:, 0], y=xs[:, 1], mode="lines", line=dict(color=BLUE, width=4)), row=rc[0], col=rc[1])
    x, y, h = o["x"][:3]
    fig.add_trace(go.Scatter(x=x + R_BODY * np.cos(th), y=y + R_BODY * np.sin(th), mode="lines", fill="toself",
                             fillcolor="rgba(255,255,255,0.7)", line=dict(color=BLUE, width=3)), row=rc[0], col=rc[1])
    fig.add_trace(go.Scatter(x=[x, x + R_BODY * math.cos(h)], y=[y, y + R_BODY * math.sin(h)], mode="lines",
                             line=dict(color=BLUE, width=4)), row=rc[0], col=rc[1])
    for side in (1, -1):
        a = h + side * sk.SENSOR_ANGLE
        fig.add_trace(go.Scatter(x=[x + R_BODY * math.cos(a)], y=[y + R_BODY * math.sin(a)], mode="markers",
                                 marker=dict(size=11, color=ORANGE)), row=rc[0], col=rc[1])
    sL, sR = o["s"]
    vL, vR = o["wheels"]
    arrived = w == "2b" and k == len(rec) - 1
    txt = [f"<b>{NAMES[w]}</b>", f"readings: left {sL:.2f}, right {sR:.2f}",
           f"wheels: left {vL:.2f}, right {vR:.2f} m/s", f"lamp {math.hypot(x, y):.2f} m away"]
    if arrived:
        txt.append(f"reaches the lamp at {rec[-1]['t']:.2f} s")
    fig.add_annotation(x=XR[0] + 0.05, y=YR[1] - 0.05, text="<br>".join(txt), showarrow=False, xanchor="left",
                       yanchor="top", align="left", font=dict(size=17), bgcolor="rgba(255,255,255,0.85)",
                       row=rc[0], col=rc[1])


def frame(t):
    fig = make_subplots(rows=2, cols=2, horizontal_spacing=0.03, vertical_spacing=0.03)
    for i, w in enumerate(NAMES):
        rc = (i // 2 + 1, i % 2 + 1)
        panel(fig, w, t, rc)
        n = i + 1
        fig.update_xaxes(range=list(XR), visible=False, row=rc[0], col=rc[1])
        fig.update_yaxes(range=list(YR), visible=False, scaleanchor=f"x{n if n > 1 else ''}", row=rc[0], col=rc[1])
    fig.add_annotation(x=0.5, y=1.0, xref="paper", yref="paper", yanchor="bottom", text=f"<b>t = {t:.1f} s</b>",
                       showarrow=False, font=dict(size=22))
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1000, showlegend=False,
                      margin=dict(l=10, r=10, t=40, b=10))
    return fig


ts = [round(0.1 * i, 1) for i in range(81)]
assert round(math.hypot(*RUNS['3a'][800]['x'][:2]), 2) == 0.89
figs = [frame(t) for t in ts]
holds = [6] + [1] * (len(ts) - 2) + [16]
make_gif(figs, here / "vehicles", fps=8, holds=holds, keys=[0, 15, 30, 80], cols=2, width=760)
