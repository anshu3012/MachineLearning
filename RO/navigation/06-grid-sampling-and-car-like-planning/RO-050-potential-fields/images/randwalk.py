"""Animation: the randomized potential field (LaValle 5.4.3) frees the robot stuck at (3.60, 0.59), U = 6.003, on the
contour map of the total potential (as in the basin animation). Random walk 1 (limit 384 steps, drawn at random from
100 to 400): each step moves x and y by 0.05 m up or down by a coin toss; it ends at (4.90, 0.49), still among the starts
that roll into the local minimum, and gradient descent rolls back into it. Random walk 2 stops after 132 steps at (2.70, 0.69), where U has
fallen below 6.003; gradient descent from there reaches the doorway. 42.0 m driven in all (seed 7).
Run -> randwalk.gif, randwalk_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import cspace as c
import drawkit as dk
import pf
from gifkit import GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
parts = pf.randomized(pf.START2, np.random.default_rng(7))
modes = [m for m, _ in parts]
assert modes == ["descend", "walk", "descend", "walk", "descend"]
w1, d1, w2, d2 = (p for _, p in parts[1:])
assert len(w1) - 1 == 384 and len(w2) - 1 == 132
assert np.allclose(w1[-1], (4.90, 0.49), atol=0.006) and np.allclose(w2[-1], (2.70, 0.69), atol=0.006)
assert np.hypot(*(d1[-1] - pf.TRAP)) < 0.02 and np.hypot(*(d2[-1] - pf.GOAL)) < 0.03
assert pf.U(w2[-1]) < 6.003 < pf.U(w2[-2])
total = pf.path_length(np.vstack([p for _, p in parts]))
assert round(total, 1) == 42.0 and round(pf.shortest_route()[0], 2) == 4.55
xs, ys, U = pf.u_grid(0.04)
Zc = np.where(np.isfinite(U), np.minimum(U, 10), 10.0)    # inside obstacles: drawn grey on top
COBS = c.cobs_disk()
done_len = 0.0


def frame(title, trails, robot, lines):
    fig = go.Figure(go.Contour(x=xs, y=ys, z=Zc, colorscale="Blues", reversescale=True, zmin=0, zmax=10,
                               contours=dict(start=0, end=10, size=1, coloring="fill"),
                               line=dict(color="rgba(30,30,30,0.45)", width=1), showscale=False, hoverinfo="skip"))
    fig.add_trace(dk.geom_trace(COBS.intersection(c.box(-0.1, -0.1, 7.1, 4.1)), "rgba(200,200,200,1)", "rgba(150,150,150,1)", 1))
    dk.room(fig)
    for P, col, w in trails:
        fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines", line=dict(color=col, width=w)))
    fig.add_trace(go.Scatter(x=[pf.TRAP[0]], y=[pf.TRAP[1]], mode="markers",
                             marker=dict(symbol="star", size=20, color=RED, line=dict(color="white", width=1))))
    dk.point(fig, *pf.GOAL, "black", None, size=12)
    dk.point(fig, *robot, "black", None, size=15)
    for i, (t, col) in enumerate(lines):
        fig.add_annotation(x=0.75, y=0.92 - 0.07 * i, xref="paper", yref="paper", xanchor="left", yanchor="top", text=t,
                           showarrow=False, font=dict(size=19, color=col))
    fig.update_xaxes(range=[-0.15, 7.15], dtick=1, title="x (m)", showgrid=False, domain=[0, 0.72], constrain="domain")
    fig.update_yaxes(range=[-0.15, 4.2], dtick=1, title="y (m)", showgrid=False, scaleanchor="x", constrain="domain")
    dk.layout(fig, 1300, 620, title, margin=dict(l=70, r=20, t=80, b=60))
    return fig


figs, holds = [], []
figs.append(frame("stopped at a local minimum: every small step goes uphill", [], pf.TRAP,
                  [("star: the local minimum (3.60, 0.59)", RED), ("U = 6.003 here", RED), ("", "black"),
                   ("next: a random walk", "black")]))
holds.append(10)
for k in list(range(12, len(w1), 12)) + [len(w1) - 1]:
    figs.append(frame("random walk 1: each step 0.05 m in x and in y, by coin tosses", [(w1[:k + 1], GREY, 2)], w1[k],
                      [("random walk 1", "black"), (f"step {k} of at most 384", "black"),
                       (f"U now: {pf.U(w1[k]):.3f}", "black"), ("ends early if U < 6.003", "black")]))
    holds.append(1)
holds[-1] = 6
for k in list(range(0, len(d1), 60)) + [len(d1) - 1]:
    figs.append(frame("walk 1 ended where downhill leads back to the local minimum", [(w1, GREY, 1), (d1[:k + 1], ORANGE, 4)],
                      d1[k], [("gradient descent", "black"), (f"U now: {pf.U(d1[k]):.3f}", "black"),
                              ("back in the local minimum:", RED) if k == len(d1) - 1 else ("", "black"),
                              ("walk 1 failed", RED) if k == len(d1) - 1 else ("", "black")]))
    holds.append(1)
holds[-1] = 8
for k in list(range(6, len(w2), 6)) + [len(w2) - 1]:
    last = k == len(w2) - 1
    figs.append(frame("random walk 2" + (": U fell below 6.003, so it stops" if last else ""),
                      [(w1, GREY, 1), (d1, ORANGE, 2), (w2[:k + 1], "black", 2)], w2[k],
                      [("random walk 2", "black"), (f"step {k}", "black"), (f"U now: {pf.U(w2[k]):.3f}", "black"),
                       ("below 6.003: it cannot roll back" if last else "ends early if U < 6.003", GREEN if last else "black")]))
    holds.append(1)
holds[-1] = 8
idx = list(range(0, len(d2), 30)) + [len(d2) - 1]
for k in idx:
    last = k == len(d2) - 1
    figs.append(frame("downhill from there reaches the door" if last else "gradient descent again",
                      [(w1, GREY, 1), (d1, ORANGE, 2), (w2, "black", 1), (d2[:k + 1], GREEN, 4)], d2[k],
                      [("gradient descent", "black"), (f"U now: {pf.U(d2[k]):.3f}", "black")] +
                      ([("", "black"), ("at the door after 2 walks", GREEN), (f"{total:.1f} m driven in all", GREEN),
                        ("(the shortest route: 4.55 m)", "black")] if last else [])))
    holds.append(1)
holds[-1] = 30
make_gif(figs, here / "randwalk", fps=8, holds=holds, keys=[0, 16, 33, 46, 69, len(figs) - 1], cols=2, width=1000)
