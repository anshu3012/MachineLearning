"""Feedback alone trails the plan; feedforward plus feedback does not. The planner's speed-up: from rest at
0.25 m/s^2 to 0.5 m/s in 2 s, then cruise, on the normal floor (drag 2 N s/m). One frame per 0.2 s.
Top: speed; feedback alone (PI, kp = 20, ki = 10) is up to 0.085 m/s behind at t = 1.10 s; with the feedforward
m a + b v added it sits on the plan. Bottom: how far each robot is behind where the plan says it should be; feedback
alone ends 10 cm behind (= 1 N of drag / ki), feedforward plus feedback 0 cm.
Run: python ff_lag.py -> ff_lag.gif, ff_lag_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, RED, make_gif
from robotctl import DT, profile, profile_acc, speed_loop

here = Path(__file__).parent
T = 12
fb = speed_loop(T, profile, aref=profile_acc)
both = speed_loop(T, profile, aref=profile_acc, ff=True)
t = fb["t"]
gap = {k: np.cumsum(s["r"] - s["v"]) * DT * 100 for k, s in (("fb", fb), ("both", both))}
e = fb["r"] - fb["v"]
assert abs(e.max() - 0.0845) < 1e-4 and abs(t[e.argmax()] - 1.10) < 1e-9
assert abs(gap["fb"][-1] - 10.0) < 0.05 and np.abs(gap["both"]).max() < 1e-6
assert abs(gap["fb"].max() - 15.8) < 0.05


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.55, 0.45], vertical_spacing=0.13)
    fig.add_trace(go.Scatter(x=t, y=fb["r"], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                             name="plan"), row=1, col=1)
    for s, col, name in ((fb, RED, "feedback alone"), (both, BLUE, "feedforward + feedback")):
        fig.add_trace(go.Scatter(x=t[:k + 1], y=s["v"][:k + 1], mode="lines", line=dict(color=col, width=4),
                                 name=name), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=gap["fb"][:k + 1], mode="lines", line=dict(color=RED, width=4),
                             showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=gap["both"][:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                             showlegend=False), row=2, col=1)
    if k >= 110:
        fig.add_annotation(x=1.10, y=fb["v"][110], xref="x", yref="y", ax=70, ay=40,
                           text="0.085 m/s behind", font=dict(size=19, color=RED), arrowcolor=RED)
    if k == len(t) - 1:
        fig.add_annotation(x=12, y=gap["fb"][-1], xref="x2", yref="y2", ax=-20, ay=-38, xanchor="right",
                           text="10 cm behind", font=dict(size=19, color=RED), arrowcolor=RED)
        fig.add_annotation(x=12, y=0, xref="x2", yref="y2", ax=-20, ay=-30, xanchor="right",
                           text="0 cm", font=dict(size=19, color=BLUE), arrowcolor=BLUE)
    fig.add_annotation(x=0.02, y=1.04, xref="paper", yref="paper", text=f"t = {t[k]:.1f} s", showarrow=False,
                       font=dict(size=21), xanchor="left")
    fig.update_xaxes(range=[0, T], row=1, col=1)
    fig.update_xaxes(range=[0, T], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[0, 0.62], title="speed (m/s)", row=1, col=1)
    fig.update_yaxes(range=[-2, 18], title="behind plan (cm)", row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=780, margin=dict(l=100, r=30, t=60, b=70),
                      legend=dict(x=0.98, xanchor="right", y=0.86, yanchor="top", font=dict(size=19)))
    return fig


ks = list(range(0, len(t), 20))
figs = [frame(k) for k in ks]
make_gif(figs, here / "ff_lag", fps=8, holds=[6] + [1] * (len(ks) - 2) + [24],
         keys=[ks.index(100), ks.index(200), len(ks) - 1], cols=1, width=850)
