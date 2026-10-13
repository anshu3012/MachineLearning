"""The root locus of the PID heading loop as the integral gain Ki rises from 0 to 2 (Kp = Kd = 0.4, I = 0.1).
Left: the three closed-loop poles, the roots of 0.1 s^3 + 0.4 s^2 + 0.4 s + Ki, with the path they have traced; the
left half-plane is green, the right half-plane red. Right: the heading after the gearbox drag (0.02 N m) starts,
for the current Ki; the faint line is PD alone, which stays 0.05 rad to the right (-0.05 rad). Ki = 0: poles 0, -2, -2. Ki = 0.119: two
poles meet at -0.67. Ki = 0.2: -2.84 and -0.58 +- 0.61j, the heading is back within 0.005 rad by 4.68 s. Ki = 1.6: two
poles on the imaginary axis at +-2j, a swing that never dies. Ki = 2: they are in the right half-plane, it grows.
Run: python locus_anim.py -> locus_anim.gif, locus_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif
from tfkit import drag_response, poles

here = Path(__file__).parent
t = np.linspace(0, 20, 20001)
KIS = [0, 0.02, 0.05, 0.08, 0.1185, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
dense = np.linspace(0, 2.0, 801)
P = np.array([np.sort_complex(poles(k)) for k in dense])
pd_only = drag_response(t, 0)
assert np.allclose(np.sort(poles(0).real), [-2, -2, 0], atol=1e-6)
p = poles(0.1185)
assert np.sum(np.abs(p + 0.667) < 0.03) == 2                      # the two slow poles meet near -0.67
p = np.sort_complex(poles(0.2))
assert abs(p[0].real + 2.839) < 1e-3 and np.allclose(sorted(np.abs(p[1:].imag)), [0.606, 0.606], atol=1e-3)
p = poles(1.6)
assert np.allclose(sorted(p.imag), [-2, 0, 2], atol=1e-6) and abs(p.real.max()) < 1e-6
th = drag_response(t, 0.2)
assert abs(t[np.where(np.abs(th) > 0.005)[0][-1]] - 4.68) < 0.01


def frame(ki):
    pk = np.sort_complex(poles(ki))
    upto = dense <= ki + 1e-9
    lab = ", ".join(f"{z.real:.2f}" if abs(z.imag) < 1e-6 else f"{z.real:.2f} ± {abs(z.imag):.2f}j"
                    for z in pk if z.imag >= -1e-6)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55], horizontal_spacing=0.1,
                        subplot_titles=[f"poles: {lab}", "heading after the gearbox drag starts (right is −)"])
    fig.add_trace(go.Scatter(x=[-4.6, 0, 0, -4.6, -4.6], y=[-3, -3, 3, 3, -3], fill="toself", mode="lines",
                             line=dict(width=0), fillcolor="rgba(84,162,75,0.13)"), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 0.8, 0.8, 0, 0], y=[-3, -3, 3, 3, -3], fill="toself", mode="lines",
                             line=dict(width=0), fillcolor="rgba(228,87,86,0.15)"), 1, 1)
    fig.add_trace(go.Scatter(x=[-4.6, 0.8], y=[0, 0], mode="lines", line=dict(color="black", width=1.5)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 0], y=[-3, 3], mode="lines", line=dict(color="black", width=1.5)), 1, 1)
    if upto.sum() > 1:
        tr = P[upto].ravel()
        fig.add_trace(go.Scatter(x=tr.real, y=tr.imag, mode="markers", marker=dict(color=BLUE, size=3, opacity=0.5)),
                      1, 1)
    fig.add_trace(go.Scatter(x=pk.real, y=pk.imag, mode="markers",
                             marker=dict(symbol="x", size=20, color=RED, line=dict(width=2))), 1, 1)
    if ki >= 1.6:
        fig.add_annotation(x=0, y=2, text="Ki = 1.6: ±2j", ax=-70, ay=-30, arrowcolor=RED,
                           font=dict(color=RED, size=18), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=pd_only, mode="lines", line=dict(color=GREY, width=2, dash="dot")), 1, 2)
    fig.add_annotation(x=3.5, y=-0.05, text="PD alone", showarrow=False, xanchor="left", yanchor="top",
                       font=dict(color=GREY, size=17), row=1, col=2)
    fig.add_trace(go.Scatter(x=[0, 20], y=[0, 0], mode="lines", line=dict(color=GREY, width=1.5, dash="dash")), 1, 2)
    col = GREEN if ki < 1.6 else RED
    fig.add_trace(go.Scatter(x=t, y=drag_response(t, ki), mode="lines", line=dict(color=col, width=4)), 1, 2)
    fig.update_xaxes(range=[-4.6, 0.8], title="real part", row=1, col=1)
    fig.update_yaxes(range=[-3, 3], title="imaginary part", row=1, col=1)
    fig.update_xaxes(range=[0, 20], title="time t (s)", row=1, col=2)
    fig.update_yaxes(range=[-0.13, 0.13], title="heading θ (rad)", row=1, col=2)
    state = "stable" if ki < 1.6 - 1e-9 else "marginally stable" if abs(ki - 1.6) < 1e-9 else "unstable"
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=620, showlegend=False,
                      margin=dict(l=70, r=30, t=140, b=70),
                      title=dict(x=0.5, y=0.96, text=f"root locus: integral gain Ki = {ki:g} N·m/(rad·s), {state}"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=21)
    return fig


figs = [frame(k) for k in KIS]
holds = [10 if k in (0, 0.1185, 0.2, 1.6) else 4 for k in KIS]
holds[-1] = 30
make_gif(figs, here / "locus_anim", fps=4, holds=holds, keys=[0, 4, 6, 11, 14, 16], cols=2, width=900)
