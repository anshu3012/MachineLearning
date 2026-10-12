"""Animation: the moment of inertia. Two robots, seen from above, each turned by the same torque, 0.2 N m (right
wheel pushed 1 N forward, left wheel 1 N back, each 0.1 m from the centre), for 1 s from rest. Left: the robot alone,
moment of inertia 0.1 kg m^2: angular acceleration 2 rad/s^2, after 1 s turning at 2 rad/s and turned 1 rad (57.3
degrees). Right: the same robot with two 1.25 kg weights 0.2 m either side of its centre, 0.2 kg m^2: 1 rad/s^2, 1 rad/s
and 0.5 rad (28.6 degrees). One frame per 0.05 s; the last frame holds. Run -> inertia_anim.gif, inertia_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import headkit as h
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
CASES = [(h.I, "robot alone: I = 0.1 kg m²", False), (0.2, "with two 1.25 kg weights: I = 0.2 kg m²", True)]
assert h.spin_up(inertia=0.1) == (2.0, 2.0, 1.0) and h.spin_up(inertia=0.2) == (1.0, 1.0, 0.5)
assert abs(2 * 1.25 * 0.2 ** 2 - 0.1) < 1e-12


def rot(pts, th):
    c, s = np.cos(th), np.sin(th)
    p = np.array(pts, dtype=float)
    return c * p[:, 0] - s * p[:, 1], s * p[:, 0] + c * p[:, 1]


def frame(t, final=False):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06, subplot_titles=[c[1] for c in CASES])
    for col, (inertia, _, loaded) in enumerate(CASES, start=1):
        al = h.TAU_MAX / inertia
        th, w = 0.5 * al * t * t, al * t
        body = [(-0.15, -0.15), (0.15, -0.15), (0.15, 0.15), (-0.15, 0.15), (-0.15, -0.15)]
        bx, by = rot(body, th)
        fig.add_trace(go.Scatter(x=bx, y=by, mode="lines", fill="toself", fillcolor="rgba(76,120,168,0.18)",
                                 line=dict(color=BLUE, width=3), showlegend=False), row=1, col=col)
        for sgn in (1, -1):                                     # wheels, 0.1 m either side
            wx, wy = rot([(-0.05, sgn * 0.09), (0.05, sgn * 0.09), (0.05, sgn * 0.12), (-0.05, sgn * 0.12),
                          (-0.05, sgn * 0.09)], th)
            fig.add_trace(go.Scatter(x=wx, y=wy, mode="lines", fill="toself", fillcolor="black",
                                     line=dict(color="black"), showlegend=False), row=1, col=col)
            fx, fy = rot([(0, sgn * 0.105), (sgn * 0.12, sgn * 0.105)], th)   # right wheel forward, left back
            fig.add_trace(go.Scatter(x=fx, y=fy, mode="lines+markers", line=dict(color=ORANGE, width=4),
                                     marker=dict(symbol="arrow", size=[0, 14], angleref="previous", color=ORANGE),
                                     showlegend=False), row=1, col=col)
        if loaded:
            for sgn in (1, -1):
                lx, ly = rot([(sgn * 0.2 - 0.035, -0.035), (sgn * 0.2 + 0.035, -0.035), (sgn * 0.2 + 0.035, 0.035),
                              (sgn * 0.2 - 0.035, 0.035), (sgn * 0.2 - 0.035, -0.035)], th)
                fig.add_trace(go.Scatter(x=lx, y=ly, mode="lines", fill="toself", fillcolor=PURPLE,
                                         line=dict(color=PURPLE), showlegend=False), row=1, col=col)
        hx, hy = rot([(0, 0), (0.33, 0)], th)                  # heading arrow
        fig.add_trace(go.Scatter(x=hx, y=hy, mode="lines+markers", line=dict(color="black", width=3),
                                 marker=dict(symbol="arrow", size=[0, 16], angleref="previous", color="black"),
                                 showlegend=False), row=1, col=col)
        a = np.linspace(0, th, 40)                              # angle turned so far
        fig.add_trace(go.Scatter(x=0.42 * np.cos(a), y=0.42 * np.sin(a), mode="lines",
                                 line=dict(color=GREY, width=3, dash="dot"), showlegend=False), row=1, col=col)
        fig.add_trace(go.Scatter(x=[0, 0.45], y=[0, 0], mode="lines", line=dict(color=GREY, width=1.5),
                                 showlegend=False), row=1, col=col)
        txt = (f"angular acceleration {al:.0f} rad/s²<br>turn rate {w:.2f} rad/s<br>"
               f"turned {th:.3f} rad = {np.degrees(th):.1f}°")
        fig.add_annotation(x=0, y=-0.56, text=txt, showarrow=False, font=dict(size=19), row=1, col=col)
        fig.update_xaxes(range=[-0.55, 0.55], visible=False, row=1, col=col)
        fig.update_yaxes(range=[-0.75, 0.55], visible=False, scaleanchor="x" if col == 1 else "x2", row=1, col=col)
    title = ("after 1 s: twice the inertia, half the angular acceleration and half the turn" if final else
             f"the same torque, 0.2 N m, on both: t = {t:.2f} s")
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=720, margin=dict(l=20, r=20, t=110, b=20),
                      title=dict(text=title, x=0.5, y=0.96, font=dict(size=21)))
    for a in fig.layout.annotations[:2]:
        a.font.size = 19
    return fig


times = list(np.round(np.arange(0, 1.0001, 0.05), 2))
figs = [frame(t) for t in times] + [frame(1.0, final=True)]
make_gif(figs, here / "inertia_anim", fps=8, holds=[10] + [2] * (len(times) - 1) + [30],
         keys=[0, 10, len(figs) - 1], cols=2, width=900)
