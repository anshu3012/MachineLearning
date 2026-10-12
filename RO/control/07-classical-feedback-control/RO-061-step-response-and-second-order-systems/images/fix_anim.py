"""The fix: the same 0.5 rad turn with the first-try gains (Kp = 0.4, Kd = 0.08: zeta = 0.2) and with the designed
gains (Kp = 0.4, Kd = 0.4: zeta = 1, wn = 2 rad/s). Left and middle: the two robots from above, target dashed.
Right: both headings over time, with the 2 percent band. The first try peaks at 0.763 rad and settles at 9.80 s;
the designed loop never passes 0.5 rad and settles at 2.92 s.
Run: python fix_anim.py -> fix_anim.gif, fix_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from robotdraw import robot
from stepkit import KD_NEW, KD_OLD, TH_REF, heading_pd, step_info

here = Path(__file__).parent
t = np.linspace(0, 10, 10001)
old, _, _ = heading_pd(t, kd=KD_OLD)
new, _, tq = heading_pd(t, kd=KD_NEW)
io, inew = step_info(t, old, TH_REF, TH_REF), step_info(t, new, TH_REF, TH_REF)
assert abs(io["peak"] - 0.763) < 5e-4 and abs(io["settle"] - 9.80) < 5e-3
assert inew["overshoot"] == 0 and abs(inew["settle"] - 2.92) < 5e-3 and tq.max() <= 0.2 + 1e-9
TK = np.round(np.arange(0, 10.01, 0.25), 2)
RUNS = [("first try:<br>Kd = 0.08, ζ = 0.2", old, RED), ("designed:<br>Kd = 0.4, ζ = 1", new, GREEN)]


def frame(tk, last=False):
    k = int(round(tk * 1000))
    fig = make_subplots(rows=1, cols=3, column_widths=[0.25, 0.25, 0.5], horizontal_spacing=0.06,
                        subplot_titles=[RUNS[0][0], RUNS[1][0], "heading θ over time"])
    for c, (_, y, col) in enumerate(RUNS, start=1):
        fig.add_trace(go.Scatter(x=[0, 0.6 * np.cos(TH_REF)], y=[0, 0.6 * np.sin(TH_REF)], mode="lines",
                                 line=dict(color=GREY, width=3, dash="dash")), 1, c)
        for tr in robot((0, 0, y[k]), scale=1.4):
            fig.add_trace(tr, 1, c)
        fig.add_annotation(x=0, y=-0.42, text=f"θ = {y[k]:.3f} rad", showarrow=False, font=dict(color=col, size=23),
                           row=1, col=c)
        fig.update_xaxes(range=[-0.5, 0.65], visible=False, row=1, col=c)
        fig.update_yaxes(range=[-0.5, 0.75], visible=False, scaleanchor=f"x{c}", scaleratio=1, row=1, col=c)
    fig.add_trace(go.Scatter(x=[0, 10, 10, 0, 0], y=[0.49, 0.49, 0.51, 0.51, 0.49], fill="toself", mode="lines",
                             line=dict(width=0), fillcolor="rgba(84,162,75,0.25)"), 1, 3)
    fig.add_trace(go.Scatter(x=[0, 10], y=[TH_REF, TH_REF], mode="lines", line=dict(color=GREY, width=2, dash="dash")),
                  1, 3)
    for _, y, col in RUNS:
        fig.add_trace(go.Scatter(x=t[:k + 1], y=y[:k + 1], mode="lines", line=dict(color=col, width=4)), 1, 3)
        fig.add_trace(go.Scatter(x=[t[k]], y=[y[k]], mode="markers", marker=dict(color=col, size=12)), 1, 3)
    if last:
        fig.add_annotation(x=io["t_peak"], y=io["peak"], text="peak 0.763 rad, settles 9.80 s", ax=120, ay=-5,
                           xanchor="left", arrowcolor=RED, font=dict(color=RED, size=18), row=1, col=3)
        fig.add_annotation(x=inew["settle"], y=0.49, text="no overshoot, settles 2.92 s", ax=90, ay=60,
                           xanchor="left", arrowcolor=GREEN, font=dict(color=GREEN, size=18), row=1, col=3)
    fig.update_xaxes(range=[0, 10], title="time t (s)", row=1, col=3)
    fig.update_yaxes(range=[0, 0.85], title="heading θ (rad)", row=1, col=3)
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=600, showlegend=False,
                      margin=dict(l=30, r=30, t=130, b=70),
                      title=dict(x=0.5, y=0.95, text=f"the same 0.5 rad turn, two pairs of gains (Kp = 0.4):   t = {tk:.2f} s"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=22)
    return fig


figs = [frame(tk) for tk in TK] + [frame(10.0, last=True)]
make_gif(figs, here / "fix_anim", fps=8, holds=[8] + [1] * (len(TK) - 1) + [30], keys=[6, 12, 20, len(figs) - 1],
         cols=2, width=950)
