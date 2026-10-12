"""Docking: motion control against force control. Both robots creep at 0.05 m/s towards a rigid dock 0.1 m ahead and
touch it at t = 2 s; at t = 32 s the plan says back away. One frame per 0.5 s. Top: the two robots (body 0.3 m long)
and the dock, with the force on the dock. Bottom: that force over time. Motion control (feedforward plus PI with
clamping) keeps a speed error it can never remove, so it pushes harder and harder until the drive's 4 N limit at
t = 7.8 s, and leaves the dock only 3.66 s after the back-away command. Force control sets the drive force to the
wanted 2 N at contact and backs away at once. Run: python dock_anim.py -> dock_anim.gif, dock_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif
from robotctl import DT, dock_run

here = Path(__file__).parent
T = 40
runs = [(dock_run(T, "clamp"), RED, "motion control", 1.0), (dock_run(T, "force"), GREEN, "force control", 0.0)]
t = runs[0][0]["t"]
mo, fo = runs[0][0], runs[1][0]
assert abs(t[np.argmax(mo["f"] > 0)] - 1.99) < 1e-9 and abs(t[np.argmax(mo["f"] >= 4 - 1e-9)] - 7.80) < 1e-6
assert abs(fo["f"][2000] - 2.0) < 1e-9
leave = lambda s: t[np.where((t >= 32) & (s["x"] < 0.1 - 1e-6))[0][0]] - 32
assert abs(leave(mo) - 3.66) < 1e-6 and leave(fo) < 0.02


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.42, 0.58], vertical_spacing=0.12)
    for s, col, name, y0 in runs:
        fig.add_shape(type="rect", x0=0.1, x1=0.16, y0=y0 + 0.05, y1=y0 + 0.85, line=dict(color=GREY, width=2),
                      fillcolor=GREY, opacity=0.5, row=1, col=1)
        x = s["x"][k]
        fig.add_trace(go.Scatter(x=[x - 0.3, x, x, x - 0.3, x - 0.3], y=[y0 + 0.2, y0 + 0.2, y0 + 0.7, y0 + 0.7, y0 + 0.2],
                                 mode="lines", fill="toself", fillcolor="rgba(255,255,255,0)", line=dict(color=col, width=4),
                                 showlegend=False), row=1, col=1)
        fig.add_annotation(x=-0.47, y=y0 + 0.45, xref="x", yref="y", text=name, showarrow=False, xanchor="left",
                           font=dict(size=19, color=col))
        if s["f"][k] > 0:
            fig.add_annotation(x=0.17, y=y0 + 0.45, xref="x", yref="y", text=f"{s['f'][k]:.1f} N", showarrow=False,
                               xanchor="left", font=dict(size=20, color=col))
        fig.add_trace(go.Scatter(x=t[:k + 1], y=s["f"][:k + 1], mode="lines", line=dict(color=col, width=4),
                                 name=name), row=2, col=1)
    fig.add_annotation(x=0.13, y=2.05, xref="x", yref="y", text="dock", showarrow=False, font=dict(size=18, color=GREY))
    fig.add_vline(x=32, line=dict(color=GREY, width=2, dash="dash"), row=2, col=1)
    fig.add_annotation(x=31.6, y=4.6, xref="x2", yref="y2", text="plan: back away", showarrow=False, xanchor="right",
                       font=dict(size=18, color=GREY))
    fig.add_annotation(x=0.02, y=1.05, xref="paper", yref="paper", text=f"t = {t[k]:.1f} s", showarrow=False,
                       font=dict(size=21), xanchor="left")
    fig.update_xaxes(range=[-0.5, 0.3], visible=False, row=1, col=1)
    fig.update_yaxes(range=[-0.05, 2.25], visible=False, row=1, col=1)
    fig.update_xaxes(range=[0, T], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[-0.2, 5], title="force on the dock (N)", row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=780, margin=dict(l=100, r=30, t=60, b=70),
                      legend=dict(x=0.99, xanchor="right", y=0.36, yanchor="top", bgcolor="rgba(255,255,255,0)", font=dict(size=18)))
    return fig


ks = list(range(0, len(t), 50))
figs = [frame(k) for k in ks]
make_gif(figs, here / "dock_anim", fps=6, holds=[6] + [1] * (len(ks) - 2) + [24],
         keys=[ks.index(1000), ks.index(3500), len(ks) - 1], cols=1, width=850)
