"""Nav2's velocity smoother, cycle by cycle at 20 Hz: accelerating and braking limited to 0.25 m/s^2 (at most
0.0125 m/s per cycle), top speed 0.6 m/s, deadband 0.02 m/s. The planner's raw commands: 0, then 0.5 m/s from 0.5 s,
0.015 m/s from 3.5 s, 0 from 7 s. One frame per 3 cycles (0.15 s). Top: raw and smoothed commands. Middle: the same
near zero; the smoother's own value settles at 0.015 m/s at 5.4 s, but it is under the deadband, so it sends 0.
Bottom: the force the speed loop (feedforward plus PI with clamping) asks for: 11 N with the raw step (0.77 s at the
4 N limit), at most 3.10 N with the smoothed commands. Run: python smoother_anim.py -> smoother_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif
from robotctl import DT, U_MAX, smoother, speed_loop

here = Path(__file__).parent
f, T = 20, 9
tt = np.arange(0, T, 1 / f)
raw = np.where(tt < 0.5, 0, np.where(tt < 3.5, 0.5, np.where(tt < 7.0, 0.015, 0.0)))
pub, inner = smoother(raw)
hold_cmd = lambda arr: (lambda t: arr[min(int(t * f + 1e-9), len(arr) - 1)])
acc = np.where(pub != 0, np.diff(np.r_[0, inner]) * f, 0.0)     # acceleration of the command actually sent
sr = speed_loop(T - 0.01, hold_cmd(raw), ff=True, i0=0.0, mode="clamp")
ss = speed_loop(T - 0.01, hold_cmd(pub), aref=hold_cmd(acc), ff=True, i0=0.0, mode="clamp")
t = sr["t"]
assert abs(tt[np.argmax(pub >= 0.5 - 1e-9)] - 2.45) < 1e-9
j = np.argmax((tt > 3.5) & (np.abs(inner - 0.015) < 1e-9))
assert abs(tt[j] - 5.4) < 1e-9 and pub[j] == 0.0
assert abs(np.abs(sr["c"]).max() - 11.0) < 1e-6 and abs((sr["u"] >= U_MAX - 1e-9).sum() * DT - 0.77) < 1e-6
assert abs((sr["u"] <= -U_MAX + 1e-9).sum() * DT - 0.48) < 1e-6
assert abs(np.abs(ss["c"]).max() - 3.10) < 5e-3 and (np.abs(ss["u"]) >= U_MAX - 1e-9).sum() == 0


def stairs(x, y):
    """Commands are held for a whole cycle: draw them as steps."""
    return np.repeat(x, 2)[1:], np.repeat(y, 2)[:-1]


def frame(i):
    tc = tt[i]
    k = int(round(tc / DT))
    fig = make_subplots(rows=3, cols=1, row_heights=[0.38, 0.27, 0.35], vertical_spacing=0.09)
    for row, rng in ((1, None), (2, None)):
        xr, yr = stairs(tt[:i + 1], raw[:i + 1])
        fig.add_trace(go.Scatter(x=xr, y=yr, mode="lines", line=dict(color=GREY, width=4),
                                 name="planner's raw command", showlegend=row == 1), row=row, col=1)
        xs, ys = stairs(tt[:i + 1], pub[:i + 1])
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=BLUE, width=4),
                                 name="smoothed command sent", showlegend=row == 1), row=row, col=1)
    xi, yi = stairs(tt[:i + 1], inner[:i + 1])
    fig.add_trace(go.Scatter(x=xi, y=yi, mode="lines", line=dict(color=PURPLE, width=4, dash="dot"),
                             name="smoother's own value (not sent)"), row=2, col=1)
    fig.add_hrect(y0=-0.02, y1=0.02, fillcolor=RED, opacity=0.15, layer="below", line_width=0, exclude_empty_subplots=False, row=2, col=1)
    fig.add_annotation(x=0.9, y=0.03, xref="x2", yref="y2", text="deadband: under 0.02 m/s, send 0", showarrow=False,
                       xanchor="left", font=dict(size=17, color=RED))
    fig.add_trace(go.Scatter(x=t[:k + 1], y=sr["c"][:k + 1], mode="lines", line=dict(color=GREY, width=4),
                             name="force asked with raw commands"), row=3, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=ss["c"][:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                             name="force asked with smoothed commands"), row=3, col=1)
    for y in (U_MAX, -U_MAX):
        fig.add_trace(go.Scatter(x=[0, T], y=[y, y], mode="lines", line=dict(color=RED, width=2, dash="dot"),
                                 showlegend=False), row=3, col=1)
    fig.add_annotation(x=8.9, y=5.2, xref="x3", yref="y3", text="drive's limit, ±4 N", showarrow=False, xanchor="right",
                       font=dict(size=17, color=RED))
    if 0.5 <= tc < 2.5:
        fig.add_annotation(x=tc, y=pub[i], xref="x", yref="y", ax=50, ay=30, xanchor="left",
                           text="+0.0125 m/s per cycle", font=dict(size=18, color=BLUE), arrowcolor=BLUE)
    fig.add_annotation(x=0.02, y=1.04, xref="paper", yref="paper", text=f"cycle {i}, t = {tc:.2f} s", showarrow=False,
                       font=dict(size=21), xanchor="left")
    for row in (1, 2, 3):
        fig.update_xaxes(range=[0, T], row=row, col=1)
    fig.update_xaxes(title="time (s)", row=3, col=1)
    fig.update_yaxes(range=[-0.03, 0.62], title="speed (m/s)", row=1, col=1)
    fig.update_yaxes(range=[-0.01, 0.05], title="zoom (m/s)", row=2, col=1)
    fig.update_yaxes(range=[-11, 12], title="force (N)", row=3, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1040, margin=dict(l=100, r=30, t=60, b=70),
                      legend=dict(x=0.99, xanchor="right", y=1.0, yanchor="top", font=dict(size=17)))
    return fig


idx = list(range(0, len(tt), 3)) + [len(tt) - 1]
figs = [frame(i) for i in idx]
make_gif(figs, here / "smoother_anim", fps=8, holds=[6] + [1] * (len(idx) - 2) + [24],
         keys=[idx.index(30), idx.index(129), len(idx) - 1], cols=1, width=850)
