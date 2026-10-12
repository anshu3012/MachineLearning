"""The basic motion planning problem on the room: move the robot from q_start = (2, 1, 0.524) to q_goal =
(3.6, 4.0, 1.081), its centre at the doorway centre, without touching an obstacle. The motion (the drive of RO-037):
turn on the spot from 30 to 61.93 degrees, then drive 3.4 m straight to (3.6, 4.0). Left: the room seen from above.
Right: the same motion as a path in the configuration space box: the turn moves the point straight up, the drive
moves it level. The centre's path keeps 0.382 m from every obstacle, so the 0.25 m body clears them by 0.132 m.
Run: python plan_cspace.py -> plan_cspace.gif, plan_cspace_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from cdraw import box_edges, room
from cmodel import Q0, R_BODY, TH_GOAL, TWO_PI, WAY, clearance, plan_configs
from gifkit import FONT, GREEN, GREY, ORANGE, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
CFG, LEGS = plan_configs(n_turn=6, n_drive=14)
assert np.allclose(np.round(np.degrees(LEGS), 2), [61.93]) and round(clearance(), 3) == 0.382
assert round(float(np.hypot(1.6, 3.0)), 3) == 3.4 and round(float(TH_GOAL), 3) == 1.081
assert all(0 <= c[2] < TWO_PI for c in CFG)                     # the heading never wraps on this path
Q = np.array([c[:3] for c in CFG])


def frame(k, title):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.44, 0.56], horizontal_spacing=0.02,
                        specs=[[{"type": "xy"}, {"type": "scene"}]],
                        subplot_titles=["the room, seen from above", "configuration space: (x, y, θ)"])
    room(fig)
    fig.add_trace(go.Scatter(x=Q[:k + 1, 0], y=Q[:k + 1, 1], mode="lines", line=dict(color=ORANGE, width=3)), 1, 1)
    x, y, th = Q[k]
    a = np.linspace(0, TWO_PI, 40)
    fig.add_trace(go.Scatter(x=x + R_BODY * np.cos(a), y=y + R_BODY * np.sin(a), mode="lines", fill="toself",
                             line=dict(color=RED, width=2), fillcolor="rgba(228,87,86,0.25)"), 1, 1)
    fig.add_annotation(x=x + 0.42 * np.cos(th), y=y + 0.42 * np.sin(th), ax=x, ay=y, xref="x", yref="y", axref="x",
                       ayref="y", showarrow=True, arrowhead=2, arrowsize=1.1, arrowwidth=3, arrowcolor=RED, text="")
    box_edges(fig)
    fig.add_trace(go.Scatter3d(x=Q[:k + 1, 0], y=Q[:k + 1, 1], z=Q[:k + 1, 2], mode="lines",
                               line=dict(color=ORANGE, width=7)), 1, 2)
    fig.add_trace(go.Scatter3d(x=[Q0[0], WAY[-1][0]], y=[Q0[1], WAY[-1][1]], z=[Q0[2], TH_GOAL], mode="markers",
                               marker=dict(size=6, color=[GREY, GREEN])), 1, 2)
    if k < len(CFG) - 1:                                       # in the last frame the green goal point shows
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[th], mode="markers", marker=dict(size=7, color=RED)), 1, 2)
    ax = dict(tickfont=dict(size=16), title_font=dict(size=19))
    fig.update_xaxes(range=[-0.1, 7.1], dtick=1, title="x (m)", showgrid=False, row=1, col=1)
    fig.update_yaxes(range=[-0.1, 4.1], dtick=1, title="y (m)", scaleanchor="x", row=1, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1350, height=660, showlegend=False,
                      margin=dict(l=60, r=10, t=110, b=40), title=dict(x=0.5, y=0.97, text=title),
                      scene=dict(xaxis=dict(title="x (m)", range=[0, 7], dtick=1, **ax),
                                 yaxis=dict(title="y (m)", range=[0, 4.2], dtick=1, **ax),
                                 zaxis=dict(title="θ (rad)", range=[0, TWO_PI], tickvals=[0, np.pi, TWO_PI],
                                            ticktext=["0", "π", "2π"], tickfont=dict(size=19),
                                            title_font=dict(size=19)),
                                 aspectmode="manual", aspectratio=dict(x=1.5, y=0.9, z=1.0),
                                 camera=dict(eye=dict(x=1.2, y=-2.0, z=0.7), center=dict(x=0, y=0, z=-0.12))))
    for an in fig.layout.annotations[:2]:
        an.font.size = 22
    return fig


figs, holds = [], []
for k, (x, y, th, kind) in enumerate(CFG):
    deg = np.degrees(th)
    if k == 0:
        title, h = "q<sub>start</sub> = (2, 1, 0.524): the robot at the start is one point (grey)", 4
    elif k == len(CFG) - 1:
        title, h = "q<sub>goal</sub> = (3.6, 4.0, 1.081) reached (green): the motion is one path in the box", 12
    elif kind == "turn":
        title, h = f"turn on the spot, θ = {deg:.1f}°: the point moves straight up", 1
    else:
        title, h = f"drive straight, (x, y) = ({x:.2f}, {y:.2f}): θ stays, the point moves level", 1
    figs.append(frame(k, title))
    holds.append(h)
keys = [0, 6, 13, len(CFG) - 1]
make_gif(figs, here / "plan_cspace", fps=3, holds=holds, keys=keys, cols=2, width=1000)
