"""Animation: why random samples explore. Left, RRT without goal bias; right, the random-walk tree of MR 10.5, which
picks a random node of the tree and steps 0.5 m in a random direction. Both start under the table at (4.0, 0.5) and
grow to 100 nodes, a few nodes per frame. The panel titles give the share of the free floor within 0.5 m of some node:
after 100 nodes about 95 percent for RRT and 27 percent for the random walk (mean of 20 seeds; this run is seed 0).
Run -> rrt_walk.gif, rrt_walk_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import drawkit as dk
import rrt
import rrtdraw as rd
from gifkit import FONT, make_gif

here = Path(__file__).parent
R = rrt.rrt(np.random.default_rng(0), n_max=100000, stop_at_goal=False, bias=0.0, n_nodes=100)
W = rrt.walk_tree(np.random.default_rng(0), 100)
cr = [rrt.coverage(rrt.rrt(np.random.default_rng(s), n_max=100000, stop_at_goal=False, bias=0.0, n_nodes=100)["nodes"])
      for s in range(20)]
cw = [rrt.coverage(rrt.walk_tree(np.random.default_rng(s), 100)["nodes"]) for s in range(20)]
assert round(100 * np.mean(cr)) == 95 and round(100 * np.mean(cw)) == 27
steps = [1, 2, 3, 5, 8, 12, 16, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]


def frame(n):
    a = 100 * rrt.coverage(R["nodes"][:n])
    b = 100 * rrt.coverage(W["nodes"][:n])
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06,
                        subplot_titles=(f"RRT: {n} nodes, {a:.0f} percent of the floor within 0.5 m",
                                        f"random walk: {n} nodes, {b:.0f} percent"))
    for col, T in ((1, R), (2, W)):
        rd.base(fig, row=1, col=col)
        fig.add_trace(rd.tree_trace(T["nodes"], T["parent"], upto=n), row=1, col=col)
        fig.add_trace(rd.nodes_trace(T["nodes"][:n]), row=1, col=col)
        fig.add_trace(go.Scatter(x=[rrt.START[0]], y=[rrt.START[1]], mode="markers", marker=dict(size=12, color="black")),
                      row=1, col=col)
        fig.update_xaxes(range=[-0.15, 7.15], dtick=1, title="x (m)", showgrid=False, constrain="domain", row=1, col=col)
        fig.update_yaxes(range=[-0.15, 4.2], dtick=1, title="y (m)" if col == 1 else None, showgrid=False,
                         scaleanchor="x" if col == 1 else "x2", constrain="domain", row=1, col=col)
    fig.update_annotations(font=dict(size=20))
    fig.update_layout(template="simple_white", width=1400, height=520, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=70, b=60))
    return fig


figs = [frame(n) for n in steps]
holds = [6] + [2] * (len(steps) - 2) + [30]
make_gif(figs, here / "rrt_walk", fps=4, holds=holds, keys=[3, 13, len(figs) - 1], cols=1, width=1000)
