"""Integrator windup inside the controller. Feedforward plus PI (kp = 20, ki = 10) cruising at 0.5 m/s; a person holds
the robot still from t = 2 s to t = 5 s. One frame per 0.2 s. Top: the command c the controller asks for, the force u
the drive gives (at most 4 N) and the integral term. While held, the integral climbs 5 N every second to 14.9 N, and
the command to 25.9 N; let go, the drive stays at 4 N until the integral has come back down, so the speed (bottom)
overshoots to 1.04 m/s. Run: python windup_anim.py -> windup_anim.gif, windup_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif
from robotctl import DT, speed_loop

here = Path(__file__).parent
s = speed_loop(14, lambda t: 0.5, v0=0.5, ff=True, i0=0.0, hold=(2, 5))
t, v, c, u, I = s["t"], s["v"], s["c"], s["u"], s["i"]
i5 = int(round(5 / DT))
assert abs(c[i5 - 1] - 25.90) < 0.01 and abs(I[i5 - 1] - 14.90) < 0.01 and abs(v[i5:].max() - 1.039) < 5e-4
sat_end = i5 + np.argmax(u[i5:] < 4 - 1e-9)       # the drive leaves its limit
assert abs(t[sat_end] - 7.82) < 1e-6, t[sat_end]


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.55, 0.45], vertical_spacing=0.12)
    for row in (1, 2):
        fig.add_vrect(x0=2, x1=5, fillcolor="#F58518", opacity=0.18, layer="below", line_width=0, exclude_empty_subplots=False, row=row, col=1)
    fig.add_trace(go.Scatter(x=[0, 14], y=[4, 4], mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                             name="drive's limit, 4 N"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=c[:k + 1], mode="lines", line=dict(color=RED, width=4, dash="dash"),
                             name="command c"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=u[:k + 1], mode="lines", line=dict(color=RED, width=4),
                             name="force u the drive gives"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=I[:k + 1], mode="lines", line=dict(color=PURPLE, width=4),
                             name="integral term"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0, 14], y=[0.6, 0.6], mode="lines", line=dict(color=RED, width=2, dash="dot"),
                             showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=v[:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                             name="speed"), row=2, col=1)
    fig.add_annotation(x=3.5, y=27.5, xref="x", yref="y", text="held", showarrow=False, font=dict(size=20, color="#F58518"))
    if t[k] >= 5.0 - 1e-9:
        fig.add_annotation(x=5, y=c[i5 - 1], xref="x", yref="y", ax=60, ay=0, xanchor="left",
                           text="25.9 N asked", font=dict(size=19, color=RED), arrowcolor=RED)
    if k >= sat_end:
        fig.add_annotation(x=t[sat_end], y=4, xref="x", yref="y", ax=70, ay=-80, xanchor="left",
                           text="drive leaves 4 N only now", font=dict(size=19, color=RED), arrowcolor=RED)
    if t[k] >= 8.07:
        fig.add_annotation(x=8.07, y=1.039, xref="x2", yref="y2", ax=60, ay=10, xanchor="left",
                           text="1.04 m/s", font=dict(size=19, color=BLUE), arrowcolor=BLUE)
    fig.add_annotation(x=12.9, y=0.66, xref="x2", yref="y2", text="top speed", showarrow=False,
                       font=dict(size=17, color=RED))
    fig.add_annotation(x=0.02, y=1.05, xref="paper", yref="paper", text=f"t = {t[k]:.1f} s", showarrow=False,
                       font=dict(size=21), xanchor="left")
    fig.update_xaxes(range=[0, 14], row=1, col=1)
    fig.update_xaxes(range=[0, 14], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[-3, 29], title="force (N)", row=1, col=1)
    fig.update_yaxes(range=[-0.05, 1.2], title="speed (m/s)", row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=820, margin=dict(l=100, r=30, t=60, b=70),
                      legend=dict(x=0.99, xanchor="right", y=0.99, yanchor="top", font=dict(size=18)))
    return fig


ks = list(range(0, len(t), 20))
figs = [frame(k) for k in ks]
make_gif(figs, here / "windup_anim", fps=8, holds=[6] + [1] * (len(ks) - 2) + [24],
         keys=[ks.index(500), len(ks) - 1], cols=1, width=850)
