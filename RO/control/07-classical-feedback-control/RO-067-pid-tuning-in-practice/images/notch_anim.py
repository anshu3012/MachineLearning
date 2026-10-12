"""The notch filter in time. The D term now uses the gyro's turn rate, which also carries the frame's 10 Hz shaking,
0.3 rad/s. The robot drives straight and the heading PID holds the heading at 0. Top: the gyro reading. Bottom: the
D term (RO-060's kd = 0.283) with no filter (red, swings 0.085 N m either way, over 40 percent of the 0.2 N m limit),
with a 1 Hz low-pass (orange, 0.009 N m) and with a 10 Hz notch (blue, under 0.001 N m once the filter has settled).
Run: python notch_anim.py -> notch_anim.gif, notch_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from tunekit import A_VIB, DT, HKD, heading_run, lowpass, notch

here = Path(__file__).parent
T = 2.0
RUNS = [("no filter", heading_run(T, step=0.0, gyro=True, vib=True), RED),
        ("low-pass at 1 Hz", heading_run(T, step=0.0, gyro=True, vib=True, filt=lowpass(1.0)), ORANGE),
        ("notch at 10 Hz", heading_run(T, step=0.0, gyro=True, vib=True, filt=notch()), BLUE)]
late = {name: abs(o["D"][150:]).max() for name, o, _ in RUNS}            # from t = 1.5 s, after the filters settle
assert abs(late["no filter"] - HKD * A_VIB) < 0.002 and abs(HKD * A_VIB - 0.0849) < 1e-12
assert abs(late["low-pass at 1 Hz"] - 0.009) < 0.0005 and late["notch at 10 Hz"] < 0.001
g = RUNS[0][1]["g"]


def frame(upto, final=False):
    n = int(round(upto / DT)) + 1
    t = RUNS[0][1]["t"][:n]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.4, 0.6])
    fig.add_trace(go.Scatter(x=t, y=g[:n], mode="lines", line=dict(color=GREY, width=2.5), name="gyro reading"),
                  row=1, col=1)
    for name, o, col in RUNS:
        fig.add_trace(go.Scatter(x=t, y=o["D"][:n], mode="lines", line=dict(color=col, width=3),
                                 name=f"D term: {name}"), row=2, col=1)
    title = (f"t = {upto:.1f} s: the frame shakes the gyro at 10 Hz" if not final else
             "D term swings: no filter 0.085, low-pass 0.009, notch under 0.001 N m")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=840,
                      margin=dict(l=120, r=30, t=230, b=80), title=dict(text=title, x=0.5, y=0.97),
                      legend=dict(x=0.5, xanchor="center", y=1.03, yanchor="bottom", font=dict(size=18)))
    fig.update_yaxes(title_text="turn rate (rad/s)", range=[-0.4, 0.4], row=1, col=1)
    fig.update_yaxes(title_text="D term (N m)", range=[-0.11, 0.11], row=2, col=1)
    fig.update_xaxes(range=[0, T], row=1, col=1)
    fig.update_xaxes(title_text="time t (s)", range=[0, T], row=2, col=1)
    return fig


times = list(np.round(np.arange(0.2, T + 0.001, 0.1), 1))
figs = [frame(x) for x in times] + [frame(T, final=True)]
make_gif(figs, here / "notch_anim", fps=4, holds=[3] + [1] * (len(times) - 1) + [12],
         keys=[4, len(figs) - 1], cols=1, width=850)
