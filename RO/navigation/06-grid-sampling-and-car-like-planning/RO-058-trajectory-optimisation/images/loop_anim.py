"""The receding-horizon loop, cycle by cycle, from t = 2.2 s to 2.7 s; the person steps onto the route at 2.4 s.
Each cycle has three frames. 1 measure: the robot has driven 0.1 s along last cycle's band (pale). 2 warm start:
the poses the robot has passed are dropped, the first pose is moved to the robot and the last to the new local goal
(cross), 1.5 m further along the global plan. 3 optimise: TEB's 4 passes of 5 steps give the new band (orange).
Then the robot drives the band's first 0.1 s and the next cycle begins. Run -> loop_anim.gif, loop_anim_frames.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
L = bk.results()["loop"]
CYC = list(range(22, 28))
assert [round(L[k]["t"], 1) for k in CYC] == [2.2, 2.3, 2.4, 2.5, 2.6, 2.7]
xs = np.array([o["x"] for o in L])
STAGES = ["1 measure the robot", "2 warm start: shift last band", "3 optimise: 4 passes of 5 steps"]


def frame(k, stage):
    o = L[k]
    fig = go.Figure()
    rd.room(fig)
    rd.route(fig, bk.ROUTE)
    if o["person"] is not None:
        rd.person(fig, bk.PERSON, bk.PERSON_R)
    fig.add_trace(go.Scatter(x=xs[:k + 1, 0], y=xs[:k + 1, 1], mode="lines", line=dict(color=BLUE, width=4)))
    if stage == 0:
        rd.band(fig, L[k - 1]["P"], "#F9D2A8", size=8)
        g = L[k - 1]["goal"]
    elif stage == 1:
        rd.band(fig, L[k - 1]["P"], "#F9D2A8", size=6, width=1.5, ticks=False)
        rd.band(fig, o["warm"][0], ORANGE, size=8)
        g = o["goal"]
    else:
        rd.band(fig, o["P"], ORANGE, size=8)
        g = o["goal"]
    fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=18, color=ORANGE)))
    rd.robot(fig, *o["x"], BLUE, fill="rgba(255,255,255,0)")
    lines = [f"<b>cycle at t = {o['t']:.1f} s</b>"] + [
        (f"<b>{s}</b>" if j == stage else f"<span style='color:#AAAAAA'>{s}</span>") for j, s in enumerate(STAGES)] + [
        "<span style='color:#AAAAAA'>4 drive the first 0.1 s</span>"]
    if k == 24:
        lines.append("<span style='color:#C2185B'>person seen in this cycle</span>")
    fig.add_annotation(x=1.72, y=3.62, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.92)")
    rd.zoom(fig, (1.7, 3.75), (1.45, 3.65))
    fig.update_layout(template="simple_white", font=FONT, width=820, height=840, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


figs, holds = [], []
for k in CYC:
    for st in range(3):
        figs.append(frame(k, st))
        holds.append(3)
holds[0], holds[-1] = 5, 12
make_gif(figs, here / "loop_anim", fps=2, holds=holds, keys=[6, 7, 8, 17], cols=2, width=620)
