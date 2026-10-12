"""The same speed-up on carpet: the real drag is 3 N s/m, the feedforward still uses the model's 2 N s/m.
One frame per 0.2 s. Top: speed; feedforward alone settles at 0.336 m/s (formula 2 x 0.5 / 3 = 0.333), feedforward plus
feedback stays within 0.015 m/s of the plan. Bottom: distance behind the plan; feedforward alone is 140 cm behind at
12 s and still falling back, feedforward plus feedback ends 4.98 cm behind (towards 0.5 N of extra drag / ki = 5 cm).
Run: python ff_carpet.py -> ff_carpet.gif, ff_carpet_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif
from robotctl import DT, profile, profile_acc, speed_loop

here = Path(__file__).parent
T = 12
ffo = speed_loop(T, profile, aref=profile_acc, ff=True, kp=0, ki=0, b_true=3)
both = speed_loop(T, profile, aref=profile_acc, ff=True, b_true=3)
t = ffo["t"]
gap = {k: np.cumsum(s["r"] - s["v"]) * DT * 100 for k, s in (("ffo", ffo), ("both", both))}
assert abs(ffo["v"][-1] - 0.336) < 5e-4 and abs(gap["ffo"][-1] - 139.7) < 0.05
assert abs((both["r"] - both["v"]).max() - 0.0146) < 1e-4 and abs(gap["both"][-1] - 4.98) < 0.01


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.55, 0.45], vertical_spacing=0.13)
    fig.add_trace(go.Scatter(x=t, y=ffo["r"], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                             name="plan"), row=1, col=1)
    for s, col, name, key in ((ffo, ORANGE, "feedforward alone", "ffo"), (both, BLUE, "feedforward + feedback", "both")):
        fig.add_trace(go.Scatter(x=t[:k + 1], y=s["v"][:k + 1], mode="lines", line=dict(color=col, width=4),
                                 name=name), row=1, col=1)
        fig.add_trace(go.Scatter(x=t[:k + 1], y=gap[key][:k + 1], mode="lines", line=dict(color=col, width=4),
                                 showlegend=False), row=2, col=1)
    if k == len(t) - 1:
        fig.add_annotation(x=12, y=ffo["v"][-1], xref="x", yref="y", ax=-30, ay=40, xanchor="right",
                           text="0.336 m/s", font=dict(size=19, color=ORANGE), arrowcolor=ORANGE)
        fig.add_annotation(x=12, y=gap["ffo"][-1], xref="x2", yref="y2", ax=-120, ay=0, xanchor="right",
                           text="140 cm behind", font=dict(size=19, color=ORANGE), arrowcolor=ORANGE)
        fig.add_annotation(x=12, y=gap["both"][-1], xref="x2", yref="y2", ax=-30, ay=-30, xanchor="right",
                           text="4.98 cm behind", font=dict(size=19, color=BLUE), arrowcolor=BLUE)
    fig.add_annotation(x=0.02, y=1.04, xref="paper", yref="paper", text=f"on carpet, t = {t[k]:.1f} s",
                       showarrow=False, font=dict(size=21), xanchor="left")
    fig.update_xaxes(range=[0, T], row=1, col=1)
    fig.update_xaxes(range=[0, T], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[0, 0.62], title="speed (m/s)", row=1, col=1)
    fig.update_yaxes(range=[-5, 150], title="behind plan (cm)", row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=780, margin=dict(l=100, r=30, t=60, b=70),
                      legend=dict(x=0.98, xanchor="right", y=0.73, yanchor="top", font=dict(size=19)))
    return fig


ks = list(range(0, len(t), 20))
figs = [frame(k) for k in ks]
make_gif(figs, here / "ff_carpet", fps=8, holds=[6] + [1] * (len(ks) - 2) + [24],
         keys=[ks.index(200), len(ks) - 1], cols=1, width=850)
