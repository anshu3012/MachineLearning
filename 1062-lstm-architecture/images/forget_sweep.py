"""The forget gate of a one-unit LSTM as the input changes: f = sigmoid(2.0 h + 1.5 x + 1.0) with h = 1, and the
old long-term memory c = 2. As x slides from 1 down to -10, the gate closes and the kept memory f * c falls from
1.98 to 0. Plotly frames: a point moves along the sigmoid and a bar shrinks.
Run: python forget_sweep.py -> forget_sweep.gif, forget_sweep_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import GREEN, RED, GREY
from frames import save

WH, WX, B, H, C = 2.0, 1.5, 1.0, 1.0, 2.0
sig = lambda z: 1 / (1 + np.exp(-z))
gate = lambda x: sig(WH * H + WX * x + B)
assert round(gate(1), 3) == 0.989 and round(gate(1) * C, 2) == 1.98 and gate(-10) * C < 0.001
FONT = dict(family="Latin Modern Roman", size=22)
zs = np.linspace(-13, 6, 300)


def frame(x):
    z, f = WH * H + WX * x + B, gate(x)
    fig = make_subplots(1, 2, column_widths=[0.62, 0.38], horizontal_spacing=0.1,
                        subplot_titles=("forget gate: f = sigmoid(z)", "long-term memory"))
    fig.add_trace(go.Scatter(x=zs, y=sig(zs), mode="lines", line=dict(color=GREY, width=3)), 1, 1)
    fig.add_trace(go.Scatter(x=[z], y=[f], mode="markers+text", marker=dict(color=RED, size=18),
                             text=[f"f = {f:.2f}"], textposition="top right" if z < 0 else "top left",
                             textfont=dict(color=RED, size=22)), 1, 1)
    fig.add_trace(go.Bar(x=["old", "kept"], y=[C, f * C], marker_color=[GREY, GREEN], width=0.6,
                         text=[f"{C:.2f}", f"{f * C:.2f}"], textposition="outside", cliponaxis=False), 1, 2)
    fig.update_xaxes(title="z = 2.0 × 1 + 1.5 × x + 1.0", range=[-13, 6], row=1, col=1)
    fig.update_yaxes(range=[-0.05, 1.12], tickvals=[0, 0.5, 1], row=1, col=1)
    fig.update_yaxes(range=[0, 2.5], row=1, col=2)
    fig.update_annotations(font=dict(size=22))
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, showlegend=False,
                      title=dict(text=f"input x = {x:g}:  z = {z:g},  the gate keeps {f:.0%} of the memory", x=0.5, y=0.97),
                      margin=dict(l=60, r=20, t=110, b=80))
    return fig


if __name__ == "__main__":
    xs = [1, 0.5, 0, -0.5, -1, -1.5, -2, -2.5, -3, -4, -5, -6, -8, -10]
    figs = [frame(x) for x in xs]
    n = len(figs)
    save("forget_sweep", figs, [0] * 4 + list(range(n)) + [n - 1] * 6, [0, 4, 6, n - 1], Path(__file__).parent, fps=2.5)
