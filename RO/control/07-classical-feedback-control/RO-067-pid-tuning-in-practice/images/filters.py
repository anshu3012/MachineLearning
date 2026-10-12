"""Two ways to keep the frame's 10 Hz shaking out of the D term, drawn as frequency responses (gain and phase against
frequency, both axes as in a Bode plot). Orange: a first-order low-pass at 1 Hz. Blue: a notch at 10 Hz, 5 Hz wide.
Both are the 100 Hz filters of the notebook. The dotted line marks the heading loop's gain crossover (2.87 rad/s, 0.46
Hz, with RO-060's heading PID), the dashed line the 10 Hz shaking. The low-pass lets 0.1 of the shaking through and lags
24 degrees at the crossover; the notch lets none through and lags 1.4 degrees. The notch's gain is exactly 0 at 10 Hz; the log axis
cannot show 0, so the curve is drawn down to its bottom edge, 0.001. Frequencies stop at 20 Hz.
Run: python filters.py -> filters.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal
from gifkit import BLUE, FONT, GREY, ORANGE
from tunekit import DT, F_VIB, heading_loop_tf, lowpass, margins, notch

here = Path(__file__).parent
f = np.unique(np.r_[np.logspace(-1, np.log10(20), 600), 10.0])
w = 2 * np.pi * f
FILT = {"low-pass at 1 Hz": (lowpass(1.0), ORANGE), "notch at 10 Hz": (notch(), BLUE)}
wg = np.logspace(-2, np.log10(np.pi / DT * 0.999), 200000)
m0 = margins(heading_loop_tf(wg), wg)
fc = m0["wgc"] / (2 * np.pi)
resp = {}
for name, ((b, a), _) in FILT.items():
    _, h = signal.freqz(b, a, worN=np.r_[w, 2 * np.pi * F_VIB, m0["wgc"]], fs=2 * np.pi / DT)
    resp[name] = (h[:-2], abs(h[-2]), np.degrees(np.angle(h[-1])))
assert abs(m0["wgc"] - 2.87) < 0.01 and abs(fc - 0.456) < 0.001
assert abs(resp["low-pass at 1 Hz"][1] - 0.10) < 0.005 and resp["notch at 10 Hz"][1] < 1e-6
assert abs(resp["low-pass at 1 Hz"][2] + 24.4) < 0.05 and abs(resp["notch at 10 Hz"][2] + 1.4) < 0.05

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08)
for name, ((b, a), col) in FILT.items():
    h = resp[name][0]
    fig.add_trace(go.Scatter(x=f, y=np.maximum(abs(h), 1e-3), mode="lines", line=dict(color=col, width=4), name=name), row=1, col=1)
    fig.add_trace(go.Scatter(x=f, y=np.degrees(np.angle(h)), mode="lines", line=dict(color=col, width=4),
                             showlegend=False), row=2, col=1)
for row in (1, 2):
    fig.add_vline(x=fc, line=dict(color=GREY, width=2, dash="dot"), row=row, col=1)
    fig.add_vline(x=F_VIB, line=dict(color="black", width=2, dash="dash"), row=row, col=1)
fig.add_annotation(x=np.log10(fc), y=np.log10(2.0), text="loop crossover 0.46 Hz", showarrow=False, xanchor="right",
                   font=dict(size=18, color=GREY), row=1, col=1)
fig.add_annotation(x=np.log10(F_VIB), y=np.log10(2.0), text="shaking 10 Hz", showarrow=False, xanchor="left",
                   font=dict(size=18), row=1, col=1)
fig.add_annotation(x=np.log10(fc), y=-24.4, text="−24°", showarrow=True, ax=-50, ay=30, font=dict(size=18, color=ORANGE),
                   row=2, col=1)
fig.add_annotation(x=np.log10(fc), y=-1.4, text="−1.4°", showarrow=True, ax=-50, ay=-25, font=dict(size=18, color=BLUE),
                   row=2, col=1)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=820, margin=dict(l=120, r=80, t=90, b=80),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.02, yanchor="bottom", font=dict(size=19)))
fig.update_yaxes(type="log", title_text="gain (output / input)", range=[-3, 0.45], row=1, col=1)
fig.update_yaxes(title_text="phase (degrees)", range=[-95, 95], dtick=45, row=2, col=1)
fig.update_xaxes(type="log", row=1, col=1)
fig.update_xaxes(type="log", title_text="frequency (Hz)", row=2, col=1)
fig.write_image(here / "filters.png")
