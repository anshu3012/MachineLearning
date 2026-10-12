"""Bandwidth: the gain curves of the heading loop with our first-try gains (Kp 0.4, Kd 0.08, zeta = 0.2, blue) and
with RO-060's tuned gains (Kp 0.2, Kd 0.283, zeta = 1, grey), and the line 3.01 dB below the zero-frequency gain of
0 dB. Each curve crosses it at its bandwidth: 3.02 rad/s for the first try, 0.91 rad/s for the tuned loop.
Run: python bandwidth.py -> bandwidth.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED
from loopkit import G_yr, KP, bandwidth, db

here = Path(__file__).parent
wl = np.logspace(-1, np.log10(20), 800)
g02 = lambda s: G_yr(s)
g1 = lambda s: G_yr(s, 0.2, 0.283)
b02, b1 = bandwidth(g02), bandwidth(g1)
assert abs(b02 - 3.02) < 5e-3 and abs(b1 - 0.91) < 5e-3 and abs(db(1 / np.sqrt(2)) + 3.01) < 5e-3
fig = go.Figure()
fig.add_trace(go.Scatter(x=wl, y=db(g1(1j * wl)), mode="lines", line=dict(color=GREY, width=4), name="RO-060's tuned gains: Kp 0.2, Kd 0.283 (ζ = 1)"))
fig.add_trace(go.Scatter(x=wl, y=db(g02(1j * wl)), mode="lines", line=dict(color=BLUE, width=4), name="first try: Kp 0.4, Kd 0.08 (ζ = 0.2)"))
fig.add_trace(go.Scatter(x=[0.1, 20], y=[-3.01, -3.01], mode="lines", line=dict(color=RED, width=2, dash="dash"),
                         name="−3.01 dB: 0.707 of the zero-frequency gain"))
fig.add_trace(go.Scatter(x=[b1, b02], y=[-3.01, -3.01], mode="markers", marker=dict(color=RED, size=14), showlegend=False))
fig.add_annotation(x=np.log10(b02), y=-3.01, text="bandwidth 3.02 rad/s", ax=130, ay=-45, arrowcolor=BLUE,
                   font=dict(color=BLUE, size=19))
fig.add_annotation(x=np.log10(b1), y=-3.01, text="bandwidth 0.91 rad/s", ax=-90, ay=60, arrowcolor=GREY,
                   font=dict(color=GREY, size=19))
fig.update_xaxes(type="log", range=[-1, np.log10(20)], title="weave rate ω (rad/s), log scale")
fig.update_yaxes(title="gain (dB)", range=[-42, 12], dtick=10)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=700,
                  legend=dict(x=0.01, y=0.02, yanchor="bottom", font=dict(size=18)),
                  margin=dict(l=90, r=30, t=60, b=70))
fig.write_image(here / "bandwidth.png", scale=1)
