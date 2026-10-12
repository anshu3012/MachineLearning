"""Animation: the contour map of the total potential U over the whole room (colours and contour lines as in the top
view of the field animation; light grey: obstacles with their 0.25 m band, where U is infinite). 82 robots start on a
0.4 m grid of free points and all follow the gradient downhill at once. Those between the table and the bottom wall
end in the local minimum at (3.60, 0.59); all others reach the doorway. The last frame colours a start every 0.1 m by where it
ends: red, the starts that roll into the local minimum (7.7 percent of the starts); black crosses, the three saddle points.
Run -> basin.gif, basin_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import cspace as c
import drawkit as dk
import pf
from gifkit import FONT, GREEN, RED, make_gif

here = Path(__file__).parent
xs, ys, U = pf.u_grid(0.04)
Zc = np.where(np.isfinite(U), np.minimum(U, 10), 10.0)    # inside obstacles: drawn grey on top
COBS = c.cobs_disk()


def ends_of(step):
    S = [np.array([x, y]) for y in np.arange(step / 2, c.H, step) for x in np.arange(step / 2, c.W, step)]
    S = [q for q in S if pf.free(q)]
    P = [pf.descend(q, n_max=3000, tol=1e-4) for q in S]
    trap = np.array([np.hypot(*(p[-1] - pf.TRAP)) < 0.1 for p in P])
    assert all(t or np.hypot(*(p[-1] - pf.GOAL)) < 0.1 for t, p in zip(trap, P))
    return S, P, trap


S, P, trap = ends_of(0.4)
S2, _, trap2 = ends_of(0.1)
share = trap2.mean()
assert len(S) == 82 and trap.sum() == 6 and len(S2) == 1529 and round(100 * share, 1) == 7.7
L = max(len(p) for p in P)


def base(title):
    fig = go.Figure(go.Contour(x=xs, y=ys, z=Zc, colorscale="Blues", reversescale=True, zmin=0, zmax=10,
                               contours=dict(start=0, end=10, size=1, coloring="fill"),
                               line=dict(color="rgba(30,30,30,0.45)", width=1), showscale=False, hoverinfo="skip"))
    fig.add_trace(dk.geom_trace(COBS.intersection(c.box(-0.1, -0.1, 7.1, 4.1)), "rgba(200,200,200,1)", "rgba(150,150,150,1)", 1))
    dk.room(fig)
    dk.point(fig, *pf.GOAL, "black", None, size=12)
    fig.update_xaxes(range=[-0.15, 7.15], dtick=1, title="x (m)", showgrid=False, domain=[0, 0.72], constrain="domain")
    fig.update_yaxes(range=[-0.15, 4.2], dtick=1, title="y (m)", showgrid=False, scaleanchor="x", constrain="domain")
    dk.layout(fig, 1300, 620, title, margin=dict(l=70, r=20, t=80, b=60))
    return fig


figs, holds = [], []
for t in list(range(0, 60, 3)) + list(range(60, L, max(1, (L - 60) // 20))) + [L - 1]:
    fig = base("82 robots follow the gradient downhill at once" if t else "82 starts, 0.4 m apart")
    pos = np.array([p[min(t, len(p) - 1)] for p in P])
    col = ["black"] * len(P) if t < L - 1 else [RED if tr else GREEN for tr in trap]
    fig.add_trace(go.Scatter(x=pos[:, 0], y=pos[:, 1], mode="markers", marker=dict(size=11, color=col,
                                                                                    line=dict(color="white", width=1))))
    figs.append(fig)
    holds.append(1)
holds[0], holds[-1] = 8, 12
fig = base("where each start ends: red, the starts that roll into the local minimum")
S2 = np.array(S2)
fig.add_trace(go.Scatter(x=S2[~trap2, 0], y=S2[~trap2, 1], mode="markers", marker=dict(size=3, color=GREEN, opacity=0.7)))
fig.add_trace(go.Scatter(x=S2[trap2, 0], y=S2[trap2, 1], mode="markers", marker=dict(size=5, color=RED)))
sx, sy = zip(*pf.SADDLES)
fig.add_trace(go.Scatter(x=sx, y=sy, mode="markers", marker=dict(symbol="x", size=16, color="black")))
fig.add_trace(go.Scatter(x=[pf.TRAP[0]], y=[pf.TRAP[1]], mode="markers", marker=dict(symbol="star", size=20, color=RED,
                                                                                         line=dict(color="white", width=1))))
for i, (t, col) in enumerate([("a start every 0.1 m, coloured", "black"), ("by where it ends:", "black"), ("", "black"),
                              ("red: in the local minimum,", RED), (f"{100 * share:.1f} percent of starts", RED), ("", "black"),
                              ("green: at the door", GREEN), ("", "black"), ("star: the local minimum", RED),
                              ("crosses: saddle points", "black")]):
    fig.add_annotation(x=0.75, y=0.92 - 0.07 * i, xref="paper", yref="paper", xanchor="left", yanchor="top", text=t,
                       showarrow=False, font=dict(size=19, color=col))
figs.append(fig)
holds.append(30)
make_gif(figs, here / "basin", fps=8, holds=holds, keys=[0, len(figs) - 1], cols=2, width=900)
