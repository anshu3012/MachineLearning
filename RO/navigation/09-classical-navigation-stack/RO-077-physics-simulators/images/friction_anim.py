"""Friction holding, then slipping: the box of the running example at rest on the soft floor, pushed sideways with a
force that grows by 2 N every second, one frame per 0.1 s for 3 s (time step 0.002 s). Top: the box, the push
(orange), the friction (purple), the floor's push up (grey), and the friction cone at the contact: all the contact
forces the floor can give lie inside it, half-angle 21.8 degrees (tan = 0.4). The floor's total force (black) stays
inside the cone while the box holds and lies on its edge once it slips, at 1.966 s, when the push passes
0.4 x 9.81 = 3.92 N. Bottom: push and friction against time. Arrows: 1 N is drawn 0.03 m long.
Run -> friction_anim.gif, friction_anim_frames.png"""
import math

import numpy as np
import plotly.graph_objects as go
import simkit as s
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif
from plotly.subplots import make_subplots

R = s.push_test()
t, x, z, vx, vz, N, f, d = R.T
k_slip = int(np.argmax(np.abs(vx) > 0))
assert round(t[k_slip], 3) == 1.966 and round(s.MU * s.M * s.G, 2) == 3.92
assert round(math.degrees(math.atan(s.MU)), 1) == 21.8
SC = 0.03                                      # m of arrow per N
CONE = math.atan(s.MU)


def arrow(fig, x0, y0, dx, dy, col, row=1, width=3):
    fig.add_annotation(x=x0 + dx, y=y0 + dy, ax=x0, ay=y0, xref=f"x{row}", yref=f"y{row}", axref=f"x{row}",
                       ayref=f"y{row}", showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=width,
                       arrowcolor=col, text="")


def frame(tq):
    k = int(np.argmin(np.abs(t - tq)))
    fig = make_subplots(rows=2, cols=1, row_heights=[0.5, 0.5], vertical_spacing=0.1)
    xb = x[k]
    fig.add_trace(go.Scatter(x=[-0.3, 0.8, 0.8, -0.3], y=[0, 0, -0.06, -0.06], fill="toself",
                             fillcolor="rgba(150,150,150,0.3)", mode="none"), row=1, col=1)
    fig.add_shape(type="rect", x0=xb - 0.1, x1=xb + 0.1, y0=0, y1=0.2, line=dict(color=BLUE, width=4),
                  fillcolor="rgba(76,120,168,0.08)", row=1, col=1)
    L = 0.42
    for sgn in (-1, 1):
        fig.add_trace(go.Scatter(x=[xb, xb + sgn * L * math.sin(CONE)], y=[0, L * math.cos(CONE)], mode="lines",
                                 line=dict(color=GREY, width=2, dash="dash")), row=1, col=1)
    F = 2.0 * t[k]
    fr = f[k]
    arrow(fig, xb - 0.1 - F * SC, 0.1, F * SC, 0, ORANGE)
    arrow(fig, xb, 0, fr * SC, 0, PURPLE)
    arrow(fig, xb, 0, 0, N[k] * SC, GREY)
    arrow(fig, xb, 0, fr * SC, N[k] * SC, "black", width=2)
    for tx, ty, txt, col, anc in ((xb - 0.1 - F * SC, 0.13, "push", ORANGE, "left"),
                                  (xb + fr * SC, -0.035, "friction", PURPLE, "right"),
                                  (xb + 0.01, N[k] * SC + 0.015, "floor's push up", GREY, "left"),
                                  (xb + fr * SC - 0.01, N[k] * SC + 0.015, "total", "black", "right")):
        fig.add_annotation(x=tx, y=ty, xref="x", yref="y", text=txt, showarrow=False, xanchor=anc,
                           font=dict(size=15, color=col))
    slipping = abs(vx[k]) > 0
    state = "<b>slipping</b>: friction at its limit, 3.92 N" if slipping else "<b>holding</b>: friction = push"
    lines = [f"<b>t = {t[k]:.1f} s</b>: push {F:.2f} N", f"friction {abs(fr):.2f} N, limit 0.4 × 9.81 = 3.92 N",
             state, f"speed {vx[k]:.3f} m/s"]
    fig.add_annotation(x=0.05, y=6.25, xref="x2", yref="y2", text="<br>".join(lines), showarrow=False,
                       xanchor="left", yanchor="top", align="left", font=dict(size=18),
                       bgcolor="rgba(255,255,255,0.9)")
    fig.add_annotation(x=xb + L * math.sin(CONE), y=L * math.cos(CONE), xref="x", yref="y", text="friction cone",
                       showarrow=False, xanchor="left", font=dict(size=16, color=GREY))
    fig.update_xaxes(range=[-0.3, 0.8], row=1, col=1, visible=False)
    fig.update_yaxes(range=[-0.06, 0.46], row=1, col=1, visible=False, scaleanchor="x")
    sel = t <= t[k] + 1e-9
    fig.add_trace(go.Scatter(x=t[sel], y=np.abs(f[sel]), mode="lines", line=dict(color=PURPLE, width=7)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=t[sel], y=2.0 * t[sel], mode="lines", line=dict(color=ORANGE, width=2.5)), row=2, col=1)
    fig.add_trace(go.Scatter(x=[0, 3], y=[3.924, 3.924], mode="lines", line=dict(color=GREY, width=1.5, dash="dash")),
                  row=2, col=1)
    fig.add_annotation(x=2.95, y=4.2, xref="x2", yref="y2", text="limit μ m g = 3.92 N", showarrow=False,
                       xanchor="right", font=dict(size=16, color=GREY))
    fig.add_annotation(x=2.6, y=5.75, xref="x2", yref="y2", text="push", showarrow=False, xanchor="right",
                       font=dict(size=17, color=ORANGE))
    fig.add_annotation(x=2.95, y=3.4, xref="x2", yref="y2", text="friction", showarrow=False, xanchor="right",
                       font=dict(size=17, color=PURPLE))
    fig.update_xaxes(title_text="time (s)", range=[0, 3.05], row=2, col=1, showgrid=False)
    fig.update_yaxes(title_text="force (N)", range=[0, 6.3], row=2, col=1, showgrid=False)
    fig.update_layout(template="simple_white", font=FONT, width=820, height=1150, showlegend=False,
                      margin=dict(l=90, r=20, t=20, b=60))
    return fig


ts = [round(v, 1) for v in np.arange(0, 3.0 + 1e-9, 0.1)]
figs = [frame(v) for v in ts]
holds = [4] + [1] * (len(ts) - 2) + [14]
holds[ts.index(2.0)] = 5
make_gif(figs, "friction_anim", fps=4, holds=holds, keys=[ts.index(1.0), ts.index(2.0), len(ts) - 1], cols=3)
