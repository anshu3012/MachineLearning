"""The 2R arm moves smoothly: theta1 from 300 to 420 degrees (60 degrees after a full turn) and theta2 from 60 to 120
degrees, 10 degrees of theta1 per frame. Left: the arm. Middle: its point in the square of joint angles (each from 0
to 360 degrees). Right: its point on the torus. When theta1 passes 360 degrees the square's point jumps from the
right edge to the left edge, while the torus point moves on without a jump.
Run: python arm_wrap.py -> arm_wrap.gif, arm_wrap_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from cmodel import arm
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
RT, rt = 2.0, 0.8
TS = np.linspace(0, 1, 13)
TH1 = 300 + 120 * TS                                       # degrees, not wrapped
TH2 = 60 + 60 * TS
assert TH1[6] == 360 and TH1[-1] == 420 and TH2[-1] == 120


def torus_pt(t1, t2):
    t1, t2 = np.radians(t1), np.radians(t2)
    return ((RT + rt * np.cos(t2)) * np.cos(t1), (RT + rt * np.cos(t2)) * np.sin(t1), rt * np.sin(t2))


def frame(k, title):
    fig = make_subplots(rows=1, cols=3, column_widths=[0.26, 0.34, 0.40], horizontal_spacing=0.05,
                        specs=[[{"type": "xy"}, {"type": "xy"}, {"type": "scene"}]],
                        subplot_titles=["the arm", "the square of joint angles", "the torus"])
    t1, t2 = TH1[k], TH2[k]
    e, h = arm(np.radians(t1), np.radians(t2))
    fig.add_trace(go.Scatter(x=[-0.15, 0.15], y=[0, 0], mode="lines", line=dict(color=GREY, width=8)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, e[0]], y=[0, e[1]], mode="lines", line=dict(color=BLUE, width=9)), 1, 1)
    fig.add_trace(go.Scatter(x=[e[0], h[0]], y=[e[1], h[1]], mode="lines", line=dict(color=ORANGE, width=9)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, e[0]], y=[0, e[1]], mode="markers", marker=dict(size=13, color="white",
                                                                                  line=dict(color="black", width=2))),
                  1, 1)
    fig.add_annotation(x=0, y=-0.48, text=f"θ1 = {t1 % 360:.0f}°<br>θ2 = {t2:.0f}°", showarrow=False, align="left",
                       font=dict(size=21), row=1, col=1)
    # square: trail split where theta1 wraps
    w1 = TH1[:k + 1] % 360
    xs, ys = [], []
    for j in range(k + 1):
        if j and w1[j] < w1[j - 1]:                         # theta1 passed 360: finish at the right edge, restart left
            c = TH2[j - 1] + (360 - TH1[j - 1]) / (TH1[j] - TH1[j - 1]) * (TH2[j] - TH2[j - 1])
            xs += [360, None, 0]
            ys += [c, None, c]
        xs.append(w1[j])
        ys.append(TH2[j])
    fig.add_trace(go.Scatter(x=[0, 360, 360, 0, 0], y=[0, 0, 360, 360, 0], mode="lines",
                             line=dict(color=GREY, width=2)), 1, 2)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=RED, width=4)), 1, 2)
    fig.add_trace(go.Scatter(x=[t1 % 360], y=[t2], mode="markers", marker=dict(size=14, color=RED)), 1, 2)
    # torus
    u, v = np.meshgrid(np.linspace(0, 360, 72), np.linspace(0, 360, 36))
    X, Y, Z = torus_pt(u, v)
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, surfacecolor=np.cos(np.radians(v)) + 0.6 * np.sin(np.radians(v)),
                             cmin=-1.6, cmax=1.6, colorscale=[[0, "rgb(160,183,210)"], [1, "rgb(225,233,243)"]],
                             showscale=False, opacity=1.0, lighting=dict(ambient=1.0, diffuse=0.0, specular=0.0)),
                  1, 3)
    tt = np.linspace(0, TS[k], max(2, 8 * k))
    px, py, pz = torus_pt(300 + 120 * tt, 60 + 60 * tt)
    fig.add_trace(go.Scatter3d(x=px, y=py, z=pz + 0.02, mode="lines", line=dict(color=RED, width=7)), 1, 3)
    p = torus_pt(t1, t2)
    fig.add_trace(go.Scatter3d(x=[p[0]], y=[p[1]], z=[p[2] + 0.02], mode="markers", marker=dict(size=8, color=RED)),
                  1, 3)
    fig.update_xaxes(visible=False, range=[-0.55, 0.55], row=1, col=1)
    fig.update_yaxes(visible=False, range=[-0.62, 0.55], scaleanchor="x", row=1, col=1)
    fig.update_xaxes(range=[-5, 365], tickvals=[0, 90, 180, 270, 360], title="θ1 (degrees)", showgrid=False,
                     row=1, col=2)
    fig.update_yaxes(range=[-5, 365], tickvals=[0, 90, 180, 270, 360], title="θ2 (degrees)", scaleanchor="x2",
                     row=1, col=2)
    hide = dict(visible=False, range=[-3, 3])
    fig.update_layout(template="simple_white", font=FONT, width=1450, height=600, showlegend=False,
                      margin=dict(l=20, r=10, t=110, b=50), title=dict(x=0.5, y=0.97, text=title),
                      scene=dict(xaxis=hide, yaxis=hide, zaxis=dict(visible=False, range=[-1.6, 1.6]),
                                 aspectmode="manual", aspectratio=dict(x=1.5, y=1.5, z=0.8),
                                 camera=dict(eye=dict(x=1.55, y=-0.35, z=1.05))))
    for a in fig.layout.annotations[:3]:
        a.font.size = 21
    return fig


figs, holds = [], []
for k in range(len(TS)):
    w = TH1[k] % 360
    if k == 0:
        title = "the arm at θ1 = 300°, θ2 = 60°: one point in the square and one on the torus"
        h = 4
    elif k == 6:
        title = "θ1 passes 360° (= 0°): in the square the point jumps from the right edge to the left edge"
        h = 6
    elif k == len(TS) - 1:
        title = "θ1 = 60°, θ2 = 120°: the torus path has no jump; the square's path is cut in two"
        h = 12
    else:
        title = f"θ1 = {w:.0f}°, θ2 = {TH2[k]:.0f}°"
        h = 1
    figs.append(frame(k, title))
    holds.append(h)
make_gif(figs, here / "arm_wrap", fps=2, holds=holds, keys=[0, 5, 6, 12], cols=2, width=1000)
