"""Sampling (the A/D step): the speed reading of a robot cruising at 0.5 m/s on a wheel 1 mm out of round ripples by
0.01 m/s once per wheel turn (10 rad/s, 1.59 Hz). The computer reads it at 100, 10 and 2 Hz; a clock line sweeps
across and a dot appears at every sample. At 100 and 10 Hz the dots follow the wave; at 2 Hz, joined up, they show a
slow wave that is not there (0.41 Hz). Run: python sampling_anim.py -> sampling_anim.gif, sampling_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from digikit import A_RIP, RATES, W_RIP
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
COL = {100: BLUE, 10: GREEN, 2: RED}
SIZE = {100: 5, 10: 9, 2: 14}
T_END = 4.0
tf = np.linspace(0, T_END, 2001)
y = 0.5 + A_RIP * np.sin(W_RIP * tf)
f_true = W_RIP / (2 * np.pi)
assert abs(f_true - 1.59) < 0.005 and abs(abs(f_true - 2) - 0.41) < 0.005
samples = {fs: np.arange(0, T_END + 1e-9, 1 / fs) for fs in RATES}


def frame(tc, last=False):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                        subplot_titles=[f"{fs} Hz: {len(samples[fs][samples[fs] <= tc + 1e-9])} samples so far" + (
                            "; joined up, a slow wave that is not there" if last and fs == 2 else "") for fs in RATES])
    for i, fs in enumerate(RATES, start=1):
        fig.add_trace(go.Scatter(x=tf, y=y, mode="lines", line=dict(color=GREY, width=2), showlegend=False),
                      row=i, col=1)
        tk = samples[fs][samples[fs] <= tc + 1e-9]
        yk = 0.5 + A_RIP * np.sin(W_RIP * tk)
        if last:
            fig.add_trace(go.Scatter(x=tk, y=yk, mode="lines", line=dict(color=COL[fs], width=3), showlegend=False),
                          row=i, col=1)
        fig.add_trace(go.Scatter(x=tk, y=yk, mode="markers", showlegend=False,
                                 marker=dict(color=COL[fs], size=SIZE[fs], line=dict(color="white", width=1))),
                      row=i, col=1)
        fig.add_vline(x=tc, line=dict(color="black", width=2), row=i, col=1)
        fig.update_yaxes(range=[0.486, 0.514], tickvals=[0.49, 0.5, 0.51], title="reading (m/s)" if i == 2 else None,
                         row=i, col=1)
    fig.update_xaxes(range=[-0.05, T_END + 0.05], title="time (s)", row=3, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1000, showlegend=False,
                      margin=dict(l=110, r=30, t=170, b=80),
                      title=dict(x=0.5, y=0.96, text=f"t = {tc:.1f} s<br><sup>grey: the speed reading, rippling 0.01 m/s at 1.59 Hz; "
                                                    f"dots: what the computer reads</sup>"))
    fig.update_annotations(font=dict(size=22))
    return fig


ts = np.round(np.arange(0, T_END + 1e-9, 0.1), 1)
figs = [frame(t) for t in ts] + [frame(T_END, last=True)]
make_gif(figs, here / "sampling_anim", fps=8, holds=[8] + [1] * (len(ts) - 1) + [24], keys=[10, len(figs) - 1],
         cols=2, width=760)
