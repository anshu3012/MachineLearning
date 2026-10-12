"""The argument principle on the heading loop. f(s) = 1 + L(s) = (s^2 + 0.8 s + 4)/s^2 has zeros at the closed-loop
poles -0.4 +- 1.96j (circles) and a double pole at 0 (cross). A point s walks clockwise round a circle (left); its
image f(s) is drawn on the right, with a counter of the image's clockwise turns round the origin. Four circles: round
the zero -0.4 + 1.96j (1 turn clockwise), round the double pole (2 turns counter-clockwise, -2), round nothing (0),
round both zeros and the double pole (0 = 2 - 2).
Run: python mapping_anim.py -> mapping_anim.gif, mapping_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from loopkit import L_head

here = Path(__file__).parent
f = lambda s: 1 + L_head(s)
z1 = -0.4 + 1j * np.sqrt(4 - 0.16)
assert abs(f(z1)) < 1e-12 and abs(z1.imag - 1.96) < 5e-3
STAGES = [(z1, 0.6, "round the zero −0.4 + 1.96j", 1),
          (0j, 1.0, "round the double pole at 0", -2),
          (1.6 + 0j, 0.6, "round nothing", 0),
          (0j, 3.0, "round both zeros and the double pole", 0)]
NPT = 16
phi = np.linspace(0, 2 * np.pi, 721)


def frame(c, r, name, want, k, done_rows):
    s = c + r * np.exp(-1j * phi)                     # clockwise
    w = f(s)
    cw = -(np.unwrap(np.angle(w)) - np.angle(w[0])) / (2 * np.pi)
    if k == NPT:
        assert abs(cw[-1] - want) < 1e-9
    i = int(round(k / NPT * (len(phi) - 1)))
    R = 1.3 * max(np.abs(w).max(), 0.5)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55], horizontal_spacing=0.08,
                        subplot_titles=["s walks clockwise (o zeros of f, × its double pole)",
                                        "the image f(s) = 1 + L(s)"])
    for col, (lo, hi) in [(1, (-3.6, 3.6)), (2, (-R, R))]:
        fig.add_trace(go.Scatter(x=[lo, hi], y=[0, 0], mode="lines", line=dict(color=GREY, width=1)), 1, col)
        fig.add_trace(go.Scatter(x=[0, 0], y=[lo, hi], mode="lines", line=dict(color=GREY, width=1)), 1, col)
    fig.add_trace(go.Scatter(x=[z1.real, z1.real], y=[z1.imag, -z1.imag], mode="markers",
                             marker=dict(symbol="circle-open", size=16, color=GREEN, line=dict(width=3))), 1, 1)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(symbol="x", size=16, color=ORANGE)), 1, 1)
    fig.add_trace(go.Scatter(x=s.real, y=s.imag, mode="lines", line=dict(color=BLUE, width=1.5, dash="dot")), 1, 1)
    fig.add_trace(go.Scatter(x=s.real[:i + 1], y=s.imag[:i + 1], mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=[s.real[i]], y=[s.imag[i]], mode="markers", marker=dict(size=14, color=BLUE)), 1, 1)
    fig.add_trace(go.Scatter(x=w.real[:i + 1], y=w.imag[:i + 1], mode="lines", line=dict(color=RED, width=4)), 1, 2)
    fig.add_trace(go.Scatter(x=[0, w.real[i]], y=[0, w.imag[i]], mode="lines", line=dict(color=RED, width=2)), 1, 2)
    fig.add_trace(go.Scatter(x=[w.real[i]], y=[w.imag[i]], mode="markers", marker=dict(size=14, color=RED)), 1, 2)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=10, color="black")), 1, 2)
    done = "<br>".join(done_rows) if done_rows else ""
    if done:
        fig.add_annotation(x=0.0, y=-0.05, xref="paper", yref="paper", text="counts so far:<br>" + done.replace("-", "−"),
                           showarrow=False, xanchor="left", yanchor="top", font=dict(size=17, color=GREY))
    fig.update_xaxes(range=[-3.6, 3.6], visible=False, row=1, col=1)
    fig.update_yaxes(range=[-3.6, 3.6], visible=False, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[-R, R], title="real part", row=1, col=2)
    fig.update_yaxes(range=[-R, R], scaleanchor="x2", scaleratio=1, row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=620, showlegend=False,
                      margin=dict(l=30, r=30, t=150, b=130), title=dict(x=0.5, y=0.96, text=f"circle {name}<br><span style='font-size:20px;color:{RED}'>"
                                 f"clockwise turns of the image round 0 so far: {cw[i]:+.2f}</span>".replace("-", "−")))
    fig.update_annotations(selector=dict(xref="paper", yref="paper", showarrow=False, yanchor="bottom"), font_size=19)
    return fig, cw


figs, holds, keys, rows = [], [], [], []
for c, r, name, want in STAGES:
    for k in range(NPT + 1):
        fig, cw = frame(c, r, name, want, k, rows)
        figs.append(fig)
        holds.append(4 if k == 0 else 1)
    holds[-1] = 8
    keys.append(len(figs) - 1)
    rows = rows + [f"{name.replace('round ', '')} {want:+d}"]
figs.append(frame(*STAGES[-1][:3], STAGES[-1][3], NPT, rows)[0])
holds.append(20)
make_gif(figs, here / "mapping_anim", fps=5, holds=holds, keys=keys[:3] + [len(figs) - 1], cols=2, width=900)
