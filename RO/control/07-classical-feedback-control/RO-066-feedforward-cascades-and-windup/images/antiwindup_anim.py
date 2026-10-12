"""The held robot of the windup animation with three controllers: no anti-windup, clamping (stop integrating while the
output is saturated and the error has the same sign as the command), and back-calculation (k_aw = 1 per s).
One frame per 0.2 s. Top: the integral term; it climbs to 14.9 N without anti-windup, stays at 0 N with clamping and
falls to -1.9 N with back-calculation. Bottom: speed after the release; peaks 1.04 and 0.515 m/s, and back-calculation
comes up to 0.5 m/s without overshooting.
Run: python antiwindup_anim.py -> antiwindup_anim.gif, antiwindup_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif
from robotctl import DT, speed_loop

here = Path(__file__).parent
run = lambda mode, kaw=None: speed_loop(14, lambda t: 0.5, v0=0.5, ff=True, i0=0.0, hold=(2, 5), mode=mode, kaw=kaw)
R = [(run("none"), RED, "no anti-windup", "1.04 m/s"), (run("clamp"), BLUE, "clamping", "0.515 m/s"),
     (run("bc", 1.0), GREEN, "back-calculation", "no overshoot")]
t = R[0][0]["t"]
i5 = int(round(5 / DT))
for (s, _, _, peak), I5, vmax in zip(R, (14.90, 0.0, -1.90), (1.039, 0.515, 0.500)):
    assert abs(s["i"][i5 - 1] - I5) < 0.01 and abs(s["v"][i5:].max() - vmax) < 5e-4


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.48, 0.52], vertical_spacing=0.12)
    for row in (1, 2):
        fig.add_vrect(x0=2, x1=5, fillcolor="#F58518", opacity=0.18, layer="below", line_width=0, exclude_empty_subplots=False, row=row, col=1)
    for s, col, name, peak in R:
        fig.add_trace(go.Scatter(x=t[:k + 1], y=s["i"][:k + 1], mode="lines", line=dict(color=col, width=4),
                                 name=name), row=1, col=1)
        fig.add_trace(go.Scatter(x=t[:k + 1], y=s["v"][:k + 1], mode="lines", line=dict(color=col, width=4),
                                 showlegend=False), row=2, col=1)
        j = i5 + s["v"][i5:].argmax() if col != GREEN else int(round(10.0 / DT))
        if k >= j:
            fig.add_annotation(x=t[j], y=s["v"][j], xref="x2", yref="y2", ax=(45 if col == RED else 60), ay=(-28 if col == RED else 70 if col == BLUE else 110),
                               xanchor="left", text=peak, font=dict(size=18, color=col), arrowcolor=col)
    fig.add_trace(go.Scatter(x=[0, 14], y=[0.6, 0.6], mode="lines", line=dict(color=RED, width=2, dash="dot"),
                             showlegend=False), row=2, col=1)
    fig.add_annotation(x=12.9, y=0.66, xref="x2", yref="y2", text="top speed", showarrow=False,
                       font=dict(size=17, color=RED))
    fig.add_annotation(x=3.5, y=18.2, xref="x", yref="y", text="held", showarrow=False, font=dict(size=20, color="#F58518"))
    fig.add_annotation(x=0.02, y=1.05, xref="paper", yref="paper", text=f"t = {t[k]:.1f} s", showarrow=False,
                       font=dict(size=21), xanchor="left")
    fig.update_xaxes(range=[0, 14], row=1, col=1)
    fig.update_xaxes(range=[0, 14], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[-4, 19.5], title="integral term (N)", row=1, col=1)
    fig.update_yaxes(range=[-0.05, 1.2], title="speed (m/s)", row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=820, margin=dict(l=100, r=30, t=60, b=70),
                      legend=dict(x=0.99, xanchor="right", y=0.99, yanchor="top", font=dict(size=18)))
    return fig


ks = list(range(0, len(t), 20))
figs = [frame(k) for k in ks]
make_gif(figs, here / "antiwindup_anim", fps=8, holds=[6] + [1] * (len(ks) - 2) + [24],
         keys=[ks.index(500), len(ks) - 1], cols=1, width=850)
