"""The derivative filter. The robot drives straight at 0.5 m/s and the heading PID holds the heading at 0; the heading
comes from 1024-tick wheel encoders, so it moves in steps of 1.53 mrad (one tick of 0.307 mm over the 0.2 m between
the wheels). Top: the measured heading of the unfiltered run, in mrad. Bottom: the D term (derivative on the
measurement, RO-060's kd = 0.283). Unfiltered (red), each step is a jump of 0.153 rad/s over one 0.01 s sample, so the
D term jumps by 0.043 N m, a fifth of the 0.2 N m torque limit. Filtered with Tf = Td/N = 0.1415 s (N = 10, blue), it
stays under 0.003 N m. Time runs frame by frame over one second.
Run: python dfilter_anim.py -> dfilter_anim.gif, dfilter_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, RED, make_gif
from tunekit import DS, DT, HKD, L_WHEELS, heading_run

here = Path(__file__).parent
T = 1.0
raw = heading_run(T, step=0.0, gamma=0.0, quant=True)
filt = heading_run(T, step=0.0, gamma=0.0, quant=True, N=10)
tick = DS / L_WHEELS
assert abs(DS - 0.000307) < 5e-7 and abs(tick - 0.00153) < 5e-6 and abs(HKD * tick / DT - 0.0434) < 0.0001
assert abs(abs(raw["D"]).max() - 0.0434) < 0.0001 and abs(filt["D"]).max() < 0.003
assert set(np.unique(np.round(raw["y"] / tick))) <= {-1.0, 0.0, 1.0}          # the measured heading flickers by one tick


def frame(upto, final=False):
    n = int(round(upto / DT)) + 1
    t = raw["t"][:n]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.42, 0.58])
    fig.add_trace(go.Scatter(x=t, y=raw["th"][:n] * 1000, mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                             name="true heading"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=raw["y"][:n] * 1000, mode="lines", line=dict(color="black", width=3, shape="hv"),
                             name="measured heading"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=raw["D"][:n], mode="lines", line=dict(color=RED, width=3),
                             name="D term, unfiltered"), row=2, col=1)
    fig.add_trace(go.Scatter(x=t, y=filt["D"][:n], mode="lines", line=dict(color=BLUE, width=4),
                             name="D term, filtered (N = 10)"), row=2, col=1)
    title = (f"t = {upto:.2f} s: one encoder tick = 1.53 mrad of heading" if not final else
             "unfiltered jumps of 0.043 N m; filtered under 0.003 N m")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=820,
                      margin=dict(l=120, r=30, t=200, b=80), title=dict(text=title, x=0.5, y=0.97),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.03, yanchor="bottom",
                                  font=dict(size=18)))
    fig.update_yaxes(title_text="heading (mrad)", range=[-2.2, 2.2], row=1, col=1)
    fig.update_yaxes(title_text="D term (N m)", range=[-0.055, 0.055], row=2, col=1)
    fig.update_xaxes(range=[0, T], row=1, col=1)
    fig.update_xaxes(title_text="time t (s)", range=[0, T], row=2, col=1)
    return fig


times = list(np.round(np.arange(0.1, T + 0.001, 0.05), 2))
figs = [frame(x) for x in times] + [frame(T, final=True)]
make_gif(figs, here / "dfilter_anim", fps=4, holds=[3] + [1] * (len(times) - 1) + [12],
         keys=[6, len(figs) - 1], cols=1, width=850)
