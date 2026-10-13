"""What aliasing does inside the loop: the robot cruises at 0.5 m/s while its speed reading carries the wheel's
ripple of 0.01 m/s at 1.59 Hz (grey). One frame per 0.4 s. Top: the PI run at 100 Hz sees the ripple as it is and
answers with a fast, small push: the true speed (blue) wobbles by 0.0025 m/s. Middle: run at 2 Hz, its samples (red
dots) trace a slow 0.41 Hz wave, the controller chases it, and the true speed (red) really surges by 0.0119 m/s.
Bottom: at 2 Hz with an anti-aliasing filter of time constant 0.5 s before the A/D, the samples (purple dots) barely
move and the surge falls to 0.0036 m/s. Run: python alias_loop.py -> alias_loop.gif, alias_loop_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from digikit import A_RIP, sampled_loop
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif

here = Path(__file__).parent
T_END = 16.0
ROWS = [(100, None, BLUE, "100 Hz: the true speed varies by"),
        (2, None, RED, "2 Hz: the true speed surges by"),
        (2, 0.5, PURPLE, "2 Hz, 0.5 s filter before the A/D: surges by")]
runs = [sampled_loop(fs, T=40.0, ripple=A_RIP, tau_f=tf, r0=0.5, r1=0.5) for fs, tf, _, _ in ROWS]
wob = []
for r in runs:
    tail = r["v"][r["t"] > 20]
    wob.append((tail.max() - tail.min()) / 2)
assert [round(w, 4) for w in wob] == [0.0025, 0.0119, 0.0036]


def frame(tc, last=False):
    titles = [f"{name} {w:.4f} m/s" if last else name.split(":")[0] for (_, _, _, name), w in zip(ROWS, wob)]
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=titles)
    for i, ((fs, tf, col, _), r) in enumerate(zip(ROWS, runs), start=1):
        m = r["t"] <= tc + 1e-9
        reading = r["v"][m] + A_RIP * np.sin(10 * r["t"][m])
        fig.add_trace(go.Scatter(x=r["t"][m][::4], y=reading[::4], mode="lines", line=dict(color=GREY, width=1.5)),
                      row=i, col=1)
        fig.add_trace(go.Scatter(x=r["t"][m], y=r["v"][m], mode="lines", line=dict(color=col, width=4)), row=i, col=1)
        if fs == 2:
            mk = r["tk"] <= tc + 1e-9
            fig.add_trace(go.Scatter(x=r["tk"][mk], y=r["yk"][mk], mode="markers",
                                     marker=dict(color=col, size=12, line=dict(color="white", width=2))), row=i, col=1)
        fig.update_yaxes(range=[0.476, 0.524], tickvals=[0.48, 0.5, 0.52], title="speed (m/s)" if i == 2 else None,
                         row=i, col=1)
    fig.update_xaxes(range=[0, T_END], title="time (s)", row=3, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, showlegend=False,
                      margin=dict(l=110, r=30, t=170, b=80),
                      title=dict(x=0.5, y=0.965, text=f"t = {tc:.1f} s: cruising at 0.5 m/s<br><sup>grey: the speed "
                                                     f"reading with the wheel's 1.59 Hz ripple; thick: the true speed</sup>"))
    fig.update_annotations(font=dict(size=22))
    return fig


ts = np.round(np.arange(0, T_END + 1e-9, 0.4), 1)
figs = [frame(t) for t in ts] + [frame(T_END, last=True)]
make_gif(figs, here / "alias_loop", fps=5, holds=[5] + [1] * (len(ts) - 1) + [20], keys=[12, len(figs) - 1],
         cols=1, width=800)
