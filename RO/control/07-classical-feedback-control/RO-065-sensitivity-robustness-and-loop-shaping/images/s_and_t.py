"""Sensitivity S and complementary sensitivity T of the PD heading loop, L(s) = (0.8 s + 4)/s^2, as gain curves in
decibels against frequency. S is below 0 dB (disturbances shrunk) up to 1.47 rad/s, peaks at Ms = 2.55 (8.1 dB) at
2.085 rad/s and tends to 0 dB (unchanged) at high frequency. T is about 0 dB (noise passed) at low frequency, peaks at
Mt = 2.73 and falls at high frequency. Run: python s_and_t.py -> s_and_t.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy.optimize import brentq
from gifkit import BLUE, FONT, GREEN, GREY, PURPLE, RED
from loopkit import L_head, db, peak

here = Path(__file__).parent
w = np.logspace(-1, 2, 2000)
L = L_head(1j * w)
S, T = 1 / (1 + L), L / (1 + L)
assert np.allclose(S + T, 1)
wsc = brentq(lambda x: abs(1 + L_head(1j * x)) - 1, 0.1, 2)
wms, Ms = peak(lambda s: 1 / (1 + L_head(s)), 0.1, 100)
wmt, Mt = peak(lambda s: L_head(s) / (1 + L_head(s)), 0.1, 100)
assert abs(wsc - 1.474) < 1e-3 and abs(Ms - 2.55) < 5e-3 and abs(Mt - 2.73) < 5e-3

fig = go.Figure()
fig.add_vrect(x0=0.1, x1=wsc, fillcolor=GREEN, opacity=0.10, line_width=0)
fig.add_vrect(x0=wsc, x1=100, fillcolor=RED, opacity=0.06, line_width=0)
fig.add_hline(y=0, line=dict(color=GREY, width=2, dash="dash"))
fig.add_trace(go.Scatter(x=w, y=db(S), line=dict(color=BLUE, width=5), name="|S|: disturbance d → heading"))
fig.add_trace(go.Scatter(x=w, y=db(T), line=dict(color=PURPLE, width=5, dash="dash"), name="|T|: noise n → heading"))
fig.add_annotation(x=np.log10(wms), y=db(Ms), text="Ms = 2.55 (8.1 dB)<br>at 2.085 rad/s", ax=110, ay=-30,
                   font=dict(size=19, color=BLUE), arrowcolor=BLUE)
fig.add_annotation(x=np.log10(wmt), y=db(Mt), text="Mt = 2.73", ax=-110, ay=5, font=dict(size=19, color=PURPLE),
                   arrowcolor=PURPLE)
fig.add_annotation(x=np.log10(0.3), y=-12, text="disturbances<br>shrunk: |S| < 1", showarrow=False,
                   font=dict(size=19, color=GREEN))
fig.add_annotation(x=np.log10(30), y=-12, text="disturbances passed<br>or grown: |S| ≥ 1", showarrow=False,
                   font=dict(size=19, color=RED))
fig.add_annotation(x=np.log10(wsc), y=-50, text="1.47 rad/s", showarrow=False, yanchor="bottom",
                   font=dict(size=17, color=GREY))
fig.update_xaxes(type="log", title_text="frequency ω (rad/s)", range=[-1, 2])
fig.update_yaxes(title_text="gain (dB)", range=[-50, 15])
fig.update_layout(template="simple_white", font=FONT, width=1000, height=650, margin=dict(l=90, r=30, t=110, b=70),
                  legend=dict(x=0.0, y=1.01, yanchor="bottom", orientation="h", font=dict(size=18)),
                  title=dict(x=0.5, y=0.97, text="PD heading loop: S + T = 1 (as complex numbers) at every ω"))
fig.write_image(here / "s_and_t.png", scale=1)
