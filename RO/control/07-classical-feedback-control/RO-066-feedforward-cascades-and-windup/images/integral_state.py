"""State feedback against a 1 degree ramp, with and without the integral state. The robot cruises at 0.5 m/s and
meets the ramp at t = 0 (gravity pulls back with 1.37 N). One frame per 0.2 s. Top: speed; state feedback
u = -20 v + 22 r settles at 0.438 m/s; with the integral state it comes back to 0.5 m/s (within 0.005 m/s after
5.32 s). Bottom: the integral term climbs until it equals the ramp's pull, 1.37 N, and then stops, because the error
is zero. Run: python integral_state.py -> integral_state.gif, integral_state_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif
from robotctl import RAMP_1DEG, speed_loop

here = Path(__file__).parent
T = 12
ramp = lambda t: -RAMP_1DEG
sf = speed_loop(T, lambda t: 0.5, v0=0.5, i0=0.0, sf=(20, 22), ki=0, dist=ramp)
si = speed_loop(T, lambda t: 0.5, v0=0.5, i0=0.0, sf=(20, 22), dist=ramp)
t = sf["t"]
assert abs(RAMP_1DEG - 1.37) < 5e-3 and abs(sf["v"][-1] - 0.4377) < 1e-4
assert abs(si["v"][-1] - 0.5) < 2e-4 and abs(si["i"][-1] - 1.37) < 3e-3 and abs(si["v"].min() - 0.4509) < 1e-4


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.55, 0.45], vertical_spacing=0.13)
    fig.add_trace(go.Scatter(x=[0, T], y=[0.5, 0.5], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                             name="wanted, 0.5 m/s"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=sf["v"][:k + 1], mode="lines", line=dict(color=RED, width=4),
                             name="state feedback"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=si["v"][:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                             name="state feedback + integral state"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0, T], y=[RAMP_1DEG] * 2, mode="lines", line=dict(color=GREY, width=3, dash="dot"),
                             showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=si["i"][:k + 1], mode="lines", line=dict(color=PURPLE, width=4),
                             showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=[t[k]], y=[si["i"][k]], mode="markers", marker=dict(color=PURPLE, size=13),
                             showlegend=False), row=2, col=1)
    fig.add_annotation(x=0.3, y=1.52, xref="x2", yref="y2", text="ramp's pull, 1.37 N", showarrow=False,
                       font=dict(size=19, color=GREY), xanchor="left")
    fig.add_annotation(x=T, y=0.25, xref="x2", yref="y2", xanchor="right",
                       text=f"integral term: {si['i'][k]:.2f} N", showarrow=False, font=dict(size=20, color=PURPLE))
    if k == len(t) - 1:
        fig.add_annotation(x=T, y=sf["v"][-1], xref="x", yref="y", ax=-30, ay=30, xanchor="right",
                           text="0.438 m/s", font=dict(size=19, color=RED), arrowcolor=RED)
    fig.add_annotation(x=0.02, y=1.04, xref="paper", yref="paper", text=f"on a 1° ramp, t = {t[k]:.1f} s",
                       showarrow=False, font=dict(size=21), xanchor="left")
    fig.update_xaxes(range=[0, T], row=1, col=1)
    fig.update_xaxes(range=[0, T], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[0.42, 0.52], title="speed (m/s)", row=1, col=1)
    fig.update_yaxes(range=[0, 1.7], title="force (N)", row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=780, margin=dict(l=100, r=30, t=60, b=70),
                      legend=dict(x=0.98, xanchor="right", y=0.80, yanchor="top", font=dict(size=19)))
    return fig


ks = list(range(0, len(t), 20))
figs = [frame(k) for k in ks]
make_gif(figs, here / "integral_state", fps=8, holds=[6] + [1] * (len(ks) - 2) + [24],
         keys=[ks.index(100), len(ks) - 1], cols=1, width=850)
