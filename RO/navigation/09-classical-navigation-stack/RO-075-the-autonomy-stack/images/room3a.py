"""Animation: vehicle 3a (same-side wires, more light = slower wheel) in the room, with a lamp at the door pose
(3.6, 3.5) and no person. It starts at rest at (2.0, 1.0) facing 30 degrees, with our robot's limits (each wheel at
most 0.6 m/s, forward speed changing by at most 0.5 m/s^2). It turns towards the lamp and slows as the light grows,
but nothing in its wiring senses the table: it creeps into the table's edge at 9.84 s, 0.92 m from the lamp.
One frame per 0.2 s. Run -> room3a.gif, room3a_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import stackkit as sk
from gifkit import BLUE, FONT, ORANGE, RED, make_gif

here = Path(__file__).parent
REC = sk.run_braitenberg()
T_HIT = REC[-1]["t"]
assert REC[-1]["hit"] and round(T_HIT, 2) == 9.84
assert round(float(np.hypot(*(REC[-1]["x"][:2] - sk.LAMP))), 2) == 0.92
LAMP_C = "#E8B400"


def frame(t):
    k = min(int(round(t / sk.DT)), len(REC) - 1)
    o = REC[k]
    xs = np.array([q["x"] for q in REC[:k + 1]])
    fig = go.Figure()
    rd.room(fig)
    th = np.linspace(0, 2 * math.pi, 40)
    for rad, op in ((0.5, 0.10), (0.3, 0.18)):
        fig.add_trace(go.Scatter(x=sk.LAMP[0] + rad * np.cos(th), y=sk.LAMP[1] + rad * np.sin(th), fill="toself",
                                 fillcolor=f"rgba(232,180,0,{op})", line=dict(width=0), mode="lines"))
    fig.add_trace(go.Scatter(x=[sk.LAMP[0]], y=[sk.LAMP[1]], mode="markers",
                             marker=dict(symbol="star", size=26, color=LAMP_C, line=dict(color="#8A6A00", width=1))))
    fig.add_trace(go.Scatter(x=xs[:, 0], y=xs[:, 1], mode="lines", line=dict(color=BLUE, width=5)))
    hit = k == len(REC) - 1
    x, y, h, v = o["x"]
    rd.robot(fig, x, y, h, RED if hit else BLUE)
    for side in (1, -1):
        a = h + side * sk.SENSOR_ANGLE
        fig.add_trace(go.Scatter(x=[x + 0.25 * math.cos(a)], y=[y + 0.25 * math.sin(a)], mode="markers",
                                 marker=dict(size=12, color=ORANGE)))
    sL, sR = o["s"]
    vL, vR = o["wheels"]
    lines = [f"<b>t = {t:.2f} s</b>" if hit else f"<b>t = {t:.1f} s</b>", f"speed {v:.2f} m/s",
             f"readings: left {sL:.2f}, right {sR:.2f}", f"wheel commands: left {vL:.2f}, right {vR:.2f}"]
    if hit:
        lines.append(f"<span style='color:{RED}'>touches the table, {math.hypot(*(o['x'][:2] - sk.LAMP)):.2f} m "
                     "from the lamp</span>")
    fig.add_annotation(x=1.35, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.9)")
    fig.add_annotation(x=sk.LAMP[0] + 0.12, y=sk.LAMP[1] + 0.16, text="lamp", showarrow=False, xanchor="left",
                       font=dict(size=18, color="#8A6A00"))
    fig.add_annotation(x=2.0, y=0.62, text="start", showarrow=False, font=dict(size=18, color="#555555"))
    rd.axes(fig)
    fig.update_layout(template="simple_white", font=FONT, width=760, height=1000, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


ts = [round(0.2 * i, 1) for i in range(int(T_HIT / 0.2) + 1)] + [T_HIT]
figs = [frame(t) for t in ts]
holds = [5] + [1] * (len(ts) - 2) + [16]
make_gif(figs, here / "room3a", fps=6, holds=holds, keys=[0, ts.index(4.0), ts.index(8.0), len(ts) - 1], cols=2,
         width=560)
