"""Aliasing, watched on the wheel: a mark on the rim of a wheel turning at 10 rad/s (1.59 turns per second, the robot
at 0.5 m/s), one frame per 0.1 s. Top: the wheel itself, what a computer sampling at 10 Hz last saw (57.3 degrees
forward per sample) and what one sampling at 2 Hz last saw (286.5 degrees per sample, which looks like 73.5 degrees
backwards). Bottom: the mark's height (grey), the 2 Hz samples (red dots) and, in the last frame, the slow wave the
2 Hz samples fit just as well: 0.41 Hz, turning backwards.
Run: python alias_wheel.py -> alias_wheel.gif, alias_wheel_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
W, R, T_END = 10.0, 5.0, 4.0                  # rad/s; wheel radius drawn in cm; s
f_alias = W / (2 * np.pi) - 2.0
assert abs(np.degrees(W * 0.1) - 57.3) < 0.05 and abs(np.degrees(W * 0.5) - 286.5) < 0.05
assert abs(np.degrees(W * 0.5) - 360 - (-73.5)) < 0.05 and abs(f_alias - (-0.41)) < 0.005
k = np.arange(0, int(T_END / 0.5) + 1)
assert np.allclose(np.sin(W * 0.5 * k), np.sin(2 * np.pi * f_alias * 0.5 * k))   # the slow wave fits every sample
th = np.linspace(0, 2 * np.pi, 121)
tf = np.linspace(0, T_END, 1601)


def wheel(fig, col, angle, colour, ghost=None):
    fig.add_trace(go.Scatter(x=R * np.cos(th), y=R * np.sin(th), mode="lines", line=dict(color="black", width=3)),
                  1, col)
    if ghost is not None:
        fig.add_trace(go.Scatter(x=[0, R * np.cos(ghost)], y=[0, R * np.sin(ghost)], mode="lines+markers",
                                 line=dict(color=colour, width=3, dash="dot"), opacity=0.4,
                                 marker=dict(size=[0, 14], color=colour)), 1, col)
    fig.add_trace(go.Scatter(x=[0, R * np.cos(angle)], y=[0, R * np.sin(angle)], mode="lines+markers",
                             line=dict(color=colour, width=5), marker=dict(size=[8, 20], color=colour)), 1, col)
    fig.update_xaxes(range=[-6.5, 6.5], visible=False, row=1, col=col)
    fig.update_yaxes(range=[-6.5, 6.5], visible=False, scaleanchor=f"x{col}", scaleratio=1, row=1, col=col)


def frame(tc, last=False):
    t10 = np.floor(tc / 0.1 + 1e-9) * 0.1
    t2 = np.floor(tc / 0.5 + 1e-9) * 0.5
    fig = make_subplots(rows=2, cols=3, row_heights=[0.5, 0.5], vertical_spacing=0.14,
                        specs=[[{}, {}, {}], [{"colspan": 3}, None, None]],
                        subplot_titles=["the wheel", "seen at 10 Hz", "seen at 2 Hz", "height of the mark (cm)"])
    wheel(fig, 1, W * tc, GREY)
    wheel(fig, 2, W * t10, GREEN, ghost=W * (t10 - 0.1) if t10 >= 0.1 else None)
    wheel(fig, 3, W * t2, RED, ghost=W * (t2 - 0.5) if t2 >= 0.5 else None)
    m = tf <= tc + 1e-9
    fig.add_trace(go.Scatter(x=tf[m], y=R * np.sin(W * tf[m]), mode="lines", line=dict(color=GREY, width=3)), 2, 1)
    tk = np.arange(0, t2 + 1e-9, 0.5)
    if last:
        fig.add_trace(go.Scatter(x=tf, y=R * np.sin(2 * np.pi * f_alias * tf), mode="lines",
                                 line=dict(color=RED, width=3, dash="dash")), 2, 1)
    fig.add_trace(go.Scatter(x=tk, y=R * np.sin(W * tk), mode="markers",
                             marker=dict(color=RED, size=15, line=dict(color="white", width=2))), 2, 1)
    fig.update_xaxes(range=[-0.05, T_END + 0.05], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[-6, 6], dtick=5, row=2, col=1)
    note = ("red dashes: a wave of 0.41 Hz turning backwards fits every 2 Hz sample" if last else
            "each 2 Hz sample: 286.5° forward, which looks like 73.5° backwards")
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=1000, showlegend=False,
                      margin=dict(l=80, r=30, t=150, b=80),
                      title=dict(x=0.5, y=0.97, text=f"t = {tc:.1f} s: the wheel turns 1.59 times a second"
                                                     f"<br><sup>{note}</sup>"))
    fig.update_annotations(font=dict(size=21))
    return fig


ts = np.round(np.arange(0, T_END + 1e-9, 0.1), 1)
figs = [frame(t) for t in ts] + [frame(T_END, last=True)]
make_gif(figs, here / "alias_wheel", fps=5, holds=[6] + [1] * (len(ts) - 1) + [20], keys=[6, len(figs) - 1],
         cols=1, width=800)
