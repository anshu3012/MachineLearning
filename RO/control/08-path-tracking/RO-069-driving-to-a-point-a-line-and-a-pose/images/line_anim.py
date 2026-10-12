"""Driving along a line, one frame per 0.25 s: the dock's centre line x = 3.6 m, heading 90 deg (green dashed). Each
frame redraws the robot's distance e from the line (purple, + to the line's left) and its heading error psi, the
heading minus the line's direction (red arc from the dotted green line-direction to the robot's heading). The rule:
v = 0.5 m/s, w = -2 e - 2 psi. The robot settles onto the line without swinging but never slows: its front meets
the dock at 6.60 s at 0.50 m/s, 0.022 m left of the line and facing 87.9 deg.
Run -> line_anim.gif, line_anim_frames.png"""
from pathlib import Path

import numpy as np
from drivekit import GOAL, R_ROBOT, WALL_Y, line_dist, line_law, run
from gifkit import FONT, GREEN, PURPLE, RED, make_gif
from plotly.subplots import make_subplots
from roomdraw import arc, arrow, axes, floor, goal, label, minus, robot, trail

here = Path(__file__).parent
deg = np.degrees
P = run(line_law, stop=lambda q: q[1] + R_ROBOT >= WALL_Y)
EP = np.array([line_dist(q) for q in zip(P["x"], P["y"], P["th"])])
E, PSI = EP[:, 0], deg(EP[:, 1])
assert round(P["t"][-1], 2) == 6.60 and round(P["v"][-2], 2) == 0.50
assert round(E[-1], 3) == 0.022 and round(deg(P["th"][-1]), 1) == 87.9
assert round(E[0], 2) == 1.60 and round(PSI[0], 1) == -60.0
assert round(deg(P["th"].min()), 1) == 13.7


def frame(t):
    fig = make_subplots(rows=2, cols=2, specs=[[{"colspan": 2}, None], [{}, {}]], row_heights=[0.7, 0.3],
                        vertical_spacing=0.1, horizontal_spacing=0.14)
    k = min(int(round(t / 0.01)), len(P["t"]) - 1)
    x, y, th = P["x"][k], P["y"][k], P["th"][k]
    floor(fig, (1, 1))
    goal(fig, rc=(1, 1), label=None)
    arrow(fig, (GOAL[0], 0.6), (GOAL[0], 3.2), GREEN, (1, 1), width=2.5, dash="dash", size=15)
    label(fig, GOAL[0] + 0.1, 0.75, "the dock's line, heading 90°", GREEN, (1, 1), size=17, anchor="left")
    trail(fig, P["x"][:k + 1], P["y"][:k + 1], RED, (1, 1))
    robot(fig, (x, y, th), RED, (1, 1))
    if abs(E[k]) > 0.15:
        arrow(fig, (GOAL[0], y), (x, y), PURPLE, (1, 1), width=3, size=13)
        label(fig, GOAL[0] + 0.12, y, f"e = {E[k]:.2f} m", PURPLE, (1, 1), size=18, anchor="left")
        fig.add_trace(dict(type="scatter", x=[x, x], y=[y, y + 0.75], mode="lines",
                           line=dict(color=GREEN, width=2.5, dash="dot"), showlegend=False), row=1, col=1)
        fig.add_trace(dict(type="scatter", x=[x, x + 0.75 * np.cos(th)], y=[y, y + 0.75 * np.sin(th)], mode="lines",
                           line=dict(color="#4C78A8", width=2.5, dash="dot"), showlegend=False), row=1, col=1)
        arc(fig, (x, y), 0.6, GOAL[2], th, RED, (1, 1), width=4, size=14)
        label(fig, x - 0.55, y + 0.62, f"ψ = {PSI[k]:.1f}°", RED, (1, 1), size=18, anchor="right")
    fig.add_trace(dict(type="scatter", x=P["t"][:k + 1], y=E[:k + 1], mode="lines", line=dict(color=PURPLE, width=3),
                       showlegend=False), row=2, col=1)
    fig.add_trace(dict(type="scatter", x=P["t"][:k + 1], y=PSI[:k + 1], mode="lines", line=dict(color=RED, width=3),
                       showlegend=False), row=2, col=2)
    if k == len(P["t"]) - 1:
        title = (f"front at the dock at {P['t'][-1]:.2f} s, still at {P['v'][-2]:.2f} m/s<br>"
                 f"<span style='font-size:19px'>on the line (e = {E[-1]:.3f} m), facing {deg(th):.1f}°,"
                 " but nothing told it to stop</span>")
    else:
        title = (f"t = {P['t'][k]:.2f} s: e = {E[k]:.2f} m, ψ = {PSI[k]:.1f}°<br><span style='font-size:19px'>"
                 f"v = {P['v'][k]:.3f} m/s, ω = {P['w'][k]:.3f} rad/s</span>")
    axes(fig, (1, 1))
    fig.update_xaxes(title=dict(text="time (s)", standoff=2), range=[0, 7], dtick=1, row=2)
    fig.update_yaxes(title=dict(text="e (m)", standoff=2), range=[-0.1, 1.7], dtick=0.5, row=2, col=1)
    fig.update_yaxes(title=dict(text="ψ (°)", standoff=2), range=[-80, 5], dtick=20, row=2, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, showlegend=False,
                      margin=dict(l=90, r=30, t=120, b=60), title=dict(x=0.5, y=0.97, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, 6.6, 0.25)) + [6.6]
figs = [frame(t) for t in ts]
holds = [5] + [1] * (len(ts) - 2) + [14]
make_gif(figs, here / "line_anim", fps=4, holds=holds, keys=[0, 4, 12, len(ts) - 1], cols=2, width=800)
