"""The loop shape we want, drawn over the PD heading loop's |L| (blue): high gain at low frequency, where drags and slow
disturbances must shrink; a gentle crossing of 0 dB, near -20 dB per decade, for phase margin; low and falling gain at
high frequency, where sensor noise lives. The PD loop crosses 0 dB at 2.08 rad/s falling at 37 dB per decade (phase
margin 22.6 degrees), and above its zero at 5 rad/s falls only 20 dB per decade, because the derivative keeps raising
the controller's gain. Run: python loop_shape.py -> loop_shape.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, PURPLE, RED
from loopkit import L_head, db, margins

here = Path(__file__).parent
m = margins(L_head)
wg = m["wgc"]
h = 1e-4
slope = 20 * (np.log10(abs(L_head(1j * wg * (1 + h)))) - np.log10(abs(L_head(1j * wg * (1 - h))))) / (
    np.log10(1 + h) - np.log10(1 - h))
assert abs(wg - 2.08) < 5e-3 and abs(slope + 37.0) < 0.5
w = np.logspace(-2, np.log10(300), 1500)

fig = go.Figure()
fig.add_vrect(x0=0.01, x1=0.25, fillcolor=GREEN, opacity=0.10, line_width=0)
fig.add_vrect(x0=1.0, x1=6.0, fillcolor=PURPLE, opacity=0.10, line_width=0)
fig.add_vrect(x0=25, x1=300, fillcolor=RED, opacity=0.08, line_width=0)
fig.add_hline(y=0, line=dict(color=GREY, width=2, dash="dash"))
fig.add_trace(go.Scatter(x=w, y=db(L_head(1j * w)), line=dict(color=BLUE, width=5), name="PD heading loop |L|"))
ww = np.array([wg / 3, wg * 3])
fig.add_trace(go.Scatter(x=ww, y=-20 * np.log10(ww / wg), mode="lines", line=dict(color=PURPLE, width=4, dash="dot"),
                         name="−20 dB per decade through the crossover"))
fig.add_annotation(x=np.log10(0.05), y=-30, text="low frequencies:<br>gain high,<br>disturbances shrink",
                   showarrow=False, font=dict(size=18, color=GREEN))
fig.add_annotation(x=np.log10(2.45), y=60, text="crossover:<br>cross 0 dB gently,<br>phase margin",
                   showarrow=False, font=dict(size=18, color=PURPLE))
fig.add_annotation(x=np.log10(87), y=40, text="high frequencies:<br>gain low and falling,<br>noise not passed on",
                   showarrow=False, font=dict(size=18, color=RED))
fig.add_annotation(x=np.log10(wg), y=0, text="PD: crosses at 2.08 rad/s,<br>falling 37 dB per decade", ax=-150, ay=100,
                   font=dict(size=17, color=BLUE), arrowcolor=BLUE)
fig.add_annotation(x=np.log10(40), y=db(L_head(40j)), text="PD: falls only 20 dB<br>per decade up here", ax=-40, ay=-75,
                   font=dict(size=17, color=BLUE), arrowcolor=BLUE)
fig.update_xaxes(type="log", title_text="frequency ω (rad/s)", range=[-2, np.log10(300)])
fig.update_yaxes(title_text="loop gain |L| (dB)", range=[-60, 100])
fig.update_layout(template="simple_white", font=FONT, width=1000, height=700, margin=dict(l=90, r=30, t=120, b=70),
                  legend=dict(x=0.0, y=1.0, yanchor="bottom", orientation="h", font=dict(size=17)),
                  title=dict(x=0.5, y=0.97, text="the loop shape we want, and the PD loop"))
fig.write_image(here / "loop_shape.png", scale=1)
