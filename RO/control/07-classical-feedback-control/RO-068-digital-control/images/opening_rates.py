"""Opening problem: the same PI speed controller run as code at 100, 10 and 2 Hz. The robot cruises at 0.4 m/s and the
command steps to 0.5 m/s at t = 0. One frame per 0.1 s: the true speed so far (coloured), the samples the computer
read (dots) and the continuous formula's response (grey dashes). Overshoot 5.0, 5.7 and 17.5 percent; the formula 4.9.
Run: python opening_rates.py -> opening_rates.gif, opening_rates_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from digikit import RATES, continuous_loop, overshoot, sampled_loop
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
COL = {100: BLUE, 10: GREEN, 2: RED}
SIZE = {100: 3, 10: 8, 2: 13}
T_END = 6.0
cont = continuous_loop(T_END)
runs = {fs: sampled_loop(fs, T=T_END) for fs in RATES}
ov = {fs: overshoot(sampled_loop(fs)) for fs in RATES}
assert abs(overshoot(continuous_loop()) - 4.9) < 0.05
assert [round(ov[f], 1) for f in RATES] == [5.0, 5.7, 17.5]


def frame(tc, last=False):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.07,
                        subplot_titles=[f"{fs} Hz: a sample every {1 / fs:g} s" + (
                            f", overshoot {ov[fs]:.1f} percent" if last else "") for fs in RATES])
    for i, fs in enumerate(RATES, start=1):
        r = runs[fs]
        fig.add_trace(go.Scatter(x=cont["t"], y=cont["v"], mode="lines", line=dict(color=GREY, width=2, dash="dash"),
                                 showlegend=False), row=i, col=1)
        fig.add_hline(y=0.5, line=dict(color="black", width=1, dash="dot"), row=i, col=1)
        m = r["t"] <= tc + 1e-9
        fig.add_trace(go.Scatter(x=r["t"][m], y=r["v"][m], mode="lines", line=dict(color=COL[fs], width=4),
                                 showlegend=False), row=i, col=1)
        mk = r["tk"] <= tc + 1e-9
        fig.add_trace(go.Scatter(x=r["tk"][mk], y=r["yk"][mk], mode="markers",
                                 marker=dict(color=COL[fs], size=SIZE[fs], line=dict(color="white", width=0 if fs == 100 else 1)),
                                 showlegend=False), row=i, col=1)
        fig.update_yaxes(range=[0.385, 0.53], dtick=0.05, title="speed (m/s)" if i == 2 else None, row=i, col=1)
    fig.update_xaxes(range=[-0.1, T_END], title="time since the command (s)", row=3, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1080, showlegend=False,
                      margin=dict(l=100, r=30, t=170, b=80),
                      title=dict(x=0.5, y=0.975, text=f"t = {tc:.1f} s<br><sup>grey dashes: the continuous formula; "
                                                    f"dots: the samples the computer read</sup>"))
    fig.update_annotations(font=dict(size=22))
    return fig


ts = np.round(np.arange(0, T_END + 1e-9, 0.1), 1)
figs = [frame(t) for t in ts] + [frame(T_END, last=True)]
make_gif(figs, here / "opening_rates", fps=8, holds=[8] + [1] * (len(ts) - 1) + [24], keys=[10, len(figs) - 1],
         cols=2, width=760)
