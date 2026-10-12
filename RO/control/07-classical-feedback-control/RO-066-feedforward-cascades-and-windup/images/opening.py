"""The opening problem: the robot cruises at 0.5 m/s under the PI speed loop of RO-060 (kp = 20, ki = 10), a person holds it
still from t = 2 s to t = 5 s, then lets go. One frame per 0.2 s. Top: the robot in the corridor. Bottom: its speed
against the plan (0.5 m/s) and the top speed (0.6 m/s). The PI asks for 25.9 N at the release, the drive gives 4 N;
let go, the robot reaches 1.04 m/s and stays above the top speed for 5.1 s.
Run: python opening.py -> opening.gif, opening_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from robotctl import DT, speed_loop

here = Path(__file__).parent
s = speed_loop(14, lambda t: 0.5, v0=0.5, hold=(2, 5))
t, v, c = s["t"], s["v"], s["c"]
x = 0.5 + np.r_[0, np.cumsum(v[:-1]) * DT]
i5 = int(round(5 / DT))
assert abs(c[i5 - 1] - 25.90) < 0.01 and abs(v[i5:].max() - 1.039) < 5e-4
assert abs((v > 0.6).sum() * DT - 5.09) < 0.01
peak_i = i5 + v[i5:].argmax()


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.26, 0.74], vertical_spacing=0.1)
    # corridor and robot
    fig.add_shape(type="rect", x0=0, x1=7.5, y0=0, y1=1, line=dict(color=GREY, width=2), fillcolor="white",
                  row=1, col=1)
    held = 2 <= t[k] < 5
    fig.add_shape(type="rect", x0=x[k] - 0.3, x1=x[k], y0=0.25, y1=0.75, line=dict(color=BLUE, width=3),
                  fillcolor=BLUE, opacity=0.4, row=1, col=1)
    label = "held by a person" if held else ("let go" if 5 <= t[k] < 6.5 else "")
    if held:
        fig.add_trace(go.Scatter(x=[x[k] - 0.45], y=[0.5], mode="markers", marker=dict(color=ORANGE, size=26),
                                 showlegend=False), row=1, col=1)
    fig.add_annotation(x=3.75, y=1.32, xref="x", yref="y", text=f"t = {t[k]:.1f} s   {label}", showarrow=False,
                       font=dict(size=22))
    fig.update_xaxes(range=[0, 7.5], row=1, col=1, dtick=1, ticksuffix=" m")
    fig.update_yaxes(range=[-0.1, 1.55], visible=False, row=1, col=1)
    # speed
    fig.add_vrect(x0=2, x1=5, fillcolor=ORANGE, opacity=0.18, layer="below", line_width=0, exclude_empty_subplots=False, row=2, col=1)
    fig.add_trace(go.Scatter(x=[0, 14], y=[0.5, 0.5], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                             name="plan, 0.5 m/s"), row=2, col=1)
    fig.add_trace(go.Scatter(x=[0, 14], y=[0.6, 0.6], mode="lines", line=dict(color=RED, width=3, dash="dot"),
                             name="top speed, 0.6 m/s"), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=v[:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                             name="robot's speed"), row=2, col=1)
    fig.add_trace(go.Scatter(x=[t[k]], y=[v[k]], mode="markers", marker=dict(color=BLUE, size=13), showlegend=False),
                  row=2, col=1)
    fig.add_annotation(x=3.5, y=1.12, xref="x2", yref="y2", text="held", showarrow=False,
                       font=dict(size=20, color=ORANGE))
    if t[k] >= 5.0 - 1e-9:
        fig.add_annotation(x=5, y=0.12, xref="x2", yref="y2", ax=70, ay=-10,
                           text="asks for 25.9 N,<br>drive gives 4 N", font=dict(size=19), xanchor="left",
                           arrowcolor=GREY)
    if k >= peak_i:
        fig.add_annotation(x=t[peak_i], y=v[peak_i], xref="x2", yref="y2", ax=60, ay=-30,
                           text="1.04 m/s", font=dict(size=20, color=BLUE), arrowcolor=BLUE)
    fig.update_xaxes(range=[0, 14], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[-0.05, 1.2], title="speed (m/s)", row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=760,
                      margin=dict(l=90, r=30, t=30, b=70),
                      legend=dict(x=0.5, xanchor="center", y=-0.2, orientation="h", font=dict(size=19)))
    return fig


ks = list(range(0, len(t), 20))
figs = [frame(k) for k in ks]
make_gif(figs, here / "opening", fps=8, holds=[6] + [1] * (len(ks) - 2) + [24],
         keys=[ks.index(400), ks.index(500), ks.index(820), len(ks) - 1], cols=2, width=900)
