"""Opening animation: the robot reaches a corner of its route at 0.5 m/s and must turn from heading 0 to 45 degrees.
Its turning torque is set by the rule that worked for the speed: proportional to the heading error, 0.2 N m per rad.
Top: the robot on the floor, seen from above, with the route's next leg dashed. Bottom: its heading over time.
The heading swings to 90.5 degrees at 2.22 s, back to -1.0 degrees at 4.44 s, and up again: the swing does not die
out. One frame per 0.2 s for 6.6 s; the last frame adds the PD controller of Section 4 (blue), which turns to 45 degrees
without swinging. Run -> opening.gif, opening_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import headkit as h
from gifkit import BLUE, FONT, GREY, RED, make_gif
from robotdraw import robot

here = Path(__file__).parent
T = 6.6
P, PD = h.run(T), h.run(T, kd=h.KD)
tp, pk = h.peaks(P)
assert abs(tp[0] - 2.22) < 1e-9 and round(np.degrees(pk[0]), 1) == 90.5
k444 = int(round(4.44 / h.DT))
assert round(np.degrees(P["th"][k444]), 1) == -1.0
assert round(np.degrees(PD["th"].max()), 1) == 45.0


def frame(t, final=False):
    k = int(round(t / h.DT))
    fig = make_subplots(rows=2, cols=1, row_heights=[0.55, 0.45], vertical_spacing=0.1,
                        subplot_titles=["", "heading over time"])
    L = np.array([0, 2.4])
    fig.add_trace(go.Scatter(x=[-0.7, 0], y=[0, 0], mode="lines", line=dict(color=GREY, width=3), showlegend=False),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=L * np.cos(h.TH_REF), y=L * np.sin(h.TH_REF), mode="lines",
                             line=dict(color=GREY, width=3, dash="dash"), showlegend=False), row=1, col=1)
    fig.add_annotation(x=2.2, y=0.15, text="dashed: the route's<br>next leg, at 45°", showarrow=False,
                       font=dict(size=18, color=GREY), row=1, col=1)
    runs = [(P, RED, "torque proportional to the error")] + ([(PD, BLUE, "PD controller (Section 4)")] if final else [])
    for run, col, name in runs:
        kk = len(run["t"]) - 1 if final else k
        fig.add_trace(go.Scatter(x=run["x"][:kk + 1], y=run["y"][:kk + 1], mode="lines", line=dict(color=col, width=4),
                                 name=name), row=1, col=1)
        for tr in robot((run["x"][kk], run["y"][kk], run["th"][kk]), scale=1.4, color=col):
            fig.add_trace(tr.update(showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=run["t"][:kk + 1], y=np.degrees(run["th"][:kk + 1]), mode="lines",
                                 line=dict(color=col, width=4), showlegend=False), row=2, col=1)
    fig.add_hline(y=45, line=dict(color=GREY, width=2, dash="dash"), row=2, col=1)
    fig.add_annotation(x=0.05, y=50, text="wanted: 45°", xanchor="left", showarrow=False, font=dict(size=17, color=GREY),
                       row=2, col=1)
    if t >= 2.22:
        fig.add_annotation(x=2.22, y=90.5, text="90.5° at 2.22 s", showarrow=True, ax=40, ay=-25, arrowhead=2,
                           font=dict(size=17, color=RED), row=2, col=1)
    if t >= 4.44:
        fig.add_annotation(x=4.44, y=-1.0, text="−1.0° at 4.44 s", showarrow=True, ax=45, ay=20, arrowhead=2,
                           font=dict(size=17, color=RED), row=2, col=1)
    fig.update_xaxes(range=[-0.8, 2.9], dtick=0.5, ticksuffix=" m", constrain="domain", row=1, col=1)
    fig.update_yaxes(range=[-0.5, 2.3], dtick=0.5, ticksuffix=" m", scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[0, T], dtick=1, title="time after the corner (s)", row=2, col=1)
    fig.update_yaxes(range=[-10, 105], dtick=15, title="heading (°)", row=2, col=1)
    title = ("the swing never dies out; the PD controller (blue) turns to 45° and stays" if final else
             f"t = {t:.1f} s: heading {np.degrees(P['th'][k]):.1f}°")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1180, margin=dict(l=90, r=30, t=140, b=70),
                      title=dict(text=title, x=0.5, y=0.985, font=dict(size=21)),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.0, yanchor="bottom", font=dict(size=18)))
    for a in fig.layout.annotations[:2]:
        a.font.size = 19
    fig.add_annotation(x=-0.75, y=2.2, xanchor="left", text="the floor, seen from above", showarrow=False,
                       font=dict(size=18, color=GREY), row=1, col=1)
    return fig


times = list(np.round(np.arange(0, T + 0.001, 0.2), 1))
figs = [frame(t) for t in times] + [frame(T, final=True)]
make_gif(figs, here / "opening", fps=5, holds=[8] + [2] * (len(times) - 1) + [26],
         keys=[0, 6, 11, len(figs) - 1], cols=2, width=900)
