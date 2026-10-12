"""Animation: the harmonic potential phi on the room's grid of nodes 0.05 m apart (5,840 free nodes, light dots): every
free node is the average of its four neighbours, obstacle nodes are held at 1 and the doorway centre at 0 (solved
exactly in the notebook; Gauss-Seidel sweeps agree to 4e-11 after 5,000 sweeps). From each start the robot steps to
its lowest neighbouring node (of 8). Under the table, at (4.0, 0.5), phi = 1 - 1.9e-9; the robot reaches the door in
91 steps, 5.61 m. From (2, 1), phi = 1 - 4.8e-5; 60 steps, 3.75 m. The right panel shows phi at each robot.
Run -> harmonic.gif, harmonic_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import cspace as c
import drawkit as dk
import pf
from gifkit import GREEN, RED, make_gif

here = Path(__file__).parent
xs, ys, fr, g, phi = pf.harmonic_solve()
PB, okb = pf.grid_descent(phi, fr, pf.START2)
PA, oka = pf.grid_descent(phi, fr, pf.START)
assert okb and oka and len(PB) - 1 == 91 and len(PA) - 1 == 60 and fr.sum() == 5840
assert round(pf.path_length(PB), 2) == 5.61 and round(pf.path_length(PA), 2) == 3.75
val = lambda p: phi[int(round(p[1] / pf.H_GRID)), int(round(p[0] / pf.H_GRID))]
assert f"{1 - val(pf.START2):.1e}" == "1.9e-09" and f"{1 - val(pf.START):.1e}" == "4.8e-05"
COBS = c.cobs_disk()
X, Y = np.meshgrid(xs, ys)


def sci(p):
    """phi at a node, written so that values a hair below 1 stay readable."""
    v = 1 - p
    if v >= 0.01:
        return f"φ = {p:.3f}"
    m, e = f"{v:.1e}".split("e")
    return f"φ = 1 − {m} × 10<sup>{int(e)}</sup>"


def frame(title, ka, kb, lines):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X[fr], y=Y[fr], mode="markers", marker=dict(size=2, color="rgba(76,120,168,0.35)"),
                             hoverinfo="skip"))
    fig.add_trace(dk.geom_trace(COBS.intersection(c.box(-0.1, -0.1, 7.1, 4.1)), "rgba(200,200,200,1)", "rgba(150,150,150,1)", 1))
    dk.room(fig)
    for P, k, col in ((PA, ka, GREEN), (PB, kb, RED)):
        fig.add_trace(go.Scatter(x=P[:k + 1, 0], y=P[:k + 1, 1], mode="lines", line=dict(color=col, width=4)))
        dk.point(fig, *P[k], col, None, size=15)
    dk.point(fig, *pf.GOAL, "black", None, size=12)
    for i, (t, col) in enumerate(lines):
        fig.add_annotation(x=0.75, y=0.92 - 0.07 * i, xref="paper", yref="paper", xanchor="left", yanchor="top", text=t,
                           showarrow=False, font=dict(size=19, color=col))
    fig.update_xaxes(range=[-0.15, 7.15], dtick=1, title="x (m)", showgrid=False, domain=[0, 0.72], constrain="domain")
    fig.update_yaxes(range=[-0.15, 4.2], dtick=1, title="y (m)", showgrid=False, scaleanchor="x", constrain="domain")
    dk.layout(fig, 1300, 620, title, margin=dict(l=70, r=20, t=80, b=60))
    return fig


figs, holds = [], []
steps = list(range(0, len(PB), 3)) + [len(PB) - 1]
for j, kb in enumerate(steps):
    ka = min(kb, len(PA) - 1)
    first, last = j == 0, j == len(steps) - 1
    lines = [("the potential at each robot:", "black"), (f"red: {sci(val(PB[kb]))}", RED), (f"green: {sci(val(PA[ka]))}", GREEN),
             ("", "black"), ("each step: to the lowest", "black"), ("of the 8 neighbouring nodes", "black")]
    if last:
        lines += [("", "black"), ("both reach the door, where φ = 0;", "black"), ("red 91 steps, 5.61 m", RED),
                  ("green 60 steps, 3.75 m", GREEN), ("(the red path joins the green one)", "black")]
    figs.append(frame("the harmonic potential: from every node one neighbour is lower" if not last else
                      "no local minimum: both robots reach the door", ka, kb, lines))
    holds.append(12 if first else 1)
holds[-1] = 30
make_gif(figs, here / "harmonic", fps=8, holds=holds, keys=[0, 12, len(figs) - 1], cols=1, width=1000)
