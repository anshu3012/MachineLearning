"""Animation: RRT* from under the table (4.0, 0.5) to the doorway centre (3.6, 4.0), seed 3. Each frame is the tree after
a number of samples; green: the best route to the door so far; dashed: the shortest route, 4.55 m. Right: the best
route's length against the number of samples. The first route appears at sample 63, 6.61 m; rewiring shortens it to
6.32 m at 200 samples, 5.15 m at 500, 4.87 m at 1,000 and 4.79 m at 2,000.
Run -> rrt_star.gif, rrt_star_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import drawkit as dk
import rrt
import rrtdraw as rd
from gifkit import GREEN, make_gif

here = Path(__file__).parent
SNAP = [63, 75, 100, 150, 200, 300, 400, 500, 700, 1000, 1500, 2000]
full = rrt.rrt_star(np.random.default_rng(3), n_max=2000, record=tuple(range(1, 2001)))
best = full["best"]
L_star, P_star = rrt.shortest_route()
assert np.isinf(best[62]) and round(best[63], 2) == 6.61 and round(best[200], 2) == 6.32 and round(best[500], 2) == 5.15
assert round(best[1000], 2) == 4.87 and round(best[2000], 2) == 4.79 and round(L_star, 2) == 4.55
xs = np.arange(63, 2001)
ys = np.array([best[k] for k in xs])


def frame(n):
    r = rrt.rrt_star(np.random.default_rng(3), n_max=n)
    P = rrt.path_from(r["nodes"], r["parent"], r["goal"])
    assert abs(rrt.length(P) - best[n]) < 1e-9
    fig = rd.base()
    fig.add_trace(rd.tree_trace(r["nodes"], r["parent"], width=1))
    fig.add_trace(go.Scatter(x=P_star[:, 0], y=P_star[:, 1], mode="lines", line=dict(color="black", width=3, dash="dash")))
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines", line=dict(color=GREEN, width=5)))
    dk.point(fig, *rrt.START, "black", None, size=12)
    dk.point(fig, *rrt.GOAL, "black", None, size=12)
    m = xs <= n
    fig.add_trace(go.Scatter(x=xs[m], y=ys[m], mode="lines", line=dict(color=GREEN, width=3), xaxis="x2", yaxis="y2"))
    fig.add_trace(go.Scatter(x=[63, 2000], y=[L_star, L_star], mode="lines", line=dict(color="black", width=2, dash="dash"),
                             xaxis="x2", yaxis="y2"))
    fig.add_trace(go.Scatter(x=[n], y=[best[n]], mode="markers", marker=dict(size=11, color=GREEN), xaxis="x2", yaxis="y2"))
    rd.panel(fig, [(f"{n} samples, {len(r['nodes'])} nodes", "black"), (f"best route: {best[n]:.2f} m", GREEN),
                   (f"shortest: {L_star:.2f} m (dashed)", "black")], x=0.72, y0=0.97, dy=0.07)
    fig = rd.finish(fig, "RRT*: every new node picks its cheapest parent and rewires its neighbours", domain=0.62)
    fig.update_layout(xaxis2=dict(domain=[0.72, 1.0], anchor="y2", range=[0, 2050], title="samples", dtick=500,
                                  showgrid=False),
                      yaxis2=dict(domain=[0.12, 0.66], anchor="x2", range=[4.3, 7.0], title="best route (m)", dtick=0.5,
                                  showgrid=False))
    return fig


figs = [frame(n) for n in SNAP]
holds = [8] + [4] * (len(SNAP) - 2) + [30]
make_gif(figs, here / "rrt_star", fps=4, holds=holds, keys=[0, 4, 7, len(figs) - 1], cols=2, width=1000)
