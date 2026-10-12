"""A trajectory: the local planner's band in the cycle the person is first seen (t = 2.4 s), after optimising.
Left: its poses, each a dot with a short line for the heading, labelled with the time at which the robot should be
there, counted from now; the person and the robot. Right: its speed between neighbouring poses (distance over time
step), against the time from now, with the 0.6 m/s wheel limit (dashed). Run -> trajectory.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, GREY, ORANGE
from plotly.subplots import make_subplots

here = Path(__file__).parent
c = bk.results()["loop"][24]
P, DT = c["P"], c["DT"]
assert round(c["t"], 1) == 2.4 and len(P) == 10
tt = np.concatenate([[0], np.cumsum(DT)])
v, w, acc, _, _ = bk.band_terms(P, DT, c["v"], c["final"])
fig = make_subplots(rows=1, cols=2, column_widths=[0.46, 0.54], horizontal_spacing=0.1,
                    subplot_titles=["where and when: the band's poses", "how fast: speed v (m/s)"])
rd.room(fig, rc=(1, 1))
rd.person(fig, bk.PERSON, bk.PERSON_R, rc=(1, 1))
rd.band(fig, P, ORANGE, rc=(1, 1))
rd.robot(fig, *c["x"], BLUE, rc=(1, 1), fill="rgba(255,255,255,0)")
for k, (x, y, th) in enumerate(P):
    if k in (2, 4, 6):
        fig.add_annotation(x=x - 0.07, y=y, text=f"{tt[k]:.1f} s", showarrow=False, xanchor="right",
                           font=dict(size=18, color="#444444"), row=1, col=1)
    elif k == len(P) - 1:
        fig.add_annotation(x=x, y=y + 0.08, text=f"{tt[k]:.1f} s", showarrow=False, yanchor="bottom",
                           font=dict(size=18, color="#444444"), row=1, col=1)
    elif k == 0:
        fig.add_annotation(x=x, y=y - 0.3, text="0 s: the robot now", showarrow=False, yanchor="top",
                           font=dict(size=18, color=BLUE), row=1, col=1)
rd.zoom(fig, (1.55, 3.45), (1.35, 3.75), rc=(1, 1))
fig.add_trace(go.Scatter(x=np.repeat(tt, 2)[1:-1], y=np.repeat(v, 2), mode="lines", line=dict(color=ORANGE, width=4)),
              row=1, col=2)
fig.add_trace(go.Scatter(x=[0, tt[-1]], y=[0.6, 0.6], mode="lines", line=dict(color=GREY, dash="dash", width=2)),
              row=1, col=2)
fig.add_annotation(x=tt[-1] / 2, y=0.64, text="limit 0.6 m/s (each wheel)", showarrow=False, font=dict(size=17, color=GREY),
                   row=1, col=2)
fig.update_xaxes(title="time from now (s)", range=[0, tt[-1] + 0.1], row=1, col=2)
fig.update_yaxes(range=[0, 0.72], row=1, col=2)
fig.update_annotations(selector=dict(text="where and when: the band's poses"), font_size=22)
fig.update_annotations(selector=dict(text="how fast: speed v (m/s)"), font_size=22)
fig.update_layout(template="simple_white", font=FONT, width=1300, height=760, showlegend=False,
                  margin=dict(l=10, r=20, t=50, b=60))
fig.write_image(here / "trajectory.png", scale=2)
print("poses", len(P), "duration", round(tt[-1], 2), "speeds", np.round(v, 3))
