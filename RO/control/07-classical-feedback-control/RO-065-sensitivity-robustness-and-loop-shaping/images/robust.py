"""Robust stability of the PD heading loop against the real robot's model error: a payload (inertia 0.15 instead of
0.1 kg m^2) and a 0.25 s delay, so the true plant is P (1 + delta) with delta(jw) = (0.1/0.15) e^{-0.25 jw} - 1. Top:
the modelled Nyquist curve L (blue), the true one (orange, dashed) and, at five frequencies, the disk of radius
|L delta| round L(jw) that holds the true point; the disks at 1.7 and 2.0 rad/s cover -1. Bottom: the size of the model
error |delta| against the robustness bound 1/|T|; where |delta| is above 1/|T| (1.6 to 2.4 rad/s) the guarantee fails.
Run: python robust.py -> robust.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED
from loopkit import I, L_head
from shapekit import I_PAY, TAU_REAL

here = Path(__file__).parent


def delta(w):
    return (I / I_PAY) * np.exp(-1j * w * TAU_REAL) - 1


wn = np.logspace(np.log10(1.1), np.log10(40), 800)
L = L_head(1j * wn)
Lt = L * (1 + delta(wn))
w = np.logspace(np.log10(0.3), 1, 2000)
Lw = L_head(1j * w)
bound = np.abs(1 + Lw) / np.abs(Lw)
bad = np.abs(delta(w)) > bound
assert abs(w[bad][0] - 1.6) < 0.05 and abs(w[bad][-1] - 2.4) < 0.05
assert abs(L_head(2j) + 1) < abs(L_head(2j) * delta(2.0)), "the disk at 2 rad/s must cover -1"

fig = make_subplots(rows=2, cols=1, row_heights=[0.58, 0.42], vertical_spacing=0.13)
ang = np.linspace(0, 2 * np.pi, 200)
for wi in (1.4, 1.7, 2.0, 2.4, 3.0):
    c, r = L_head(1j * wi), abs(L_head(1j * wi) * delta(wi))
    covers = abs(c + 1) < r
    fig.add_trace(go.Scatter(x=c.real + r * np.cos(ang), y=c.imag + r * np.sin(ang), mode="lines", fill="toself",
                             fillcolor="rgba(228,87,86,0.10)" if covers else "rgba(107,107,107,0.06)",
                             line=dict(color=RED if covers else GREY, width=2), showlegend=False), 1, 1)
    fig.add_annotation(x=c.real, y=c.imag - r, text=f"{wi:g} rad/s", showarrow=False, yanchor="top", yshift=-2,
                       font=dict(size=16, color=RED if covers else GREY), row=1, col=1)
fig.add_trace(go.Scatter(x=L.real, y=L.imag, mode="lines", line=dict(color=BLUE, width=4), name="modelled L"), 1, 1)
fig.add_trace(go.Scatter(x=Lt.real, y=Lt.imag, mode="lines", line=dict(color=ORANGE, width=4, dash="dash"),
                         name="true L (payload, 0.25 s delay)"), 1, 1)
fig.add_trace(go.Scatter(x=[-1], y=[0], mode="markers", marker=dict(color=RED, size=16, symbol="x"), name="−1"), 1, 1)
fig.add_trace(go.Scatter(x=w, y=np.abs(delta(w)), line=dict(color=ORANGE, width=4), name="|δ|: size of the model error", legend="legend2"),
              2, 1)
fig.add_trace(go.Scatter(x=w, y=bound, line=dict(color=BLUE, width=4, dash="dash"), name="1/|T|: error the loop can take",
                         legend="legend2"),
              2, 1)
fig.add_vrect(x0=w[bad][0], x1=w[bad][-1], fillcolor=RED, opacity=0.12, line_width=0, row=2, col=1)
fig.add_annotation(x=np.log10(2.0), y=1.6, text="no guarantee:<br>1.6 to 2.4 rad/s", showarrow=False,
                   font=dict(size=17, color=RED), row=2, col=1)
fig.update_xaxes(title_text="real part", range=[-3.0, 0.6], row=1, col=1)
fig.update_yaxes(title_text="imaginary part", range=[-2.0, 1.3], scaleanchor="x", scaleratio=1, row=1, col=1)
fig.update_xaxes(type="log", title_text="ω (rad/s)", range=[np.log10(0.3), 1], tickvals=[0.3, 0.5, 1, 2, 3, 5, 10],
                 row=2, col=1)
fig.update_yaxes(title_text="relative size", range=[0, 2.0], row=2, col=1)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=1170, margin=dict(l=90, r=30, t=170, b=70),
                  legend=dict(x=0.02, y=0.995, yanchor="top", font=dict(size=17), bgcolor="rgba(255,255,255,0.8)"),
                  legend2=dict(x=0.02, y=0.385, yanchor="top", font=dict(size=17), bgcolor="rgba(255,255,255,0.8)"),
                  title=dict(x=0.5, y=0.97, text="PD loop and the real robot's model error:<br>"
                                                  "the disks at 1.7 and 2.0 rad/s cover −1"))
fig.write_image(here / "robust.png", scale=1)
