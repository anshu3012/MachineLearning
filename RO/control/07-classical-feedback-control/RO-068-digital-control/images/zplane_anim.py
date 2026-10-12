"""Poles of the sampled speed loop as the sample period T grows from 0.01 s to 2 s, one T per frame. Left: the z-plane
with the unit circle; the two poles of the loop (red dots, their paths so far as red lines) and, for comparison, the
continuous loop's poles at -0.575 and -2.175 rad/s sent through z = e^(sT) (hollow blue circles). Both red poles slide
left along the real axis; the faster one passes 0 near T = 0.5 s (0.706 and 0.002 at 2 Hz), and leaves the circle
through -1 at T = 1.1175 s; at T = 2 s (0.5 Hz) it is at -2.029. Right: the speed step response sampled every T; the
speed axis zooms out from T = 1.2 s on, because the swings outgrow it.
Run: python zplane_anim.py -> zplane_anim.gif, zplane_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from digikit import loop_poles, sampled_loop
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
TS = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1175, 1.2, 1.4, 1.6, 1.8, 2.0]
S_CONT = (-0.5746, -2.1754)                      # the continuous loop's poles, rad/s
P = {T: np.sort(loop_poles(T).real)[::-1] for T in TS}       # both poles are real here: slow one first
assert all(abs(loop_poles(T).imag).max() < 1e-12 for T in TS)
assert np.allclose(P[0.01], [0.9943, 0.9783], atol=5e-5) and np.allclose(P[0.1], [0.9423, 0.7861], atol=5e-5)
assert np.allclose(P[0.5], [0.7057, 0.0017], atol=5e-5) and np.allclose(P[1.0], [0.3950, -0.8282], atol=5e-5)
assert abs(P[1.1175][1] + 1) < 5e-4 and np.allclose(P[2.0], [-0.2989, -2.0293], atol=5e-5)
RUNS = {T: sampled_loop(1 / T, T=12.0) for T in TS}
th = np.linspace(0, 2 * np.pi, 361)


def label(T):
    hz = 1 / T
    return f"{T:g} s ({hz:.3g} Hz)"


def frame(i, last=False):
    T = TS[i]
    fig = make_subplots(rows=1, cols=2, column_widths=[0.52, 0.48], horizontal_spacing=0.11,
                        subplot_titles=["z-plane: poles of the sampled loop", "speed after the step"])
    fig.add_trace(go.Scatter(x=np.cos(th), y=np.sin(th), mode="lines", line=dict(color="black", width=2)), 1, 1)
    fig.add_trace(go.Scatter(x=[-2.3, 1.3], y=[0, 0], mode="lines", line=dict(color=GREY, width=1)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 0], y=[-1.3, 1.3], mode="lines", line=dict(color=GREY, width=1)), 1, 1)
    for j in (0, 1):
        path = [P[t][j] for t in TS[:i + 1]]
        fig.add_trace(go.Scatter(x=path, y=[0] * len(path), mode="lines",
                                 line=dict(color=RED, width=2)), 1, 1)
    fig.add_trace(go.Scatter(x=[np.exp(s * T) for s in S_CONT], y=[0, 0], mode="markers",
                             marker=dict(color="white", size=17, line=dict(color=BLUE, width=3))), 1, 1)
    fig.add_trace(go.Scatter(x=P[T], y=[0, 0], mode="markers", marker=dict(color=RED, size=14)), 1, 1)
    fig.add_annotation(x=-2.25, y=-1.15, xref="x", yref="y", showarrow=False, text="unit circle: distance 1",
                       font=dict(size=17), xanchor="left")
    r = RUNS[T]
    fig.add_hline(y=0.5, line=dict(color="black", width=1, dash="dot"), row=1, col=2)
    fig.add_trace(go.Scatter(x=r["t"], y=r["v"], mode="lines", line=dict(color=RED, width=3)), 1, 2)
    if T >= 0.1:
        fig.add_trace(go.Scatter(x=r["tk"], y=r["yk"], mode="markers", marker=dict(color=RED, size=9)), 1, 2)
    fig.update_xaxes(range=[-2.3, 1.3], scaleanchor="y", scaleratio=1, title="real part", row=1, col=1)
    fig.update_yaxes(range=[-1.3, 1.3], title="imaginary part", row=1, col=1)
    fig.update_xaxes(range=[0, 12], title="time since the command (s)", row=1, col=2)
    zoom = T >= 1.2
    fig.update_yaxes(range=[-0.3, 1.3] if zoom else [0.35, 0.65], title="speed (m/s)", row=1, col=2)
    a, b = P[T]
    worst = max(abs(a), abs(b))
    text = f"sample period T = {label(T)}: poles {a:.3f} and {b:.3f}, farthest {worst:.3f} from 0".replace("-", "−")
    if last:
        sub = "outside the circle each tick multiplies by −2.03: the speed swings until the 4 N limit holds it"
    elif zoom:
        sub = "a pole outside the circle: the swings grow; the speed axis is zoomed out"
    else:
        sub = "red: the loop's poles; hollow blue: where the continuous poles would land"
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=640, showlegend=False,
                      margin=dict(l=90, r=30, t=150, b=80),
                      title=dict(x=0.5, y=0.96, text=f"{text}<br><span style='font-size:18px'>{sub}</span>",
                                 font=dict(size=21)))
    fig.update_annotations(font=dict(size=20))
    return fig


figs = [frame(i) for i in range(len(TS))] + [frame(len(TS) - 1, last=True)]
holds = [3 if T in (0.01, 0.1, 0.5, 1.1175) else 1 for T in TS] + [8]
make_gif(figs, here / "zplane_anim", fps=2, holds=holds, keys=[TS.index(0.1), TS.index(0.5), TS.index(1.1175),
                                                             len(figs) - 1], cols=2, width=900)
