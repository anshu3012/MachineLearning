"""Velocity model without noise, played. v = 0.5 m/s and omega = 1 rad/s give R = v/omega = 0.5 m; the ICC lies R to
the robot's left, at (1.750, 1.433). Over 1 s the robot turns 1 rad about it (green radius swinging, blue arc) and ends
at (2.249, 1.409) facing 87.3 deg. A faint robot takes one Euler step of 1 s instead: heading held at 30 deg, it drives
straight to (2.433, 1.250), 24 cm from the arc's end. The last frame shows both ends.
Run: python velocity_anim.py -> velocity_anim.gif, velocity_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, make_gif
from motion import DT, START, V, W, arc_end
from robotdraw import robot

here = Path(__file__).parent
X0, Y0, TH0 = START
R = V / W
XC, YC = X0 - R * np.sin(TH0), Y0 + R * np.cos(TH0)
XE, YE, THE = arc_end(X0, Y0, TH0, V, W, DT)
EX, EY = X0 + V * DT * np.cos(TH0), Y0 + V * DT * np.sin(TH0)       # one Euler step of 1 s
assert R == 0.5 and (round(XC, 3), round(YC, 3)) == (1.750, 1.433)
assert (round(XE, 3), round(YE, 3), round(np.degrees(THE), 1)) == (2.249, 1.409, 87.3)
assert (round(EX, 3), round(EY, 3)) == (2.433, 1.250) and round(np.hypot(EX - XE, EY - YE) * 100) == 24
SC = 0.3


def label(fig, x, y, s, col, anchor="center", size=20):
    fig.add_annotation(x=x, y=y, text=s, showarrow=False, xanchor=anchor, font=dict(color=col, size=size))


def arrow(fig, x, y, th, n, col=ORANGE):
    fig.add_trace(go.Scatter(x=[x, x + n * np.cos(th)], y=[y, y + n * np.sin(th)], mode="lines+markers",
                             line=dict(color=col, width=4),
                             marker=dict(symbol="arrow", size=[0, 15], angleref="previous", color=col)))


def frame(t, icc=True):
    """t: time driven so far (s); icc: show the ICC and the radius."""
    fig = go.Figure()
    a0 = np.arctan2(Y0 - YC, X0 - XC)                                  # direction ICC -> start, -60 deg
    if t > 0:                                                          # the Euler step, heading held at 30 deg
        fig.add_trace(go.Scatter(x=[X0, X0 + V * t * np.cos(TH0)], y=[Y0, Y0 + V * t * np.sin(TH0)], mode="lines",
                                 line=dict(color=GREY, dash="dash", width=2)))
        for tr in robot((X0 + V * t * np.cos(TH0), Y0 + V * t * np.sin(TH0), TH0), scale=SC, color=GREY,
                        opacity=0.35, arrow=False, fill="rgba(107,107,107,0.15)"):
            fig.add_trace(tr)
        s = np.linspace(a0, a0 + W * t, 40)
        fig.add_trace(go.Scatter(x=XC + R * np.cos(s), y=YC + R * np.sin(s), mode="lines",
                                 line=dict(color=BLUE, width=6)))
    xr, yr, thr = arc_end(X0, Y0, TH0, V, W, t) if t > 0 else START
    if icc:
        fig.add_trace(go.Scatter(x=[X0, XC], y=[Y0, YC], mode="lines", line=dict(color=GREEN, width=3)))
        label(fig, 1.86, 1.2165, "R = 0.5 m", GREEN, "right")
        if t > 0:
            fig.add_trace(go.Scatter(x=[XC, xr], y=[YC, yr], mode="lines", line=dict(color=GREEN, width=3)))
            s = np.linspace(a0, a0 + W * t, 30)
            fig.add_trace(go.Scatter(x=XC + 0.12 * np.cos(s), y=YC + 0.12 * np.sin(s), mode="lines+markers",
                                     line=dict(color=PURPLE, width=3),
                                     marker=dict(symbol="arrow", size=[0] * 29 + [12], angleref="previous",
                                                 color=PURPLE)))
            label(fig, 1.87, 1.36, "ωΔt = 1 rad" if t == 1 else f"turned {W * t:.1f} rad so far", PURPLE, "left")
        fig.add_trace(go.Scatter(x=[XC], y=[YC], mode="markers", marker=dict(size=15, color=GREEN)))
        label(fig, XC, YC + 0.04, "ICC (1.750, 1.433)", GREEN)
    arrow(fig, X0, Y0, TH0, 0.13)
    label(fig, 2.08, 1.0, "heading 30°", ORANGE, "left")
    fig.add_trace(go.Scatter(x=[X0], y=[Y0], mode="markers", marker=dict(size=12, color="black")))
    label(fig, X0, 0.925, "start (2, 1)", "black")
    if t == 1:
        fig.add_shape(type="line", x0=EX, y0=EY, x1=XE, y1=YE, line=dict(color="black", width=2, dash="dot"),
                      opacity=1)
        label(fig, 2.36, 1.345, "24 cm", "black", "left")
        label(fig, 2.46, 1.15, "Euler step (2.433, 1.250)", GREY)
        arrow(fig, XE, YE, THE, 0.12)
        label(fig, XE + 0.006, 1.56, "heading 87.3°", ORANGE)
    for tr in robot((xr, yr, thr), scale=SC, arrow=t < 1):
        fig.add_trace(tr)
    if t == 1:
        fig.add_trace(go.Scatter(x=[XE], y=[YE], mode="markers", marker=dict(size=12, color="black")))
        label(fig, 2.32, YE, "end (2.249, 1.409)", "black", "left")
    fig.update_xaxes(range=[1.6, 2.62], dtick=0.1, showgrid=True, gridcolor="#e4e4e4", title="x (m)")
    fig.update_yaxes(range=[0.88, 1.6], dtick=0.1, showgrid=True, gridcolor="#e4e4e4", title="y (m)",
                     scaleanchor="x")
    head = (f"t = {t:.1f} s: the robot has turned {W * t:.1f} rad about the ICC" if t > 0 else
            "R = v / ω = 0.5 m: the ICC lies 0.5 m to the robot's left")
    sub = "faint: one Euler step of 1 s, heading held at 30°" if t > 0 else "square to its heading of 30°"
    fig.update_layout(template="simple_white", width=1000, height=880, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=130, b=70),
                      title=dict(x=0.5, y=0.96, font=dict(size=23),
                                 text=f"{head}<br><span style='font-size:20px;color:{GREY}'>{sub}</span>"))
    return fig


f0 = frame(0, icc=False)
f0.update_layout(title_text="v = 0.5 m/s, ω = 1 rad/s held for Δt = 1 s: where does the robot end?")
figs = [f0, frame(0)] + [frame(round(0.2 * k, 1)) for k in range(1, 6)]
holds = [8, 8] + [3] * 4 + [24]
make_gif(figs, here / "velocity_anim", fps=4, holds=holds, keys=[3, 6], cols=2, width=950)
