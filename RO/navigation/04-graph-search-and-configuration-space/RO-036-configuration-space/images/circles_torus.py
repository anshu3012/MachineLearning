"""Two joint circles become a torus. Left: the 2R arm at (theta1, theta2) = (30, 60) degrees. Right: the angle of
joint 2 is a point on a small circle; the angle of joint 1 is a point on a big circle; at every angle of joint 1
there is a whole circle of angles of joint 2, so copies of the small circle are placed round the big one, 30 degrees
apart, until they sweep out the surface of a torus. Every point of the torus is one configuration of the arm; the
red point is (30, 60) degrees. Run: python circles_torus.py -> circles_torus.gif, circles_torus_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from cmodel import L1, L2, arm
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
RT, rt = 2.0, 0.8                                           # the torus drawn: big radius 2, small radius 0.8
T1, T2 = np.radians(30), np.radians(60)
E, Hd = arm(T1, T2)
assert np.allclose(Hd, (0.260, 0.350), atol=5e-4)


def torus_pt(t1, t2):
    return ((RT + rt * np.cos(t2)) * np.cos(t1), (RT + rt * np.cos(t2)) * np.sin(t1), rt * np.sin(t2))


def arm_panel(fig):
    fig.add_trace(go.Scatter(x=[-0.15, 0.15], y=[0, 0], mode="lines", line=dict(color=GREY, width=8)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, E[0]], y=[0, E[1]], mode="lines", line=dict(color=BLUE, width=9)), 1, 1)
    fig.add_trace(go.Scatter(x=[E[0], Hd[0]], y=[E[1], Hd[1]], mode="lines", line=dict(color=ORANGE, width=9)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, E[0]], y=[0, E[1]], mode="markers", marker=dict(size=14, color="white",
                                                                                  line=dict(color="black", width=2))),
                  1, 1)
    fig.add_annotation(x=0.1, y=-0.03, text="θ1 = 30°", showarrow=False, xanchor="left", yanchor="top",
                       font=dict(size=19, color=BLUE), row=1, col=1)
    fig.add_annotation(x=E[0] + 0.03, y=E[1] + 0.03, text="θ2 = 60°", showarrow=False, xanchor="left",
                       font=dict(size=19, color=ORANGE), row=1, col=1)


def frame(title, n_copies=0, big=False, small=True, surface=False, point=False):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.3, 0.7], horizontal_spacing=0.02,
                        specs=[[{"type": "xy"}, {"type": "scene"}]],
                        subplot_titles=["the arm", "its configurations"])
    arm_panel(fig)
    s = np.linspace(0, 2 * np.pi, 120)
    if surface:
        u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 72), np.linspace(0, 2 * np.pi, 36))
        X, Y, Z = torus_pt(u, v)
        fig.add_trace(go.Surface(x=X, y=Y, z=Z, surfacecolor=np.cos(v) + 0.6 * np.sin(v), cmin=-1.6, cmax=1.6,
                                 colorscale=[[0, "rgb(150,175,205)"], [1, "rgb(225,233,243)"]], showscale=False,
                                 opacity=1.0, lighting=dict(ambient=1.0, diffuse=0.0, specular=0.0)), 1, 2)
    if big:
        x, y, z = torus_pt(s, 0 * s)
        x, y = RT * np.cos(s), RT * np.sin(s)
        fig.add_trace(go.Scatter3d(x=x, y=y, z=0 * s, mode="lines", line=dict(color=BLUE, width=7)), 1, 2)
    for k in range(n_copies):
        x, y, z = torus_pt(np.radians(30 * k) + 0 * s, s)
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color=ORANGE, width=5)), 1, 2)
    if small and n_copies == 0:
        x, y, z = torus_pt(0 * s, s)
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color=ORANGE, width=7)), 1, 2)
    if point:
        x, y, z = torus_pt(T1 + 0 * s, s)
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color=ORANGE, width=7)), 1, 2)
        x, y, z = torus_pt(s, T2 + 0 * s)
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color=BLUE, width=7)), 1, 2)
        p = torus_pt(T1, T2)
        nrm = (np.cos(T2) * np.cos(T1), np.cos(T2) * np.sin(T1), np.sin(T2))  # outward: lift the point off
        p = [c + 0.1 * n for c, n in zip(p, nrm)]
        fig.add_trace(go.Scatter3d(x=[p[0]], y=[p[1]], z=[p[2]], mode="markers+text", marker=dict(size=10, color=RED),
                                   text=["  (30°, 60°)"], textposition="middle right", textfont=dict(size=23, color=RED)),
                      1, 2)
    fig.update_xaxes(visible=False, range=[-0.2, 0.45], row=1, col=1)
    fig.update_yaxes(visible=False, range=[-0.15, 0.45], scaleanchor="x", row=1, col=1)
    hide = dict(visible=False, range=[-3, 3])
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=640, showlegend=False,
                      margin=dict(l=10, r=10, t=110, b=10), title=dict(x=0.5, y=0.97, text=title),
                      scene=dict(xaxis=hide, yaxis=hide, zaxis=dict(visible=False, range=[-1.6, 1.6]),
                                 aspectmode="manual", aspectratio=dict(x=1.6, y=1.6, z=0.85),
                                 camera=dict(eye=dict(x=1.45, y=-0.45, z=1.1))))
    for a in fig.layout.annotations[:2]:
        a.font.size = 21
    return fig


figs, holds = [], []
figs.append(frame("joint 2's angle θ2 is a point on a circle", small=True))
holds.append(4)
figs.append(frame("joint 1's angle θ1 is a point on another circle", big=True))
holds.append(4)
for n in range(1, 13):
    figs.append(frame(f"at every θ1 there is a whole circle of θ2: copies 30° apart ({n} of 12)", n_copies=n, big=True,
                      small=False))
    holds.append(1)
holds[-1] = 3
figs.append(frame("the copies sweep out the surface of a torus", surface=True, big=False, small=False))
holds.append(4)
figs.append(frame("one point of the torus is one configuration of the arm: (θ1, θ2) = (30°, 60°)", surface=True,
                  small=False, point=True))
holds.append(12)
make_gif(figs, here / "circles_torus", fps=2, holds=holds, keys=[0, 1, 6, len(figs) - 1], cols=2, width=900)
