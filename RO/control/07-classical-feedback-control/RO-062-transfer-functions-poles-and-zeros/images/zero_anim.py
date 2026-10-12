"""A zero changes the shape without moving the poles. The 0.5 rad turn with Kp = Kd = 0.4, two ways:
D on the measured turn rate, closed loop 4 / (s^2 + 4 s + 4), poles -2 and -2, no zero (blue);
D on the error, closed loop (4 s + 4) / (s^2 + 4 s + 4), the same poles and a zero at -1 (orange).
The zero adds the derivative of the blue response (purple dotted) to it: the orange turn peaks at 0.568 rad at 1.0 s,
13.5 percent past the target, although the damping ratio is 1. Left: the poles (x) and the zero (o).
Run: python zero_anim.py -> zero_anim.gif, zero_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import scipy.signal as sig
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, RED, make_gif

here = Path(__file__).parent
t = np.linspace(0, 5, 5001)
_, y = sig.step(sig.lti([4], [1, 4, 4]), T=t)
_, yz = sig.step(sig.lti([4, 4], [1, 4, 4]), T=t)
y, yz = 0.5 * y, 0.5 * yz
dy = np.gradient(y, t)
assert np.abs(yz - (y + dy)).max() < 1e-3                       # the zero at -1 adds the derivative: yz = y + y'
assert abs(yz.max() - 0.5677) < 1e-4 and abs(t[yz.argmax()] - 1.0) < 2e-3 and y.max() <= 0.5   # no zero: never past
TK = np.round(np.arange(0, 5.01, 0.125), 3)


def frame(tk):
    k = int(round(tk * 1000))
    fig = make_subplots(rows=1, cols=2, column_widths=[0.38, 0.62], horizontal_spacing=0.1,
                        subplot_titles=["poles (x) and the zero (o)", "the 0.5 rad turn"])
    fig.add_trace(go.Scatter(x=[-3, 1], y=[0, 0], mode="lines", line=dict(color="black", width=1.5)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 0], y=[-1.5, 1.5], mode="lines", line=dict(color="black", width=1.5)), 1, 1)
    fig.add_trace(go.Scatter(x=[-2], y=[0], mode="markers", marker=dict(symbol="x", size=22, color=RED,
                                                                       line=dict(width=2))), 1, 1)
    fig.add_annotation(x=-2, y=0, text="−2, twice", showarrow=False, yanchor="bottom", yshift=16,
                       font=dict(color=RED, size=18), row=1, col=1)
    fig.add_trace(go.Scatter(x=[-1], y=[0], mode="markers", marker=dict(symbol="circle-open", size=20, color=ORANGE,
                                                                       line=dict(width=4))), 1, 1)
    fig.add_annotation(x=-1, y=0, text="zero at −1<br>(D on the error)", showarrow=False, yanchor="top", yshift=-16,
                       font=dict(color=ORANGE, size=18), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0, 5], y=[0.5, 0.5], mode="lines", line=dict(color=GREY, width=2, dash="dash")), 1, 2)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=dy[:k + 1], mode="lines", line=dict(color=PURPLE, width=3, dash="dot"),
                             name="added: its rate of change"), 1, 2)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=y[:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                             name="D on the turn rate: no zero"), 1, 2)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=yz[:k + 1], mode="lines", line=dict(color=ORANGE, width=4),
                             name="D on the error: zero at −1"), 1, 2)
    if tk >= 1.0:
        fig.add_annotation(x=1.0, y=yz.max(), text="peak 0.568 rad: 13.5 % past", ax=110, ay=-30, xanchor="left",
                           arrowcolor=ORANGE, font=dict(color=ORANGE, size=19), row=1, col=2)
    fig.update_xaxes(range=[-3, 1], title="real part", row=1, col=1)
    fig.update_yaxes(range=[-1.5, 1.5], title="imaginary part", row=1, col=1)
    fig.update_xaxes(range=[0, 5], title="time t (s)", row=1, col=2)
    fig.update_yaxes(range=[0, 0.75], title="heading θ (rad)", row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=680,
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.2, font=dict(size=18)),
                      margin=dict(l=70, r=30, t=180, b=70),
                      title=dict(x=0.5, y=0.97, text=f"same poles, one zero added:   t = {tk:.2f} s"))
    for tr in fig.data:
        if not tr.name:
            tr.showlegend = False
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=21)
    return fig


figs = [frame(tk) for tk in TK]
make_gif(figs, here / "zero_anim", fps=8, holds=[8] + [1] * (len(TK) - 2) + [30], keys=[8, len(TK) - 1], cols=1,
         width=900)
