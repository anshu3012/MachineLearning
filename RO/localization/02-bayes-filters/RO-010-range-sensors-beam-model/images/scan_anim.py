"""Figure 1 as an animation. The robot at pose (2, 2, 0) in the 5 m x 4 m room fires its four beams one by one,
at 0, 90, 180 and 270 degrees from its heading. Each beam travels out and stops at the first surface: the forward
beam stops at a person 1.00 m ahead although the wall is 3 m away. The readings fill in beside the room; the last
frame is the whole scan. Run -> scan_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import POSE, raycast
from gifkit import BLUE, FONT, GREY, RED, make_gif
from roomkit import PERSON, axes, person, robot, room, text

here = Path(__file__).parent
READ = [1.00, 1.97, 2.04, 1.99]                # the scan of the Note, beams at 0, 90, 180, 270 degrees
ANG = [0, 90, 180, 270]
X0, Y0, _ = POSE
LABEL = [(2.5, 1.78, "1.00", "center"), (2.1, 3.0, "1.97", "left"), (1.0, 2.24, "2.04", "center"),
         (2.1, 1.0, "1.99", "left")]
STOP = ["the person, 1.00 m", "the wall, 1.97 m", "the wall, 2.04 m", "the wall, 1.99 m"]


def tip(k, frac=1.0):
    a = np.radians(ANG[k])
    return X0 + READ[k] * frac * np.cos(a), Y0 + READ[k] * frac * np.sin(a)


def frame(done, k=None, frac=None, title=""):
    """done: beams that have stopped; beam k is on its way, frac of its reading travelled."""
    fig = go.Figure()
    axes(fig, dom=(0.0, 0.62))
    room(fig)
    if 0 in done:
        fig.add_trace(go.Scatter(x=[PERSON[0] + PERSON[2], 5.0], y=[2, 2], mode="lines",
                                 line=dict(color=BLUE, width=3, dash="dash")))
        text(fig, 4.2, 1.72, "wall at 3 m", BLUE, ref=("x", "y"), anchor="center", bgcolor="white")
    for j in done:
        x, y = tip(j)
        fig.add_trace(go.Scatter(x=[X0, x], y=[Y0, y], mode="lines+markers", line=dict(color=RED, width=4),
                                 marker=dict(size=[0, 11], color=RED)))
        lx, ly, s, anc = LABEL[j]
        text(fig, lx, ly, s, RED, ref=("x", "y"), anchor=anc, bgcolor="white")
    if k is not None:
        x, y = tip(k, frac)
        fig.add_trace(go.Scatter(x=[X0, x], y=[Y0, y], mode="lines+markers", line=dict(color=RED, width=4),
                                 marker=dict(size=[0, 15], color=RED, symbol="circle-open", line=dict(width=4))))
    person(fig)
    robot(fig, X0, Y0, label="robot (2, 2, 0)")
    text(fig, 0.68, 0.93, "readings z (m)", size=FONT["size"])
    for j in range(4):
        got = j in done
        text(fig, 0.68, 0.80 - 0.1 * j, f"beam {ANG[j]}°:  " + (f"{READ[j]:.2f}" if got else "…"),
             RED if got else GREY)
    text(fig, 0.68, 0.30, "red: what each beam reads", RED, size=18)
    if 0 in done:
        text(fig, 0.68, 0.22, "dashed blue: where the forward", BLUE, size=18)
        text(fig, 0.68, 0.15, "beam should end (the wall)", BLUE, size=18)
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, showlegend=False,
                      margin=dict(l=30, r=20, t=70, b=30), title=dict(text=title, x=0.5, font_size=22))
    return fig


figs, holds, keys = [frame([], title="the robot at (2, 2, 0) fires its four beams one by one")], [4], []
done = []
for k in range(4):
    for f in (0.35, 0.7):
        figs.append(frame(done, k, f, title=f"beam {ANG[k]}° travels out"))
        holds.append(1)
    done = done + [k]
    figs.append(frame(done, title=f"beam {ANG[k]}° stops at {STOP[k]}"
                      + ("; the wall is 3 m away" if k == 0 else "")))
    holds.append(7 if k == 0 else 5)
    if k == 0:
        keys.append(len(figs) - 1)
figs.append(frame(done, title="the scan: four readings, z = (1.00, 1.97, 2.04, 1.99)"))
holds.append(20)
keys.append(len(figs) - 1)
make_gif(figs, here / "scan_anim", fps=4, holds=holds, keys=keys, cols=2, width=900)
assert [raycast(POSE, np.radians(a)) for a in ANG] == [3.0, 2.0, 2.0, 2.0]   # the map: forward wall 3 m away
assert abs(PERSON[0] - PERSON[2] - X0 - READ[0]) < 1e-9                      # the person's near edge: 1.00 m ahead
