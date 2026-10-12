"""The measured speed arrives late: the controller averages the last 20 wheel speeds (0.2 s at 100 Hz). The robot
speeds up at 0.25 m/s^2; each frame slides the 0.2 s window one step on and plots its average at the current time.
The average of a straight-line rise is the speed at the window's middle, 0.095 s ago: 0.024 m/s behind.
Run: python avg_anim.py -> avg_anim.gif, avg_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif
from tunekit import DT, NW

here = Path(__file__).parent
A = 0.25
t = np.arange(0, 1.0001, DT)
v = A * t
avg = np.array([np.mean(np.maximum(A * (tk - DT * np.arange(NW)), 0)) for tk in t])   # samples t, ..., t - 0.19; 0 before the start
lag = (NW - 1) / 2 * DT
assert abs(lag - 0.095) < 1e-12 and np.allclose((v - avg)[NW:], A * lag) and abs(A * lag - 0.024) < 5e-4


def frame(tk, final=False):
    k = int(round(tk / DT))
    fig = go.Figure()
    fig.add_vrect(x0=tk - (NW - 1) * DT, x1=tk, fillcolor=ORANGE, opacity=0.15, line_width=0)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=v[:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                             name="true speed"))
    w = slice(k - NW + 1, k + 1)
    fig.add_trace(go.Scatter(x=t[w], y=v[w], mode="markers", marker=dict(color=BLUE, size=7),
                             name="the 20 samples in the window"))
    fig.add_trace(go.Scatter(x=t[:k + 1], y=avg[:k + 1], mode="lines", line=dict(color=ORANGE, width=4),
                             name="measured speed: their average"))
    fig.add_trace(go.Scatter(x=[tk], y=[avg[k]], mode="markers", marker=dict(color=ORANGE, size=16),
                             showlegend=False))
    fig.add_trace(go.Scatter(x=[tk - lag, tk], y=[avg[k], avg[k]], mode="lines",
                             line=dict(color=GREY, width=3, dash="dot"), showlegend=False))
    fig.add_annotation(x=tk - (NW - 1) * DT / 2, y=v[k] + 0.03, text="window: 0.2 s", showarrow=False,
                       font=dict(size=19, color=ORANGE))
    txt = (f"t = {tk:.2f} s: measured {avg[k]:.3f} m/s, true {v[k]:.3f} m/s" if not final else
           "measured = true speed of 0.095 s ago, 0.024 m/s behind")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=620,
                      margin=dict(l=100, r=30, t=150, b=80), title=dict(text=txt, x=0.5, y=0.96),
                      legend=dict(x=0.4, y=1.0, xanchor="left", yanchor="top", font=dict(size=18)),
                      xaxis=dict(title="time t (s)", range=[0, 1.02]),
                      yaxis=dict(title="speed (m/s)", range=[0, 0.3]))
    return fig


times = [round(x, 2) for x in np.arange(0.3, 1.0001, 0.05)]
figs = [frame(x) for x in times] + [frame(1.0, final=True)]
make_gif(figs, here / "avg_anim", fps=4, holds=[4] + [2] * (len(times) - 1) + [14], keys=[0, len(figs) - 1],
         cols=1, width=850)
