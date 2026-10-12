"""Driving to the pose with the polar-coordinate controller, one frame per 0.25 s: rho (grey dashed), alpha (red arc
at the robot, from its heading to the line of sight) and beta (purple arc at the dock pose, from the line of sight to
the dock heading, both continued back through the dock point) are redrawn every frame; the lower panels plot them over
time. The rule: v = 1 x rho, w = 5 alpha - 4 beta, scaled down together when a wheel would pass 0.6 m/s. The robot
first swings out to the right, so the line of sight turns towards 90 deg; alpha and beta reach 0 together and the
robot arrives at 8.45 s facing 90.0 deg. Run -> pose_anim.gif, pose_anim_frames.png"""
from pathlib import Path

import numpy as np
from drivekit import GOAL, START, pose_law, polar, run
from gifkit import FONT, GREY, PURPLE, RED, make_gif
from plotly.subplots import make_subplots
from roomdraw import axes, floor, goal, label, minus, polar_marks, robot, trail

here = Path(__file__).parent
P = run(pose_law)
deg = np.degrees
POL = np.array([polar(q) for q in zip(P["x"], P["y"], P["th"])])
RHO, ALPHA = POL[:, 0], deg(POL[:, 1])
BETA = deg(POL[:, 2])
assert round(P["t"][-1], 2) == 8.45 and round(deg(P["th"][-1]), 1) == 90.0
assert round(RHO[0], 2) == 2.97 and round(ALPHA[0], 1) == 27.4 and round(BETA[0], 1) == 32.6
assert round(P["v"][0], 3) == 0.598 and round(P["w"][0], 3) == 0.023


def frame(t):
    fig = make_subplots(rows=2, cols=2, specs=[[{"colspan": 2}, None], [{}, {}]], row_heights=[0.7, 0.3],
                        vertical_spacing=0.1, horizontal_spacing=0.14)
    k = min(int(round(t / 0.01)), len(P["t"]) - 1)
    q = (P["x"][k], P["y"][k], P["th"][k])
    floor(fig, (1, 1))
    goal(fig, rc=(1, 1))
    trail(fig, P["x"][:k + 1], P["y"][:k + 1], RED, (1, 1))
    robot(fig, q, RED, (1, 1))
    polar_marks(fig, q, RHO[k], np.radians(ALPHA[k]), np.radians(BETA[k]), (1, 1), min_rho=1.2)
    fig.add_trace(dict(type="scatter", x=P["t"][:k + 1], y=RHO[:k + 1], mode="lines", line=dict(color=GREY, width=3)),
                  row=2, col=1)
    fig.add_trace(dict(type="scatter", x=P["t"][:k + 1], y=ALPHA[:k + 1], mode="lines", line=dict(color=RED, width=3)),
                  row=2, col=2)
    fig.add_trace(dict(type="scatter", x=P["t"][:k + 1], y=BETA[:k + 1], mode="lines",
                       line=dict(color=PURPLE, width=3)), row=2, col=2)
    label(fig, 6.0, 26, "α", RED, (2, 2), size=18)
    label(fig, 7.2, 26, "β", PURPLE, (2, 2), size=18)
    if k == len(P["t"]) - 1:
        title = (f"arrives at {P['t'][-1]:.2f} s, within 1 cm<br><span style='font-size:19px'>"
                 f"facing {deg(P['th'][-1]):.1f}°: α and β reached 0 before ρ</span>")
    else:
        title = (f"t = {P['t'][k]:.2f} s: ρ = {RHO[k]:.2f} m, α = {ALPHA[k]:.1f}°, β = {BETA[k]:.1f}°"
                 f"<br><span style='font-size:19px'>"
                 f"v = {P['v'][k]:.3f} m/s, ω = {P['w'][k]:.3f} rad/s</span>")
    axes(fig, (1, 1))
    fig.update_xaxes(title=dict(text="time (s)", standoff=2), range=[0, 8.6], dtick=2, row=2)
    fig.update_yaxes(title=dict(text="ρ (m)", standoff=2), range=[0, 3.1], dtick=1, row=2, col=1)
    fig.update_yaxes(title=dict(text="angle (°)", standoff=2), range=[-2, 35], dtick=10, row=2, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, showlegend=False,
                      margin=dict(l=90, r=30, t=120, b=60), title=dict(x=0.5, y=0.97, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, 8.45, 0.25)) + [8.45]
figs = [frame(t) for t in ts]
holds = [5] + [1] * (len(ts) - 2) + [14]
k_keys = [0, 8, 16, len(ts) - 1]
make_gif(figs, here / "pose_anim", fps=4, holds=holds, keys=k_keys, cols=2, width=800)
