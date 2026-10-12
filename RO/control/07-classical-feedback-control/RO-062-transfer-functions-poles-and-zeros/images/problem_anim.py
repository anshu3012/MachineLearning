"""The opening problem. The robot drives straight at 0.5 m/s while its worn gearbox (RO-060) drags with a steady
0.02 N m that turns it to the right. Three heading loops, all with RO-061's PD gains
(Kp = Kd = 0.4): no integral (Ki = 0), a small integral gain (Ki = 0.2) and a large one (Ki = 2).
Top: the path from above; the sideways scale is stretched 4 times (scaleratio). Bottom: the heading over time.
PD alone settles 0.05 rad to the right and drifts 0.72 m to the right in 30 s (15 m); Ki = 0.2 brings the heading back to 0;
Ki = 2 weaves wider and wider, to 0.30 rad by 30 s. Run: python problem_anim.py -> problem_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif
from tfkit import KI_BAD, KI_GOOD, drag_response, drive_path

here = Path(__file__).parent
t = np.linspace(0, 30, 30001)
RUNS = []
for ki, col, name in ((0.0, BLUE, "PD only (Ki = 0)"), (KI_GOOD, GREEN, "Ki = 0.2"), (KI_BAD, RED, "Ki = 2")):
    th = drag_response(t, ki)
    x, y = drive_path(t, th)
    RUNS.append((name, col, th, x, y))
assert abs(RUNS[0][2][-1] + 0.05) < 1e-4 and abs(RUNS[0][4][-1] + 0.725) < 1e-3
assert abs(RUNS[1][2][-1]) < 1e-4 and abs(np.abs(RUNS[2][2]).max() - 0.302) < 1e-3
TK = np.round(np.arange(0, 30.01, 0.5), 1)


def frame(tk):
    k = int(round(tk * 1000))
    fig = make_subplots(rows=2, cols=1, row_heights=[0.45, 0.55], vertical_spacing=0.16,
                        subplot_titles=["path from above (sideways scale stretched 4 times)", "heading θ over time"])
    fig.add_trace(go.Scatter(x=[0, 15], y=[0, 0], mode="lines", line=dict(color=GREY, width=2, dash="dash"),
                             showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 30], y=[0, 0], mode="lines", line=dict(color=GREY, width=2, dash="dash"),
                             showlegend=False), 2, 1)
    for name, col, th, x, y in RUNS:
        fig.add_trace(go.Scatter(x=x[:k + 1], y=y[:k + 1], mode="lines", line=dict(color=col, width=4), name=name), 1, 1)
        fig.add_trace(go.Scatter(x=[x[k]], y=[y[k]], mode="markers", marker=dict(color=col, size=12),
                                 showlegend=False), 1, 1)
        fig.add_trace(go.Scatter(x=t[:k + 1], y=th[:k + 1], mode="lines", line=dict(color=col, width=4),
                                 showlegend=False), 2, 1)
    if tk >= 30:
        fig.add_annotation(x=15, y=RUNS[0][4][-1], text="0.72 m to the right of the line", showarrow=False, xanchor="right",
                           yanchor="top", yshift=-6, font=dict(color=BLUE, size=19), row=1, col=1)
        fig.add_annotation(x=5.5, y=-0.05, text="PD alone: 0.05 rad to the right", showarrow=False, xanchor="left",
                           yanchor="top", yshift=-4, font=dict(color=BLUE, size=19), row=2, col=1)
        fig.add_annotation(x=5.5, y=0.25, text="Ki = 2: weaves wider, ±0.30 rad by 30 s", showarrow=False,
                           xanchor="left", yanchor="middle", font=dict(color=RED, size=19), row=2, col=1)
    fig.update_xaxes(title="distance along the line (m)", range=[0, 15.5], row=1, col=1)
    fig.update_yaxes(title="sideways (m), left is +", range=[-0.85, 0.12], scaleanchor="x", scaleratio=4, constrain="domain",
                     row=1, col=1)
    fig.update_xaxes(title="time t (s)", range=[0, 30], row=2, col=1)
    fig.update_yaxes(title="heading θ (rad), left is +", range=[-0.33, 0.33], row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=900,
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.13, font=dict(size=20)),
                      margin=dict(l=90, r=30, t=170, b=70),
                      title=dict(x=0.5, y=0.97, text=f"right gearbox drags 0.02 N·m to the right, driving at 0.5 m/s:   t = {tk:.1f} s"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=21)
    return fig


figs = [frame(tk) for tk in TK]
make_gif(figs, here / "problem_anim", fps=8, holds=[8] + [1] * (len(TK) - 2) + [30], keys=[10, 30, 50, len(TK) - 1],
         cols=2, width=850)
