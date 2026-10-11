"""The robot of Section 4.2 turning about its ICC for 1 s. Wheel speeds 0.6 and 0.4 m/s, wheel separation L = 0.2 m:
omega = (0.6 - 0.4)/0.2 = 1 rad/s, v = 0.5 m/s, so the ICC lies R = v/omega = 0.5 m to the robot's left.
Start pose (0, 0, 0), ICC (0, 0.5). Right wheel, midpoint and left wheel sit 0.6, 0.5 and 0.4 m from the ICC; all turn
by the same angle, so after 1 s (1 rad) their arcs are 0.6, 0.5 and 0.4 m. Arrows: the three speeds, drawn at half
length. Faint: the start pose.
Run: python icc_turn.py -> icc_turn.gif, icc_turn_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from robotdraw import L, robot, step

here = Path(__file__).parent
VR, VL = 0.6, 0.4
V, W = (VR + VL) / 2, (VR - VL) / L
R = V / W
ICC = np.array([0.0, R])
POINTS = [("right wheel", -L / 2, VR, "v<sub>R</sub>", RED), ("midpoint", 0.0, V, "v", ORANGE),
          ("left wheel", L / 2, VL, "v<sub>L</sub>", PURPLE)]          # offset to the robot's left, speed, colour
assert np.isclose(W, 1) and np.isclose(V, 0.5) and np.isclose(R, 0.5)

q = (0.0, 0.0, 0.0)                                                 # the kinematic model, fine steps, for 1 s
for _ in range(10000):
    q = step(q, V, W, 1e-4)
assert np.allclose(q, (R * np.sin(1), R - R * np.cos(1), 1), atol=1e-4)  # it lands on the circle about the ICC


def place(phi, off):
    """World position of the point `off` to the robot's left, after the robot has turned phi about the ICC."""
    return ICC + (R - off) * np.array([np.sin(phi), -np.cos(phi)])


grid = np.linspace(0, 1, 1001)
for _, off, spd, _, _ in POINTS:                                     # arc after 1 s = distance x 1 rad = speed x 1 s
    pts = np.array([place(g, off) for g in grid])
    assert np.isclose(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum(), spd, atol=1e-5)


def arc(r, a0, a1, n=60):
    t = np.linspace(a0, a1, n)
    return ICC[0] + r * np.cos(t), ICC[1] + r * np.sin(t)


def frame(phi):
    fig = go.Figure()
    for d in (0.6, 0.5, 0.4):                                        # each point's circle about the ICC
        x, y = arc(d, 0, 2 * np.pi, 200)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=GREY, width=2, dash="dash"), opacity=0.5))
    fig.add_trace(go.Scatter(x=[0, 0], y=[-0.2, 0.62], mode="lines", line=dict(color=GREY, width=2), opacity=0.35))
    for tr in robot((0, 0, 0), opacity=0.25, arrow=False):
        fig.add_trace(tr)
    # distances from the ICC, measured at the start pose
    for xa, off, lab, col in ((-0.17, 0.1, "R − L/2 = 0.4", PURPLE), (-0.31, 0.0, "R = 0.5", ORANGE),
                              (-0.45, -0.1, "R + L/2 = 0.6", RED)):
        fig.add_trace(go.Scatter(x=[xa, -0.04], y=[off, off], mode="lines", line=dict(color=GREY, width=1.5, dash="dot")))
        fig.add_annotation(x=xa, y=off, ax=xa, ay=R, xref="x", yref="y", axref="x", ayref="y", text="",
                           arrowside="end+start", arrowhead=2, arrowsize=1.2, arrowwidth=2.2, arrowcolor=col)
        fig.add_annotation(x=xa - 0.035, y=(off + R) / 2, text=lab, showarrow=False, textangle=-90,
                           font=dict(color=col, size=21), bgcolor="white")
    fig.add_trace(go.Scatter(x=[-0.45, 0], y=[R, R], mode="lines", line=dict(color=GREY, width=1.5, dash="dot")))
    # the axle line turns about the ICC; the wedge at the ICC is the angle turned so far
    a = -np.pi / 2 + phi
    u = np.array([np.cos(a), np.sin(a)])
    ends = np.array([ICC - 0.12 * u, ICC + 0.7 * u])
    fig.add_trace(go.Scatter(x=ends[:, 0], y=ends[:, 1], mode="lines", line=dict(color=GREY, width=2)))
    if phi > 0:
        x, y = arc(0.14, -np.pi / 2, a)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=GREY, width=3)))
        b = -np.pi / 2 + phi / 2
        fig.add_annotation(x=ICC[0] + 0.24 * np.cos(b), y=ICC[1] + 0.24 * np.sin(b), text=f"{phi:.1f} rad",
                           showarrow=False, font=dict(color=GREY, size=20), bgcolor="white")
    for _, off, _, _, col in POINTS:                                 # arcs travelled so far
        x, y = arc(R - off, -np.pi / 2, a)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=col, width=5)))
    for tr in robot((*place(phi, 0), phi), arrow=False):
        fig.add_trace(tr)
    h = np.array([np.cos(phi), np.sin(phi)])                         # speed arrows, half length, along the heading
    for _, off, spd, _, col in POINTS:
        p0 = place(phi, off)
        p1 = p0 + 0.5 * spd * h
        fig.add_trace(go.Scatter(x=[p0[0], p1[0]], y=[p0[1], p1[1]], mode="lines+markers", line=dict(color=col, width=4),
                                 marker=dict(symbol="arrow", size=[0, 15], angleref="previous", color=col)))
        fig.add_trace(go.Scatter(x=[p0[0]], y=[p0[1]], mode="markers", marker=dict(size=11, color=col)))
    fig.add_trace(go.Scatter(x=[ICC[0]], y=[ICC[1]], mode="markers", marker=dict(size=15, color=GREEN)))
    fig.add_annotation(x=0.035, y=0.535, text="ICC", showarrow=False, xanchor="left", font=dict(color=GREEN, size=24))
    # one line per point: arc = distance x angle; at 1 s the arc is also the speed
    for j, (name, off, spd, sym, col) in enumerate(POINTS):
        d = R - off
        s = f"{name}, {d:.1f} m from the ICC:  arc = {d:.1f} × {phi:.1f} = {d * phi:.2f} m"
        if phi == 1:
            s = f"{name}, {d:.1f} m from the ICC:  arc {d:.1f} m in 1 s, so {sym} = {spd:.1f} m/s"
        fig.add_annotation(x=0.5, y=1.15 - 0.05 * j, xref="paper", yref="paper", text=s, showarrow=False,
                           font=dict(color=col, size=21))
    fig.add_annotation(x=0.5, y=-0.05, xref="paper", yref="paper", showarrow=False, font=dict(color=GREY, size=20),
                       text="speed = angular velocity × distance from the ICC  (ω = 1 rad/s; m and m/s)")
    fig.update_xaxes(range=[-0.64, 0.76], visible=False)
    fig.update_yaxes(range=[-0.24, 1.14], visible=False, scaleanchor="x")
    fig.update_layout(template="simple_white", width=900, height=1130, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=200, b=90),
                      title=dict(x=0.5, y=0.975, font=dict(size=24),
                                 text=f"t = {phi:.1f} s: the robot has turned {phi:.1f} rad about the ICC"))
    return fig


phis = [round(0.1 * i, 1) for i in range(11)]
figs = [frame(p) for p in phis]
holds = [6] + [2] * (len(phis) - 2) + [20]
make_gif(figs, here / "icc_turn", fps=6, holds=holds, keys=[5, len(phis) - 1], cols=2, width=850)
