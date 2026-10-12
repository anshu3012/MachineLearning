"""The robot drives RO-001's circle (0.5 m/s, turning at 1 rad/s, radius 0.5 m) from (2, 1, 0.524) for one full
turn, 6.283 s. Left: the room seen from above, the robot's body (a disk of radius 0.25 m) with its heading arrow.
Right: the configuration space box; the point (x, y, theta) climbs as the heading turns, leaves the top face at
theta = 2 pi after 5.760 s, comes back in at the bottom face (theta = 0), and ends where it started.
Run: python circle_cspace.py -> circle_cspace.gif, circle_cspace_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from cmodel import Q0, R_BODY, TWO_PI, circle_drive, wrap
from gifkit import FONT, GREY, ORANGE, RED, make_gif
from plotly.subplots import make_subplots
from cdraw import box_edges, room

here = Path(__file__).parent
T_WRAP = TWO_PI - Q0[2]
assert round(T_WRAP, 3) == 5.760 and round(TWO_PI, 3) == 6.283
assert np.allclose(circle_drive(TWO_PI)[:2], Q0[:2])
TIMES = list(np.round(np.arange(0, 5.6, 0.4), 6)) + [5.6, T_WRAP - 0.02, T_WRAP + 0.02, 6.0, TWO_PI]


def frame(t, title):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.44, 0.56], horizontal_spacing=0.02,
                        specs=[[{"type": "xy"}, {"type": "scene"}]],
                        subplot_titles=["the room, seen from above", "configuration space: (x, y, θ)"])
    room(fig)
    ts = np.linspace(0, t, max(2, int(t / 0.05) + 1))
    q = np.array([circle_drive(s) for s in ts])
    fig.add_trace(go.Scatter(x=q[:, 0], y=q[:, 1], mode="lines", line=dict(color=ORANGE, width=3)), 1, 1)
    x, y, th = circle_drive(t)
    a = np.linspace(0, TWO_PI, 40)
    fig.add_trace(go.Scatter(x=x + R_BODY * np.cos(a), y=y + R_BODY * np.sin(a), mode="lines", fill="toself",
                             line=dict(color=RED, width=2), fillcolor="rgba(228,87,86,0.25)"), 1, 1)
    fig.add_annotation(x=x + 0.42 * np.cos(th), y=y + 0.42 * np.sin(th), ax=x, ay=y, xref="x", yref="y", axref="x",
                       ayref="y", showarrow=True, arrowhead=2, arrowsize=1.1, arrowwidth=3, arrowcolor=RED, text="")
    box_edges(fig)
    zw = wrap(q[:, 2])
    cut = np.where(np.diff(zw) < -1)[0]
    xs, ys, zs = list(q[:, 0]), list(q[:, 1]), list(zw)
    for c in cut[::-1]:                                     # break the trail where it wraps
        for arr in (xs, ys, zs):
            arr.insert(c + 1, None)
    fig.add_trace(go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color=ORANGE, width=6)), 1, 2)
    fig.add_trace(go.Scatter3d(x=[Q0[0]], y=[Q0[1]], z=[Q0[2]], mode="markers", marker=dict(size=4, color=GREY)), 1, 2)
    if t > T_WRAP:                                          # the exit at the top face and the entry at the bottom
        xw, yw, _ = circle_drive(T_WRAP)
        fig.add_trace(go.Scatter3d(x=[xw, xw], y=[yw, yw], z=[0, TWO_PI], mode="lines+markers",
                                   line=dict(color=GREY, width=3, dash="dash"), marker=dict(size=4, color=GREY)), 1, 2)
    fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[wrap(th)], mode="markers", marker=dict(size=7, color=RED)), 1, 2)
    fig.update_xaxes(range=[-0.1, 7.1], dtick=1, title="x (m)", showgrid=False, row=1, col=1)
    fig.update_yaxes(range=[-0.1, 4.1], dtick=1, title="y (m)", scaleanchor="x", row=1, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1350, height=660, showlegend=False,
                      margin=dict(l=60, r=10, t=110, b=40), title=dict(x=0.5, y=0.97, text=title),
                      scene=dict(xaxis=dict(title="x (m)", range=[0, 7], dtick=1, tickfont=dict(size=16), title_font=dict(size=19)),
                                 yaxis=dict(title="y (m)", range=[0, 4], dtick=1, tickfont=dict(size=16), title_font=dict(size=19)),
                                 zaxis=dict(title="θ (rad)", range=[0, TWO_PI], tickvals=[0, np.pi, TWO_PI],
                                            ticktext=["0", "π", "2π"], tickfont=dict(size=19), title_font=dict(size=19)),
                                 aspectmode="manual", aspectratio=dict(x=1.5, y=0.9, z=1.0),
                                 camera=dict(eye=dict(x=1.5, y=-1.9, z=0.85), center=dict(x=0, y=0, z=-0.12))))
    for a in fig.layout.annotations[:2]:
        a.font.size = 22
    return fig


figs, holds = [], []
for t in TIMES:
    x, y, th = circle_drive(t)
    if abs(t - (T_WRAP - 0.02)) < 1e-9:
        title = f"t = {t:.2f} s: θ = {wrap(th):.2f} rad, the point is about to leave the top face"
        h = 4
    elif abs(t - (T_WRAP + 0.02)) < 1e-9:
        title = f"t = {t:.2f} s: θ passed 2π and reads {wrap(th):.2f} rad: the point is back at the bottom face"
        h = 5
    elif t == TWO_PI:
        title = "t = 6.28 s: one full turn, back at (2, 1, 0.524), the point where it started"
        h = 12
    elif t == 0:
        title = "t = 0 s: the robot at (2, 1, 0.524) is one point of the box"
        h = 4
    else:
        title = f"t = {t:.1f} s: (x, y, θ) = ({x:.2f}, {y:.2f}, {wrap(th):.2f})"
        h = 1
    figs.append(frame(t, title))
    holds.append(h)
keys = [0, 7, TIMES.index(T_WRAP + 0.02), len(TIMES) - 1]
make_gif(figs, here / "circle_cspace", fps=3, holds=holds, keys=keys, cols=2, width=1000)
