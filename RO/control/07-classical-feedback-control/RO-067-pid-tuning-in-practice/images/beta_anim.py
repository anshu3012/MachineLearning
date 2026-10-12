"""Set-point weighting on RO-060's heading PID (kp = 0.2, ki = 0.05, kd = 0.283, derivative on the measurement). The
heading command steps from 0 to 0.1 rad at t = 0.5 s; the proportional term sees only beta times the command: beta = 1,
0.5 and 0. Overshoot 22.5, 1.6 and 0.3 percent; inside 2 percent of the command after 11.11, 5.42 and 9.53 s. The integral
always acts on the whole error, so every run ends on 0.1 rad.
Run: python beta_anim.py -> beta_anim.gif, beta_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, ORANGE, make_gif
from tunekit import heading_run, overshoot, settle

here = Path(__file__).parent
T = 14.0
RUNS = [(b, heading_run(T, beta=b, gamma=0.0), c) for b, c in ((1.0, BLUE), (0.5, GREEN), (0.0, ORANGE))]
want = {1.0: (22.5, 11.11), 0.5: (1.6, 5.42), 0.0: (0.3, 9.53)}
for b, o, _ in RUNS:
    os_, ts = want[b]
    assert abs(max(overshoot(o), 0) - os_) < 0.06 and abs(settle(o) - ts) < 0.006, (b, overshoot(o), settle(o))
    assert abs(o["th"][-1] - 0.1) < 0.001


def frame(upto, final=False):
    n = int(round(upto / 0.01)) + 1
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.58, 0.42])
    for b, o, col in RUNS:
        os_, ts = want[b]
        fig.add_trace(go.Scatter(x=o["t"][:n], y=o["th"][:n], mode="lines", line=dict(color=col, width=3.5),
                                 name=f"β = {b:g}: overshoot {os_:g} percent, settled {ts:.2f} s"), row=1, col=1)
        fig.add_trace(go.Scatter(x=o["t"][:n], y=o["c"][:n], mode="lines", line=dict(color=col, width=3),
                                 showlegend=False), row=2, col=1)
    fig.add_hline(y=0.1, line=dict(color="black", width=1, dash="dash"), row=1, col=1)
    title = (f"t = {upto:.1f} s: heading command 0.1 rad from t = 0.5 s" if not final else
             "β = 0.5 cuts the overshoot to 1.6 percent and settles fastest")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=820,
                      margin=dict(l=110, r=30, t=220, b=80), title=dict(text=title, x=0.5, y=0.97),
                      legend=dict(x=0.5, xanchor="center", y=1.03, yanchor="bottom", font=dict(size=18)))
    fig.update_yaxes(title_text="heading (rad)", range=[-0.005, 0.135], row=1, col=1)
    fig.update_yaxes(title_text="torque request (N m)", range=[-0.01, 0.025], row=2, col=1)
    fig.update_xaxes(range=[0, T], row=1, col=1)
    fig.update_xaxes(title_text="time t (s)", range=[0, T], row=2, col=1)
    return fig


times = [0.3, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0]
figs = [frame(x) for x in times] + [frame(T, final=True)]
make_gif(figs, here / "beta_anim", fps=3, holds=[3] + [1] * (len(times) - 1) + [12],
         keys=[4, len(figs) - 1], cols=1, width=850)
