"""The three margins of the heading loop with a 0.1 s delay, L(s) = (0.8 s + 4) e^{-0.1 s}/s^2, read off its Nyquist
plot (omega > 0 only, true scale). Stage 1, gain: the whole curve is scaled up until the point where it crosses the
negative real axis (omega = 11.66 rad/s, at -0.0747) reaches -1: gain margin 13.4. Stage 2, phase: the curve is turned
clockwise until the point where it crosses the circle of radius 1 (omega = 2.08 rad/s, angle -169.3 degrees) reaches
-1: phase margin 10.7 degrees. Stage 3, delay: extra delay turns each point by omega x delay; at 0.09 s the same point
reaches -1: delay margin 0.09 s. Run: python margins_anim.py -> margins_anim.gif, margins_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from loopkit import L_head, deg, margins

here = Path(__file__).parent
TAU = 0.1
L = lambda s: L_head(s, TAU)
m = margins(L)
GM, PM, DM, WGC, WPC = m["gm"], m["pm"], m["dm"], m["wgc"], m["wpc"]
assert abs(GM - 13.4) < 0.05 and abs(20 * np.log10(GM) - 22.5) < 0.05 and abs(WPC - 11.66) < 0.005
assert abs(PM - 10.7) < 0.05 and abs(WGC - 2.08) < 5e-3 and abs(DM - 0.09) < 5e-3
assert abs(abs(L(1j * WPC)) - 0.0747) < 5e-5 and abs(deg(L(1j * WGC)) + 169.3) < 0.05
w = np.logspace(-0.6, 3, 3000)
a = np.linspace(0, 2 * np.pi, 361)


def frame(z, head, readout, col, marks, last=False):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.cos(a), y=np.sin(a), mode="lines", line=dict(color=GREY, width=1.5, dash="dot")))
    fig.add_trace(go.Scatter(x=[-2.4, 1.4], y=[0, 0], mode="lines", line=dict(color=GREY, width=1)))
    fig.add_trace(go.Scatter(x=[0, 0], y=[-1.7, 1.2], mode="lines", line=dict(color=GREY, width=1)))
    fig.add_trace(go.Scatter(x=(L(1j * w)).real, y=(L(1j * w)).imag, mode="lines",
                             line=dict(color=BLUE, width=2), opacity=0.35))
    fig.add_trace(go.Scatter(x=z.real, y=z.imag, mode="lines", line=dict(color=col, width=4)))
    for p, c in marks:
        fig.add_trace(go.Scatter(x=[p.real], y=[p.imag], mode="markers", marker=dict(size=14, color=c)))
    fig.add_trace(go.Scatter(x=[-1], y=[0], mode="markers", marker=dict(symbol="x", size=18, color=RED)))
    fig.add_annotation(x=-1, y=0, text="−1", showarrow=False, yshift=-24, xshift=-12, font=dict(color=RED, size=20))
    fig.add_annotation(x=0.72, y=0.72, text="radius 1", showarrow=False, xanchor="left", font=dict(color=GREY, size=17))
    fig.add_annotation(x=0.5, y=1.0, xref="paper", yref="paper", text=readout.replace("-", "−"), showarrow=False,
                       yanchor="bottom",
                       font=dict(size=20, color=col))
    if last:
        fig.add_annotation(x=0.02, y=0.02, xref="paper", yref="paper", showarrow=False, xanchor="left",
                           yanchor="bottom", align="left", font=dict(size=19, color="black"),
                           text=f"gain margin {GM:.1f} ({20 * np.log10(GM):.1f} dB)<br>phase margin {PM:.1f}°"
                                f"<br>delay margin {DM:.2f} s")
    fig.update_xaxes(range=[-2.4, 1.4], title="real part")
    fig.update_yaxes(range=[-1.7, 1.2], title="imaginary part", scaleanchor="x", scaleratio=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=880, showlegend=False,
                      margin=dict(l=90, r=30, t=170, b=80), title=dict(x=0.5, y=0.96, text=head))
    return fig


pc, gc = L(1j * WPC), L(1j * WGC)
base = L(1j * w)
figs, holds = [], []
figs.append(frame(base, "delay 0.1 s: how far is the curve from −1?", "ω > 0 part of the Nyquist plot", BLUE,
                  [(pc, GREEN), (gc, PURPLE)]))
holds.append(8)
for k in np.geomspace(1, GM, 9)[1:]:
    figs.append(frame(k * base, "1. gain margin: scale the whole curve up", f"gain × {k:.2f}: green point at "
                      f"{(k * pc).real:.3f}", GREEN, [(k * pc, GREEN)]))
    holds.append(1)
holds[-1] = 8
for ph in np.linspace(0, PM, 7)[1:]:
    r = base * np.exp(-1j * np.radians(ph))
    figs.append(frame(r, "2. phase margin: turn the curve clockwise", f"extra lag {ph:.1f}°: purple point at angle "
                      f"{deg(gc) - ph:.1f}°", PURPLE, [(gc * np.exp(-1j * np.radians(ph)), PURPLE)]))
    holds.append(1)
holds[-1] = 8
for d in np.linspace(0, DM, 7)[1:]:
    r = L_head(1j * w, TAU + d)
    figs.append(frame(r, "3. delay margin: add delay, fast points turn more", f"extra delay {d:.3f} s: purple point "
                      f"at angle {deg(gc) - np.degrees(WGC * d):.1f}°", ORANGE,
                      [(L_head(1j * WGC, TAU + d), PURPLE)]))
    holds.append(1)
figs.append(frame(base, "the three margins of the heading loop with a 0.1 s delay", "each one alone brings the curve "
                  "to −1", BLUE, [(pc, GREEN), (gc, PURPLE)], last=True))
holds.append(16)
n1, n2 = 9, 15
make_gif(figs, here / "margins_anim", fps=3, holds=holds, keys=[0, n1 - 1, n2 - 1, len(figs) - 2, len(figs) - 1][1:],
         cols=2, width=800)
