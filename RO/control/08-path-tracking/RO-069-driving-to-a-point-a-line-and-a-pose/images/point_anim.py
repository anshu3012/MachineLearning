"""Driving to the point, one frame per 0.25 s: the distance rho to the dock point (grey dashed line) and the angle
alpha from the robot's heading (dotted) to the line of sight (red arc) are redrawn every frame; the lower panels plot
them over time. The rule: v = 1 x rho, w = 5 x alpha, both scaled down together when a wheel would pass 0.6 m/s.
alpha is gone by about 4 s; from 4.11 s (rho = 0.6 m) the speed is 1 x rho and rho shrinks to 37 % every second.
Run -> point_anim.gif, point_anim_frames.png"""
from pathlib import Path

import numpy as np
from drivekit import GOAL, START, point_law, polar, run
from gifkit import FONT, GREY, RED, make_gif
from plotly.subplots import make_subplots
from roomdraw import axes, floor, goal, label, minus, polar_marks, robot, trail

here = Path(__file__).parent
P = run(point_law)
deg = np.degrees
POL = np.array([polar(q) for q in zip(P["x"], P["y"], P["th"])])
RHO, ALPHA = POL[:, 0], deg(POL[:, 1])
K06 = int(np.argmax(RHO <= 0.6))
T06 = P["t"][K06]
assert round(T06, 2) == 4.11
assert abs(RHO[K06 + 100] / RHO[K06] - np.exp(-1)) < 0.01            # 37 % one second later
assert round(RHO[0], 2) == 2.97 and round(ALPHA[0], 1) == 27.4
assert abs(ALPHA[400]) < 0.1


def frame(t):
    fig = make_subplots(rows=2, cols=2, specs=[[{"colspan": 2}, None], [{}, {}]], row_heights=[0.7, 0.3],
                        vertical_spacing=0.1, horizontal_spacing=0.14)
    k = min(int(round(t / 0.01)), len(P["t"]) - 1)
    q = (P["x"][k], P["y"][k], P["th"][k])
    floor(fig, (1, 1))
    goal(fig, rc=(1, 1))
    trail(fig, P["x"][:k + 1], P["y"][:k + 1], RED, (1, 1))
    robot(fig, q, RED, (1, 1))
    polar_marks(fig, q, RHO[k], np.radians(ALPHA[k]), 0.0, (1, 1), show_beta=False)
    fig.add_trace(dict(type="scatter", x=P["t"][:k + 1], y=RHO[:k + 1], mode="lines", line=dict(color=GREY, width=3)),
                  row=2, col=1)
    fig.add_trace(dict(type="scatter", x=P["t"][:k + 1], y=ALPHA[:k + 1], mode="lines", line=dict(color=RED, width=3)),
                  row=2, col=2)
    if t >= T06:
        fig.add_trace(dict(type="scatter", x=[T06], y=[0.6], mode="markers", marker=dict(color="black", size=9)),
                      row=2, col=1)
        label(fig, T06 + 0.25, 1.15, "ρ = 0.6 m:<br>v = 1 × ρ", "black", (2, 1), size=15, anchor="left")
    if k == len(P["t"]) - 1:
        title = (f"arrives at {P['t'][-1]:.2f} s, within 1 cm<br><span style='font-size:19px'>"
                 f"facing {deg(P['th'][-1]):.1f}°: α reached 0 long before ρ</span>")
    else:
        title = (f"t = {P['t'][k]:.2f} s: ρ = {RHO[k]:.2f} m, α = {ALPHA[k]:.1f}°<br><span style='font-size:19px'>"
                 f"v = {P['v'][k]:.3f} m/s, ω = {P['w'][k]:.3f} rad/s</span>")
    axes(fig, (1, 1))
    fig.update_xaxes(title=dict(text="time (s)", standoff=2), range=[0, 8.5], dtick=2, row=2)
    fig.update_yaxes(title=dict(text="ρ (m)", standoff=2), range=[0, 3.1], dtick=1, row=2, col=1)
    fig.update_yaxes(title=dict(text="α (°)", standoff=2), range=[-2, 30], dtick=10, row=2, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, showlegend=False,
                      margin=dict(l=90, r=30, t=120, b=60), title=dict(x=0.5, y=0.97, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, 8.1, 0.25)) + [8.1]
figs = [frame(t) for t in ts]
holds = [5] + [1] * (len(ts) - 2) + [14]
k_keys = [0, 4, 17, len(ts) - 1]
make_gif(figs, here / "point_anim", fps=4, holds=holds, keys=k_keys, cols=2, width=800)
