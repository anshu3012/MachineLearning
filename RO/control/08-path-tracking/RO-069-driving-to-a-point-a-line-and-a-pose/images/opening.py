"""The opening problem: the robot starts at (2.0, 1.0) facing 30 deg and must stop at the dock pose (3.6, 3.5) facing
90 deg. Driving to the point (aim at it, slow down near it) gets there in 8.10 s but facing 64.0 deg, 26.0 deg short.
The last frame adds the pose controller of Section 4, which arrives in 8.45 s facing 90.0 deg.
Run -> opening.gif, opening_frames.png"""
from pathlib import Path

import numpy as np
from drivekit import GOAL, START, point_law, pose_law, run
from gifkit import BLUE, FONT, GREY, RED, make_gif
from plotly.subplots import make_subplots
from roomdraw import axes, floor, goal, label, minus, robot, trail

here = Path(__file__).parent
P = run(point_law)
Q = run(pose_law)
deg = np.degrees
assert round(P["t"][-1], 2) == 8.10 and round(deg(P["th"][-1]), 1) == 64.0
assert round(Q["t"][-1], 2) == 8.45 and round(deg(Q["th"][-1]), 1) == 90.0
assert round(90 - deg(P["th"][-1]), 1) == 26.0


def frame(t, last=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], vertical_spacing=0.09)
    floor(fig, (1, 1))
    goal(fig, rc=(1, 1))
    k = min(int(round(t / 0.01)), len(P["t"]) - 1)
    trail(fig, P["x"][:k + 1], P["y"][:k + 1], RED, (1, 1))
    robot(fig, (P["x"][k], P["y"][k], P["th"][k]), RED, (1, 1))
    robot(fig, START, GREY, (1, 1), fill="rgba(0,0,0,0)", width=1)
    label(fig, START[0] - 0.32, START[1], "start", GREY, (1, 1), size=17, anchor="right")
    fig.add_trace(dict(type="scatter", x=P["t"][:k + 1], y=deg(P["th"][:k + 1]), mode="lines",
                       line=dict(color=RED, width=3), showlegend=False), row=2, col=1)
    fig.add_trace(dict(type="scatter", x=[0, 9], y=[90, 90], mode="lines", line=dict(color=GREY, width=2, dash="dash"),
                       showlegend=False), row=2, col=1)
    label(fig, 0.2, 99, "dock heading 90°", GREY, (2, 1), size=16, anchor="left")
    if last:
        trail(fig, Q["x"], Q["y"], BLUE, (1, 1))
        robot(fig, (Q["x"][-1], Q["y"][-1], Q["th"][-1]), BLUE, (1, 1))
        fig.add_trace(dict(type="scatter", x=Q["t"], y=deg(Q["th"]), mode="lines", line=dict(color=BLUE, width=3),
                           showlegend=False), row=2, col=1)
        label(fig, 4.6, 2.3, "pose controller (Section 4):<br>8.45 s, facing 90.0°", BLUE, (1, 1), size=17,
              anchor="left")
        label(fig, 4.6, 1.3, "to the point: 8.10 s,<br>facing 64.0°", RED, (1, 1), size=17, anchor="left")
        title = "both stop within 1 cm of the dock point<br><span style='font-size:19px'>only the pose controller faces the dock</span>"
    elif k == len(P["t"]) - 1:
        title = (f"to the point: arrives at {P['t'][-1]:.2f} s facing {deg(P['th'][-1]):.1f}°"
                 f"<br><span style='font-size:19px'>26.0° short of the dock's 90°</span>")
    else:
        title = (f"to the point: t = {P['t'][k]:.1f} s<br><span style='font-size:19px'>"
                 f"heading {deg(P['th'][k]):.1f}°, speed {P['v'][k]:.2f} m/s</span>")
    axes(fig, (1, 1))
    fig.update_xaxes(title=dict(text="time (s)", standoff=2), range=[0, 9], dtick=1, row=2, col=1)
    fig.update_yaxes(title=dict(text="heading (°)", standoff=2), range=[20, 105], dtick=30, row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, showlegend=False,
                      margin=dict(l=90, r=30, t=120, b=60), title=dict(x=0.5, y=0.97, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, 8.1, 0.4)) + [8.1]
figs = [frame(t) for t in ts] + [frame(8.1, last=True)]
holds = [4] + [1] * (len(ts) - 2) + [6, 14]
make_gif(figs, here / "opening", fps=4, holds=holds, keys=[0, 5, len(ts) - 1, len(figs) - 1], cols=2, width=800)
