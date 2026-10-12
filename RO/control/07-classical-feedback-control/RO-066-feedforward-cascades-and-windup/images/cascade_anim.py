"""A 90 degree turn three ways, one frame per 0.1 s for 8 s. Blue: the heading cascade (outer P, 1 rad/s per rad, capped
at 1 rad/s; inner PI on the gyro, poles at -10 rad/s; torque limited to 0.2 N m): the inner loop catches its command
within 0.48 s and the heading is within 2 degrees after 4.22 s, without overshoot (a perfect inner loop would take 3.93 s,
dotted). Purple: RO-060's heading PID (0.2, 0.283, 0.05): overshoots by 20.8 degrees. Red: one heading PID with the
cascade's gains multiplied out (12, 10, 2), with clamping: nothing caps its turn rate, it spins at up to 2.19 rad/s and
overshoots by 48.4 degrees. Top: the cascade robot from above. Middle: yaw rate. Bottom: heading.
Run: python cascade_anim.py -> cascade_anim.gif, cascade_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, RED, make_gif
from robotctl import KIW, KTH, KW, W_CAP, heading_loop, heading_pid

here = Path(__file__).parent
T = 8
ref = lambda t: np.pi / 2
s = heading_loop(T, ref)
p = heading_pid(T, ref)
q = heading_pid(T, ref, kp=KW * KTH + KIW, ki=KIW * KTH, kd=KW, clamp=True)
t, th, w, wc = s["t"], s["th"], s["w"], s["wc"]
inner_ok = np.argmax(np.abs(w - wc) < 0.05 * np.abs(wc))
outer_ok = np.where(np.abs(th - np.pi / 2) > np.radians(2))[0][-1] + 1
assert abs(t[inner_ok] - 0.48) < 1e-9 and abs(t[outer_ok] - 4.22) < 1e-9 and th.max() <= np.pi / 2 + 1e-3
assert abs(np.degrees(p["th"].max() - np.pi / 2) - 20.8) < 0.05
assert abs(np.degrees(q["th"].max() - np.pi / 2) - 48.4) < 0.05 and abs(q["w"].max() - 2.19) < 5e-3
tc = np.pi / 2 - W_CAP / KTH                        # perfect inner loop: 0.571 s at the cap, then exponential
ideal = np.where(t < tc, W_CAP * t, np.pi / 2 - np.exp(-KTH * (t - tc)))
assert abs(tc + np.log(1 / np.radians(2)) - 3.93) < 5e-3


def robot(theta):
    c, sn = np.cos(theta), np.sin(theta)
    pts = np.array([[-0.15, -0.1], [0.15, -0.1], [0.15, 0.1], [-0.15, 0.1], [-0.15, -0.1]])
    return pts @ np.array([[c, -sn], [sn, c]]).T


def frame(k):
    fig = make_subplots(rows=3, cols=1, row_heights=[0.28, 0.33, 0.39], vertical_spacing=0.08)
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, 0.3], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                             showlegend=False), row=1, col=1)
    pr = robot(th[k])
    fig.add_trace(go.Scatter(x=pr[:, 0], y=pr[:, 1], mode="lines", fill="toself", fillcolor="rgba(76,120,168,0.35)",
                             line=dict(color=BLUE, width=3), showlegend=False), row=1, col=1)
    fig.add_annotation(x=0.25 * np.cos(th[k]), y=0.25 * np.sin(th[k]), ax=0, ay=0, xref="x", yref="y", axref="x",
                       ayref="y", showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor=BLUE, text="")
    fig.add_annotation(x=0.02, y=0.31, xref="x", yref="y", text="target: 90°", showarrow=False, xanchor="left",
                       font=dict(size=18, color=GREY))
    fig.add_annotation(x=-0.44, y=-0.25, xref="x", yref="y", text="cascade robot", showarrow=False, xanchor="left",
                       font=dict(size=18, color=BLUE))
    fig.add_trace(go.Scatter(x=[0, T], y=[W_CAP] * 2, mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                             showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=wc[:k + 1], mode="lines", line=dict(color=ORANGE, width=4, dash="dash"),
                             name="cascade: yaw-rate command"), row=2, col=1)
    for run, col, name in ((q, RED, "one PID, gains 12, 10, 2"), (p, PURPLE, "RO-060's heading PID"),
                           (s, BLUE, "cascade")):
        fig.add_trace(go.Scatter(x=t[:k + 1], y=run["w"][:k + 1], mode="lines", line=dict(color=col, width=4),
                                 name=name), row=2, col=1)
        fig.add_trace(go.Scatter(x=t[:k + 1], y=np.degrees(run["th"][:k + 1]), mode="lines",
                                 line=dict(color=col, width=4), showlegend=False), row=3, col=1)
    fig.add_trace(go.Scatter(x=[0, T], y=[90, 90], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                             showlegend=False), row=3, col=1)
    fig.add_trace(go.Scatter(x=t[:k + 1], y=np.degrees(ideal[:k + 1]), mode="lines",
                             line=dict(color=GREY, width=3, dash="dot"), name="perfect inner loop"), row=3, col=1)
    fig.add_annotation(x=4.0, y=1.14, xref="x2", yref="y2", text="cap, 1 rad/s", showarrow=False, xanchor="left",
                       font=dict(size=16, color=GREY))
    if k >= inner_ok:
        fig.add_annotation(x=t[inner_ok], y=w[inner_ok], xref="x2", yref="y2", ax=110, ay=-80, xanchor="left",
                           text="inner loop on its command: 0.48 s", font=dict(size=17, color=BLUE), arrowcolor=BLUE)
    if k >= outer_ok:
        fig.add_annotation(x=t[outer_ok], y=np.degrees(th[outer_ok]), xref="x3", yref="y3", ax=20, ay=50,
                           text="within 2°: 4.22 s", font=dict(size=17, color=BLUE), arrowcolor=BLUE, xanchor="left")
    fig.add_annotation(x=0.02, y=1.03, xref="paper", yref="paper", text=f"t = {t[k]:.1f} s   cascade heading {np.degrees(th[k]):.0f}°",
                       showarrow=False, font=dict(size=21), xanchor="left")
    fig.update_xaxes(range=[-0.45, 0.45], visible=False, row=1, col=1)
    fig.update_yaxes(range=[-0.32, 0.36], visible=False, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[0, T], row=2, col=1)
    fig.update_xaxes(range=[0, T], title="time (s)", row=3, col=1)
    fig.update_yaxes(range=[-1.7, 2.4], title="yaw rate (rad/s)", row=2, col=1)
    fig.update_yaxes(range=[0, 150], title="heading (°)", row=3, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, margin=dict(l=100, r=30, t=60, b=70),
                      legend=dict(x=0.99, xanchor="right", y=0.69, yanchor="top", font=dict(size=16)))
    return fig


ks = list(range(0, len(t), 10))
figs = [frame(k) for k in ks]
make_gif(figs, here / "cascade_anim", fps=8, holds=[6] + [1] * (len(ks) - 2) + [24],
         keys=[ks.index(50), ks.index(200), len(ks) - 1], cols=1, width=800)
