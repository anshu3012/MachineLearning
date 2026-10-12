"""Nav2's graceful controller (green) against this Note's polar-coordinate controller (blue) on the dock, one frame
per 0.25 s. The graceful controller runs Nav2's SmoothControlLaw with the plugin's default parameters (k_phi 2.0,
k_delta 1.0, beta 0.4, lambda 2.0, v_linear_max 0.5 m/s, v_angular_max 1.0 rad/s, slowdown_radius 1.5 m). Lower
panel: the forward speed of each. The graceful controller starts slowing 1.5 m from the dock, so it arrives later,
at 11.15 s instead of 8.45 s, facing 89.95 deg. Run -> graceful_anim.gif, graceful_anim_frames.png"""
from pathlib import Path

import numpy as np
from drivekit import GOAL, START, graceful_law, polar, pose_law, run
from gifkit import BLUE, FONT, GREEN, GREY, make_gif
from plotly.subplots import make_subplots
from roomdraw import axes, floor, goal, label, minus, robot, trail

here = Path(__file__).parent
deg = np.degrees
B = run(pose_law)
G = run(graceful_law)
RHO_G = np.array([polar(q)[0] for q in zip(G["x"], G["y"], G["th"])])
K15 = int(np.argmax(RHO_G <= 1.5))
assert round(B["t"][-1], 2) == 8.45 and round(G["t"][-1], 2) == 11.15 and round(deg(G["th"][-1]), 2) == 89.95
assert round(G["v"][0], 3) == 0.495 and round(G["v"].max(), 3) == 0.495
assert G["v"][K15 + 20] < G["v"][K15 - 5]


def frame(t):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], vertical_spacing=0.09)
    floor(fig, (1, 1))
    goal(fig, rc=(1, 1), label=None)
    robot(fig, START, GREY, (1, 1), fill="rgba(0,0,0,0)", width=1)
    for r, col in ((B, BLUE), (G, GREEN)):
        i = min(int(round(t / 0.01)), len(r["t"]) - 1)
        trail(fig, r["x"][:i + 1], r["y"][:i + 1], col, (1, 1))
        robot(fig, (r["x"][i], r["y"][i], r["th"][i]), col, (1, 1))
        fig.add_trace(dict(type="scatter", x=r["t"][:i + 1], y=r["v"][:i + 1], mode="lines",
                           line=dict(color=col, width=3), showlegend=False), row=2, col=1)
    label(fig, 4.3, 2.0, "polar-coordinate<br>controller", BLUE, (1, 1), size=17, anchor="left")
    label(fig, 4.3, 1.4, "Nav2 graceful<br>controller", GREEN, (1, 1), size=17, anchor="left")
    if t >= G["t"][-1]:
        title = ("both stop within 1 cm of the dock point, facing 90° to within 0.1°<br><span style='font-size:19px'>"
                 f"polar: {B['t'][-1]:.2f} s; graceful: {G['t'][-1]:.2f} s, slowing from 1.5 m out</span>")
    else:
        title = f"t = {t:.2f} s<br><span style='font-size:19px'>the same start and dock pose</span>"
    axes(fig, (1, 1))
    fig.update_xaxes(title=dict(text="time (s)", standoff=2), range=[0, 11.5], dtick=1, row=2, col=1)
    fig.update_yaxes(title=dict(text="speed v (m/s)", standoff=2), range=[0, 0.65], dtick=0.2, row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, showlegend=False,
                      margin=dict(l=90, r=30, t=120, b=60), title=dict(x=0.5, y=0.97, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, 11.15, 0.25)) + [11.15]
figs = [frame(t) for t in ts]
holds = [5] + [1] * (len(ts) - 2) + [14]
make_gif(figs, here / "graceful_anim", fps=5, holds=holds, keys=[0, 12, 28, len(ts) - 1], cols=2, width=800)
