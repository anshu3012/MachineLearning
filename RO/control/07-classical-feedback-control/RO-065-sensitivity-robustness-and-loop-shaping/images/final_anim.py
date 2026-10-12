"""The lead-lag heading controller against the PD loop, on the opening problem: a 0.02 N m drag starts at t = 1 s. Top:
as modelled; the PD loop (blue) settles 0.05 rad off, the lead-lag (green) peaks at 0.071 rad and creeps down towards
0.0096 rad (0.0097 at 30 s). Bottom: the real robot (payload, inertia 0.15 kg m^2, and a 0.25 s delay); the PD swing keeps growing, the
lead-lag settles (peak 0.095 rad). Run: python final_anim.py -> final_anim.gif, final_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, make_gif
from shapekit import DRAG, I_PAY, TAU_REAL, sim

here = Path(__file__).parent
t = np.arange(0, 30.001, 1e-3)
runs = {(k, real): sim(k, t, dist=DRAG, **(dict(inertia=I_PAY, tau=TAU_REAL) if real else {}))[0]
        for k in ("pd", "leadlag") for real in (False, True)}
assert abs(runs["leadlag", False].max() - 0.0712) < 5e-4 and abs(runs["leadlag", False][-1] - 0.0097) < 2e-4
assert abs(runs["leadlag", True].max() - 0.0949) < 5e-4 and np.ptp(runs["leadlag", True][t > 25]) < 1e-3
assert np.ptp(runs["pd", True][t > 25]) > 0.5


def frame(tn, last=False):
    k = t <= tn
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.17, subplot_titles=(
        "as modelled: inertia 0.1 kg·m², no delay",
        "the real robot: payload (inertia 0.15 kg·m²), 0.25 s delay"))
    for a in fig.layout.annotations:
        a.font = dict(size=20)
    for row, real, rng in ((1, False, 0.12), (2, True, 0.6)):
        fig.add_trace(go.Scatter(x=[1, 1], y=[-rng, rng], mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                                 showlegend=False), row, 1)
        for kind, col, name in (("pd", BLUE, "PD, Kd = 0.08"), ("leadlag", GREEN, "lead-lag")):
            fig.add_trace(go.Scatter(x=t[k][::20], y=runs[kind, real][k][::20], mode="lines",
                                     line=dict(color=col, width=4), name=name, showlegend=row == 1), row, 1)
    if last:
        fig.add_annotation(x=30, y=0.05, text="PD: 0.05 rad", ax=-60, ay=-40, font=dict(size=18, color=BLUE),
                           arrowcolor=BLUE, row=1, col=1)
        fig.add_annotation(x=30, y=0.0097, text="lead-lag: 0.0097 rad at 30 s", ax=-90, ay=25, font=dict(size=18, color=GREEN),
                           arrowcolor=GREEN, row=1, col=1)
        fig.add_annotation(x=20, y=0.0, text="lead-lag settles", ax=0, ay=60, font=dict(size=18, color=GREEN),
                           arrowcolor=GREEN, row=2, col=1)
        fig.add_annotation(x=t[np.argmax(runs["pd", True])], y=runs["pd", True].max(), text="PD keeps growing",
                           ax=-150, ay=0, font=dict(size=18, color=BLUE), arrowcolor=BLUE, row=2, col=1)
    fig.update_xaxes(range=[0, 30], title_text="time (s)")
    fig.update_yaxes(title_text="heading error (rad)", range=[-0.02, 0.12], row=1, col=1)
    fig.update_yaxes(title_text="heading error (rad)", range=[-0.6, 0.6], row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1000, margin=dict(l=100, r=30, t=210, b=70),
                      legend=dict(x=0.0, y=1.06, yanchor="bottom", orientation="h", font=dict(size=18)),
                      title=dict(x=0.5, y=0.975, text=f"the same drag, PD against lead-lag<br>t = {tn:.0f} s"))
    return fig


times = list(range(0, 31, 2))
figs = [frame(x) for x in times] + [frame(30, last=True)]
make_gif(figs, here / "final_anim", fps=3, holds=[3] + [1] * (len(times) - 1) + [12], keys=[4, len(times)], cols=2,
         width=800)
