"""Animation: the opening problem. Two robots follow the potential field downhill at the same time (gradient descent,
pf.descend). The one starting at (2, 1) reaches the doorway centre (3.6, 4.0) after 3.47 m; the one starting at
(4.0, 0.5), between the table and the bottom wall, stops at (3.60, 0.59), 3.41 m from the door.
Run -> problem.gif, problem_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import drawkit as dk
import pf
from gifkit import GREEN, RED, make_gif

here = Path(__file__).parent
PA, PB = pf.descend(pf.START), pf.descend(pf.START2)
LA, LB = pf.path_length(PA), pf.path_length(PB)
end = PB[-1]
assert round(LA, 2) == 3.47 and abs(PA[-1][1] - 3.98) < 0.01
assert (round(end[0], 2), round(end[1], 2)) == (3.60, 0.59) and round(float(np.hypot(*(end - pf.GOAL))), 2) == 3.41
N = 40
ia = np.unique(np.linspace(0, len(PA) - 1, N).astype(int))
ib = np.unique(np.linspace(0, len(PB) - 1, N).astype(int))


def frame(k, title, last=False):
    fig = go.Figure()
    dk.room(fig)
    a, b = ia[min(k, len(ia) - 1)], ib[min(k, len(ib) - 1)]
    for P, j, col in ((PA, a, GREEN), (PB, b, RED)):
        fig.add_trace(go.Scatter(x=P[:j + 1, 0], y=P[:j + 1, 1], mode="lines", line=dict(color=col, width=4)))
    dk.disk(fig, *PA[a], np.arctan2(*(pf.GOAL - PA[a])[::-1]))
    dk.disk(fig, *PB[b], np.arctan2(*(pf.GOAL - PB[b])[::-1]))
    dk.point(fig, *pf.GOAL, "black", None, size=12)
    fig.add_annotation(x=2.95, y=4.3, text="door (3.6, 4.0)", xanchor="right", showarrow=False, font=dict(size=18))
    fig.add_annotation(x=1.68, y=1.0, text="start<br>(2, 1)", xanchor="right", showarrow=False,
                       font=dict(size=18, color=GREEN))
    fig.add_annotation(x=4.35, y=0.5, text="start (4.0, 0.5)", xanchor="left", showarrow=False,
                       font=dict(size=18, color=RED))
    lines = [(f"green: {ia[min(k, len(ia) - 1)]} steps so far", GREEN), (f"red: {ib[min(k, len(ib) - 1)]} steps so far", RED)]
    if last:
        lines = [("green: reached the door", GREEN), (f"after {LA:.2f} m of driving", GREEN), ("", "black"),
                 ("red: stopped at (3.60, 0.59),", RED), ("3.41 m from the door,", RED), ("and no step goes downhill", RED)]
    for i, (t, col) in enumerate(lines):
        fig.add_annotation(x=0.74, y=0.92 - 0.075 * i, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           text=t, showarrow=False, font=dict(size=19, color=col))
    fig.update_xaxes(range=[-0.2, 7.2], dtick=1, title="x (m)", showgrid=False, domain=[0, 0.7], constrain="domain")
    fig.update_yaxes(range=[-0.2, 4.45], dtick=1, title="y (m)", showgrid=False, scaleanchor="x", constrain="domain")
    dk.layout(fig, 1300, 640, title, margin=dict(l=70, r=20, t=80, b=60))
    return fig


figs, holds = [frame(0, "two starts, each step downhill from where the robot is")], [8]
for k in range(1, N):
    figs.append(frame(k, "each step downhill from where the robot is"))
    holds.append(1)
figs.append(frame(N, "one robot reaches the door, the other stops", last=True))
holds.append(24)
make_gif(figs, here / "problem", fps=8, holds=holds, keys=[0, 12, len(figs) - 1], cols=1, width=1000)
