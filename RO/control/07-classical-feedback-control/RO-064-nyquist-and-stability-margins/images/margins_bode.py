"""The heading loop's margins on its Bode plot. Solid: L(s) = (0.8 s + 4) e^{-0.1 s}/s^2 (0.1 s delay); dashed: no
delay. Gain crosses 0 dB at 2.08 rad/s for both (a delay does not change the gain). Phase there: -157.4 degrees with no
delay (phase margin 22.6), -169.3 degrees with 0.1 s (10.7). With 0.1 s the phase reaches -180 degrees at 11.66 rad/s,
where the gain is -22.5 dB: gain margin 22.5 dB (13.4). Without delay the phase never reaches -180: no gain margin limit.
Run: python margins_bode.py -> margins_bode.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, PURPLE, RED
from loopkit import L_head, db, margins

here = Path(__file__).parent
w = np.logspace(-1, 2, 2000)
m0, m1 = margins(L_head), margins(lambda s: L_head(s, 0.1))
assert abs(m0["pm"] - 22.6) < 0.05 and np.isinf(m0["gm"]) and abs(m1["pm"] - 10.7) < 0.05
assert abs(20 * np.log10(m1["gm"]) - 22.5) < 0.05 and abs(m1["wpc"] - 11.66) < 0.005 and abs(m1["wgc"] - 2.08) < 5e-3
ph0 = np.degrees(np.unwrap(np.angle(L_head(1j * w))))
ph1 = np.degrees(np.unwrap(np.angle(L_head(1j * w, 0.1))))
assert abs(np.interp(np.log(m0["wgc"]), np.log(w), ph0) + 157.4) < 0.05

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08)
fig.add_trace(go.Scatter(x=w, y=db(L_head(1j * w)), line=dict(color=BLUE, width=4)), 1, 1)
fig.add_trace(go.Scatter(x=w, y=ph0, line=dict(color=BLUE, width=3, dash="dash")), 2, 1)
fig.add_trace(go.Scatter(x=w, y=ph1, line=dict(color=BLUE, width=4)), 2, 1)
for r, y in [(1, 0), (2, -180)]:
    fig.add_trace(go.Scatter(x=[w[0], w[-1]], y=[y, y], line=dict(color=GREY, width=1.5)), r, 1)
wg, wp = m1["wgc"], m1["wpc"]
fig.add_trace(go.Scatter(x=[wg * 0.92] * 2, y=[-157.4, -180], mode="lines", line=dict(color=PURPLE, width=2,
                                                                                        dash="dot")), 2, 1)
fig.add_trace(go.Scatter(x=[wg, wg], y=[-169.3, -180], mode="lines", line=dict(color=PURPLE, width=6)), 2, 1)
fig.add_trace(go.Scatter(x=[wg, wg * 0.92], y=[-169.3, -157.4], mode="markers", marker=dict(size=10, color=PURPLE)),
              2, 1)
fig.add_trace(go.Scatter(x=[wp, wp], y=[-22.5, 0], mode="lines", line=dict(color=GREEN, width=6)), 1, 1)
fig.add_trace(go.Scatter(x=[wp], y=[-180], mode="markers", marker=dict(size=12, color=GREEN)), 2, 1)
fig.add_trace(go.Scatter(x=[wg], y=[0], mode="markers", marker=dict(size=12, color=PURPLE)), 1, 1)
fig.add_annotation(x=np.log10(wp), y=-11, text="gain margin 22.5 dB<br>(× 13.4) at 11.66 rad/s", showarrow=False,
                   xanchor="left", xshift=10, font=dict(color=GREEN, size=18), row=1, col=1)
fig.add_annotation(x=np.log10(wg), y=-196, text="10.7° with 0.1 s delay", showarrow=False,
                   xanchor="left", xshift=8, font=dict(color=PURPLE, size=18), row=2, col=1)
fig.add_annotation(x=np.log10(wg), y=-140, text="phase margin 22.6° without delay", showarrow=False, xanchor="right", xshift=-14,
                   font=dict(color=PURPLE, size=18), row=2, col=1)
fig.add_annotation(x=np.log10(wg), y=0, text="0 dB at 2.08 rad/s", showarrow=False, xanchor="left", xshift=10,
                   yshift=14, font=dict(color=PURPLE, size=18), row=1, col=1)
fig.add_annotation(x=-0.98, y=-232, text="solid: 0.1 s delay   dashed: no delay (never reaches −180°)",
                   showarrow=False, xanchor="left", font=dict(color=BLUE, size=17), row=2, col=1)
fig.update_xaxes(type="log", range=[-1, 2], row=1, col=1)
fig.update_xaxes(type="log", range=[-1, 2], title="frequency ω (rad/s)", row=2, col=1)
fig.update_yaxes(title="gain of L (dB)", range=[-60, 60], row=1, col=1)
fig.update_yaxes(title="phase of L (°)", range=[-240, -120], dtick=30, row=2, col=1)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=900, showlegend=False,
                  margin=dict(l=100, r=30, t=40, b=80))
fig.write_image(here / "margins_bode.png")
