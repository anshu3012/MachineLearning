"""Non-minimum phase: reversing robot, front point. The robot turns 0.5 rad left (RO-061's critically damped turn)
while driving at 0.1 m/s, forwards (left) or backwards (middle). The purple dot is a point on the front bumper, 0.1 m
ahead of the axle, with its trail. Right: the sideways position of that point. Forwards it moves left from the start
(0.24 m after 5 s). Backwards it first moves the wrong way, 0.016 m to the left by 0.94 s, crosses back at 1.78 s and
ends 0.145 m to the right. Run: python reverse_anim.py -> reverse_anim.gif, reverse_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREEN, GREY, PURPLE, RED, make_gif
from robotdraw import robot
from tfkit import reverse_front

here = Path(__file__).parent
t = np.linspace(0, 5, 5001)
A = 0.1
RUNS = []
for v, col, name in ((0.1, GREEN, "forwards, 0.1 m/s: green line"), (-0.1, RED, "backwards, 0.1 m/s: red line")):
    x, y, th, yf = reverse_front(t, v, a=A)
    RUNS.append((name, col, x, y, th, x + A * np.cos(th), yf))
yr = RUNS[1][6]
k_up = int(yr.argmax())
cross = t[np.where(yr[1:] * yr[:-1] < 0)[0][0] + 1]
assert abs(yr.max() - 0.0159) < 2e-4 and abs(t[k_up] - 0.938) < 0.01 and abs(cross - 1.781) < 0.01
assert abs(yr[-1] + 0.1451) < 2e-4 and RUNS[0][6].min() > -1e-9 and abs(RUNS[0][6][-1] - 0.2409) < 5e-4
TK = np.round(np.arange(0, 5.01, 0.125), 3)


def frame(tk):
    k = int(round(tk * 1000))
    fig = make_subplots(rows=1, cols=3, column_widths=[0.27, 0.27, 0.46], horizontal_spacing=0.11,
                        subplot_titles=[RUNS[0][0], RUNS[1][0], "sideways position of the front point"])
    for c, (name, col, x, y, th, xf, yf) in enumerate(RUNS, start=1):
        fig.add_trace(go.Scatter(x=[-0.8, 0.8], y=[0, 0], mode="lines", line=dict(color=GREY, width=1.5, dash="dash")),
                      1, c)
        for tr in robot((x[k], y[k], th[k]), scale=1.0):
            fig.add_trace(tr, 1, c)
        fig.add_trace(go.Scatter(x=xf[:k + 1], y=yf[:k + 1], mode="lines", line=dict(color=PURPLE, width=3)), 1, c)
        fig.add_trace(go.Scatter(x=[xf[k]], y=[yf[k]], mode="markers", marker=dict(color=PURPLE, size=12)), 1, c)
        fig.update_xaxes(range=[-0.25, 0.8] if c == 1 else [-0.8, 0.25], visible=False, row=1, col=c)
        fig.update_yaxes(range=[-0.35, 0.45], visible=False, scaleanchor=f"x{c}", scaleratio=1, row=1, col=c)
        fig.add_trace(go.Scatter(x=t[:k + 1], y=yf[:k + 1], mode="lines", line=dict(color=col, width=4)), 1, 3)
    fig.add_trace(go.Scatter(x=[0, 5], y=[0, 0], mode="lines", line=dict(color=GREY, width=1.5, dash="dash")), 1, 3)
    if tk >= 0.94:
        fig.add_annotation(x=t[k_up], y=yr[k_up], text="backwards: 0.016 m the wrong way first", ax=0.1, ay=0.22,
                           axref="x3", ayref="y3", xanchor="left", arrowcolor=RED, font=dict(color=RED, size=18),
                           row=1, col=3)
    if tk >= 1.78:
        fig.add_annotation(x=cross, y=0, text="crosses back at 1.78 s", ax=0.1, ay=-0.09, axref="x3", ayref="y3",
                           xanchor="left", arrowcolor=RED, font=dict(color=RED, size=18), row=1, col=3)
    fig.update_xaxes(range=[0, 5], title="time t (s)", row=1, col=3)
    fig.update_yaxes(range=[-0.17, 0.27], title="sideways (m), left is +", row=1, col=3)
    fig.update_layout(template="simple_white", font=FONT, width=1350, height=600, showlegend=False,
                      margin=dict(l=20, r=30, t=140, b=70),
                      title=dict(x=0.5, y=0.96, text=f"turn 0.5 rad left while driving; purple: front point 0.1 m ahead"
                                                     f" of the axle:   t = {tk:.2f} s"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=21)
    return fig


figs = [frame(tk) for tk in TK]
make_gif(figs, here / "reverse_anim", fps=8, holds=[8] + [1] * (len(TK) - 2) + [30], keys=[8, 16, len(TK) - 1],
         cols=1, width=950)
