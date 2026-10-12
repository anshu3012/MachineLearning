"""Still: the problem and the three planners of this Note side by side, on the disk robot's C-space of the room (light
grey: obstacles grown by 0.25 m). Red star: (3.60, 0.59), where gradient descent on the potential field stopped. Black
dashed: the shortest route from under the table (4.0, 0.5) to the doorway centre, 4.55 m. Left: RRT, 67 samples, route
6.08 m (seed 22). Middle: RRT* after 2,000 samples, 4.79 m (seed 3). Right: RRT-Connect, 27 rounds, 5.40 m (seed 38).
Run -> overview.png (and overview.html)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import rrt
import rrtdraw as rd
from gifkit import FONT, GREEN, PURPLE, RED

here = Path(__file__).parent
a = rrt.rrt(np.random.default_rng(22))
b = rrt.rrt_star(np.random.default_rng(3), n_max=2000)
cc = rrt.rrt_connect(np.random.default_rng(38))
Pa = rrt.path_from(a["nodes"], a["parent"], a["goal"])
Pb = rrt.path_from(b["nodes"], b["parent"], b["goal"])
Pc = rrt.connect_path(cc)
L_star, P_star = rrt.shortest_route()
assert [round(rrt.length(P), 2) for P in (Pa, Pb, Pc)] == [6.08, 4.79, 5.40] and round(L_star, 2) == 4.55
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.03,
                    subplot_titles=("RRT: 67 samples, 6.08 m", "RRT*: 2,000 samples, 4.79 m", "RRT-Connect: 27 rounds, 5.40 m"))
trees = [[(a["nodes"], a["parent"], rd.TREE)], [(b["nodes"], b["parent"], rd.TREE)],
         [(np.array(cc["Ts"][0]), cc["Ts"][1], rd.TREE), (np.array(cc["Tg"][0]), cc["Tg"][1], PURPLE)]]
for col, (P, ts) in enumerate(zip((Pa, Pb, Pc), trees), start=1):
    rd.base(fig, row=1, col=col)
    for N, par, colr in ts:
        fig.add_trace(rd.tree_trace(N, par, color=colr, width=1), row=1, col=col)
    fig.add_trace(go.Scatter(x=P_star[:, 0], y=P_star[:, 1], mode="lines", line=dict(color="black", width=2, dash="dash")),
                  row=1, col=col)
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines", line=dict(color=GREEN, width=4)), row=1, col=col)
    fig.add_trace(go.Scatter(x=[3.6], y=[0.593], mode="markers", marker=dict(symbol="star", size=16, color=RED,
                                                                           line=dict(color="white", width=1))), row=1, col=col)
    fig.add_trace(go.Scatter(x=[rrt.START[0], rrt.GOAL[0]], y=[rrt.START[1], rrt.GOAL[1]], mode="markers",
                             marker=dict(size=9, color="black")), row=1, col=col)
    fig.update_xaxes(range=[-0.15, 7.15], dtick=1, showgrid=False, constrain="domain", row=1, col=col)
    fig.update_yaxes(range=[-0.15, 4.2], dtick=1, showgrid=False, scaleanchor="x" if col == 1 else f"x{col}",
                     constrain="domain", row=1, col=col, showticklabels=col == 1)
fig.update_annotations(font=dict(size=20))
fig.update_layout(template="simple_white", width=1500, height=430, font=FONT, showlegend=False,
                  margin=dict(l=40, r=10, t=50, b=30))
fig.write_image(here / "overview.png", scale=1)
