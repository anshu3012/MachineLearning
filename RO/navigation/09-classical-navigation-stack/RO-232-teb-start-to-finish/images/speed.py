"""The robot's forward speed over the drive, sampled at every 0.1 s cycle. Blue: our Python version of TEB's algorithm;
orange: RO-058's band. Solid: the person steps in at 2.4 s; dashed: the room clear. Grey lines: TEB's speed limit
for our robot, 0.5 m/s, and the wheel limit RO-058's band used, 0.6 m/s. Dots: arrival at the door pose (within
0.02 m and 0.05 rad, stopped); diamond: our robot first within 0.02 m of the door. Run -> speed.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import tebkit as tk
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
R, B = tk.results(), bk.results()
runs = [(R["person"], BLUE, "solid", "TEB (ours), person"), (R["clear"], BLUE, "dash", "TEB (ours), clear"),
        (B["loop"], ORANGE, "solid", "RO-058 band, person"), (B["free"], ORANGE, "dash", "RO-058 band, clear")]
assert [round(r[0][-1]["t"], 1) for r in runs] == [9.8, 7.9, 8.0, 6.7]
P = R["person"]
xs = np.array([c["x"] for c in P])
i2 = int(np.argmax(np.hypot(*(xs[:, :2] - bk.GOAL[:2]).T) < 0.02))
assert round(P[i2]["t"], 1) == 7.9

fig = go.Figure()
for run, col, dash, name in runs:
    t = [c["t"] for c in run]
    v = [c["v"] for c in run]
    fig.add_trace(go.Scatter(x=t, y=v, mode="lines", line=dict(color=col, width=3, dash=dash), name=name))
    fig.add_trace(go.Scatter(x=[t[-1]], y=[v[-1]], mode="markers", marker=dict(size=13, color=col), showlegend=False))
fig.add_trace(go.Scatter(x=[P[i2]["t"]], y=[P[i2]["v"]], mode="markers", marker=dict(symbol="diamond", size=14,
                         color=BLUE), showlegend=False))
for y, txt in ((0.5, "TEB limit for our robot, 0.5 m/s"), (0.6, "wheel limit, 0.6 m/s")):
    fig.add_hline(y=y, line=dict(color=GREY, width=1.5, dash="dot"))
    fig.add_annotation(x=0.1, y=y + 0.025, text=txt, showarrow=False, xanchor="left", font=dict(size=18, color=GREY))
fig.add_vline(x=2.4, line=dict(color="#C2185B", width=1.5, dash="dot"))
fig.add_annotation(x=2.45, y=0.665, text="person steps in", showarrow=False, xanchor="left",
                   font=dict(size=18, color="#C2185B"))
fig.add_annotation(x=P[i2]["t"] + 0.15, y=P[i2]["v"] + 0.03, xanchor="left", text="within 0.02 m, 7.9 s", showarrow=False,
                   font=dict(size=17, color=BLUE))
fig.update_xaxes(title="time (s)", range=[0, 10.2])
fig.update_yaxes(title="forward speed (m/s)", range=[-0.22, 0.7])
fig.update_layout(template="simple_white", font=FONT, width=1000, height=600, margin=dict(l=90, r=20, t=20, b=80),
                  legend=dict(x=0.28, y=0.38, bgcolor="rgba(255,255,255,0.9)"))
fig.write_image(here / "speed.png")
