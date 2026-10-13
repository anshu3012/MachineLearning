"""Three sets of gains from the same start, one frame per 0.5 s for 30 s. Blue: k_rho = 1, k_alpha = 5, k_beta = -4
(spring 4, damper 4): arrives at 8.45 s facing 90.0 deg. Red: k_beta = +4, the wrong sign (the spring pushes):
its front hits the wall at 4.70 s, 0.79 m left of the dock. Purple: k_alpha = 0.5, smaller than k_rho (the damper
pushes): it circles and is still 1.87 m from the dock after 30 s. Lower panel: the distance rho of each.
Run -> gains_anim.gif, gains_anim_frames.png"""
from pathlib import Path

import numpy as np
from drivekit import GOAL, START, STOP_RHO, polar, pose_law, run
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif
from plotly.subplots import make_subplots
from roomdraw import axes, floor, goal, label, minus, robot, trail

here = Path(__file__).parent
deg = np.degrees


def hit(q):
    return q[1] > 3.5 + 0.005 or np.hypot(GOAL[0] - q[0], GOAL[1] - q[1]) < STOP_RHO


RUNS = [((1, 5, -4), BLUE, "k_ρ = 1, k_α = 5, k_β = −4"), ((1, 5, 4), RED, "k_β = +4"), ((1, 0.5, -4), PURPLE, "k_α = 0.5")]
R = [run(lambda q, k=k: pose_law(q, k=k), t_max=30, stop=hit) for k, _, _ in RUNS]
RHO = [np.array([polar(q)[0] for q in zip(r["x"], r["y"], r["th"])]) for r in R]
assert round(R[0]["t"][-1], 2) == 8.45 and round(deg(R[0]["th"][-1]), 1) == 90.0
assert round(R[1]["t"][-1], 2) == 4.70 and round(GOAL[0] - R[1]["x"][-1], 2) == 0.79
assert round(R[2]["t"][-1], 2) == 30.01 and round(RHO[2][-1], 2) == 1.87


def frame(t):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], vertical_spacing=0.09)
    floor(fig, (1, 1))
    goal(fig, rc=(1, 1), label=None)
    robot(fig, START, GREY, (1, 1), fill="rgba(0,0,0,0)", width=1)
    for (k, col, name), r, rho in zip(RUNS, R, RHO):
        i = min(int(round(t / 0.01)), len(r["t"]) - 1)
        trail(fig, r["x"][:i + 1], r["y"][:i + 1], col, (1, 1))
        robot(fig, (r["x"][i], r["y"][i], r["th"][i]), col, (1, 1))
        fig.add_trace(dict(type="scatter", x=r["t"][:i + 1], y=rho[:i + 1], mode="lines",
                           line=dict(color=col, width=3), showlegend=False), row=2, col=1)
    if t >= R[1]["t"][-1]:
        label(fig, R[1]["x"][-1] - 0.3, 3.32, "collides with the wall", RED, (1, 1), size=17, anchor="right")
    if t >= R[0]["t"][-1]:
        label(fig, GOAL[0] + 0.32, 3.3, "facing 90.0°", BLUE, (1, 1), size=17, anchor="left")
    sub = lambda c, txt: f"<span style='color:{c}'>{txt}</span>"
    key = (f"<br><span style='font-size:18px'>{sub(BLUE, 'blue: k<sub>ρ</sub> = 1, k<sub>α</sub> = 5, k<sub>β</sub> = −4')}"
           f"<br>{sub(RED, 'red: k<sub>β</sub> = +4, the wrong sign')}; "
           f"{sub(PURPLE, 'purple: k<sub>α</sub> = 0.5, below k<sub>ρ</sub>')}</span>")
    if t >= 30:
        title = f"after 30 s: purple still circles, {RHO[2][-1]:.2f} m from the dock" + key
    else:
        title = f"t = {t:.1f} s: one change from blue in each other run" + key
    axes(fig, (1, 1))
    fig.update_xaxes(title=dict(text="time (s)", standoff=2), range=[0, 30.5], dtick=5, row=2, col=1)
    fig.update_yaxes(title=dict(text="ρ (m)", standoff=2), range=[0, 3.2], dtick=1, row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1200, showlegend=False,
                      margin=dict(l=90, r=30, t=190, b=60), title=dict(x=0.5, y=0.975, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, 30.0, 0.5)) + [30.0]
figs = [frame(t) for t in ts]
holds = [5] + [1] * (len(ts) - 2) + [14]
make_gif(figs, here / "gains_anim", fps=5, holds=holds, keys=[0, 10, 18, len(ts) - 1], cols=2, width=800)
