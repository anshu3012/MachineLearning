"""The pose controller (k_rho = 1, k_alpha = 5, k_beta = -4) from eight starts on a half circle of radius 2 m below
the dock, every 20 deg from 200 to 340 deg, each facing 90 deg; one frame per 0.25 s. Each robot first turns towards
the dock, swings out and comes in along the dock's line; all eight stop within 1 cm of the dock point between 6.45 and
7.80 s, facing 90.0 deg to within 0.05 deg. Run -> many_anim.gif, many_anim_frames.png"""
from pathlib import Path

import numpy as np
from drivekit import GOAL, pose_law, run
from gifkit import BLUE, FONT, GREY, make_gif
from plotly.subplots import make_subplots
from roomdraw import axes, floor, goal, minus, robot, trail

here = Path(__file__).parent
deg = np.degrees
ANG = np.arange(200, 341, 20)
STARTS = [(GOAL[0] + 2 * np.cos(np.radians(a)), GOAL[1] + 2 * np.sin(np.radians(a)), np.radians(90)) for a in ANG]
R = [run(pose_law, q0=q, t_max=30) for q in STARTS]
T = np.array([r["t"][-1] for r in R])
TH = np.array([deg(r["th"][-1]) for r in R])
assert len(R) == 8 and round(T.min(), 2) == 6.45 and round(T.max(), 2) == 7.80
assert np.all(np.abs(TH - 90) < 0.05) and max(r["y"].max() for r in R) < 3.5


def frame(t):
    fig = make_subplots(rows=1, cols=1)
    floor(fig, (1, 1))
    goal(fig, rc=(1, 1), label=None)
    for q, r in zip(STARTS, R):
        i = min(int(round(t / 0.01)), len(r["t"]) - 1)
        robot(fig, q, GREY, (1, 1), fill="rgba(0,0,0,0)", width=1)
        trail(fig, r["x"][:i + 1], r["y"][:i + 1], BLUE, (1, 1), width=2.5)
        robot(fig, (r["x"][i], r["y"][i], r["th"][i]), BLUE, (1, 1), width=2)
    if t >= T.max():
        title = ("all eight stop within 1 cm of the dock point<br><span style='font-size:19px'>"
                 f"between {T.min():.2f} and {T.max():.2f} s, facing 90.0° to within 0.05°</span>")
    else:
        title = (f"t = {t:.2f} s<br><span style='font-size:19px'>eight starts 2 m from the dock, each facing 90°;"
                 " the same gains for all</span>")
    axes(fig, (1, 1), yr=(1.0, 4.15))
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=820, showlegend=False,
                      margin=dict(l=90, r=30, t=120, b=60), title=dict(x=0.5, y=0.97, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, 7.8, 0.25)) + [7.8]
figs = [frame(t) for t in ts]
holds = [5] + [1] * (len(ts) - 2) + [14]
make_gif(figs, here / "many_anim", fps=4, holds=holds, keys=[0, 6, 14, len(ts) - 1], cols=2, width=800)
