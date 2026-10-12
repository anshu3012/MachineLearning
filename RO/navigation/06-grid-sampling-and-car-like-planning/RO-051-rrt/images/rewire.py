"""Animation: one RRT* step up close (seed 3, sample 119), zoomed on the left of the table. The sample (2.410, 3.212)
is within 0.5 m of its nearest node B, so it becomes the new node. Three tree nodes lie within r = 0.5 m: A, B, C.
Choose the parent: cost from the start through each (cost of the node + edge length): A 4.220 + 0.383 = 4.603,
B 4.711 + 0.259 = 4.970, C 5.211 + 0.454 = 5.665; A is cheapest though B is nearest. Rewire: C costs 5.211 through
its parent B, but 4.603 + 0.454 = 5.057 through the new node, so C changes parent. The route to the door shortens
from 6.599 m to 6.445 m, by the same 0.154 m. Costs shown are sums of the rounded parts.
Run -> rewire.gif, rewire_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import drawkit as dk
import rrt
import rrtdraw as rd
from gifkit import GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
r0 = rrt.rrt_star(np.random.default_rng(3), n_max=118)
r1 = rrt.rrt_star(np.random.default_rng(3), n_max=119, log=True)
e = r1["events"][-1]
N, C, Pa = r0["nodes"], r0["cost"], r0["parent"]
A, B, Cn = 12, 16, 21
assert sorted(e["near_set"]) == [A, B, Cn] and e["near"] == B and e["parent"] == A and e["rewired"] == [(Cn, B)]
q = e["q_new"]
rd3 = lambda v: round(float(v), 3)
cA, cB, cC = rd3(C[A]), rd3(C[B]), rd3(C[Cn])
dA, dB, dC = (rd3(np.hypot(*(N[k] - q))) for k in (A, B, Cn))
assert (cA, dA, cB, dB, cC, dC) == (4.220, 0.383, 4.711, 0.259, 5.211, 0.454)
new = rd3(cA + dA)
assert new == 4.603 and rd3(new + dC) == 5.057 and rd3(cC - (new + dC)) == 0.154
g0, g1 = rd3(C[r0["goal"]]), rd3(r1["cost"][r1["goal"]])
assert (g0, g1) == (6.599, 6.445) and rd3(g0 - g1) == 0.154
P0 = rrt.path_from(r0["nodes"], r0["parent"], r0["goal"])
P1 = rrt.path_from(r1["nodes"], r1["parent"], r1["goal"])
X0, X1, Y0, Y1 = 1.55, 3.85, 2.25, 4.1
labels = {A: "A", B: "B", Cn: "C"}


def frame(stage, title, lines):
    fig = rd.base()
    nodes, par = (r1["nodes"], r1["parent"]) if stage >= 4 else (N, Pa)
    fig.add_trace(rd.tree_trace(nodes, par, width=2))
    fig.add_trace(rd.nodes_trace(N, size=7))
    route = P1 if stage >= 5 else P0
    fig.add_trace(go.Scatter(x=route[:, 0], y=route[:, 1], mode="lines", line=dict(color=GREEN, width=6),
                             opacity=0.35))
    fig.add_trace(go.Scatter(x=[q[0]], y=[q[1]], mode="markers",
                             marker=dict(symbol="star", size=22, color=ORANGE, line=dict(color="white", width=1))))
    if stage == 1:
        fig.add_trace(go.Scatter(x=[N[B][0], q[0]], y=[N[B][1], q[1]], mode="lines", line=dict(color=ORANGE, width=3, dash="dot")))
    if stage >= 2:
        t = np.linspace(0, 2 * np.pi, 120)
        fig.add_trace(go.Scatter(x=q[0] + 0.5 * np.cos(t), y=q[1] + 0.5 * np.sin(t), mode="lines",
                                 line=dict(color=ORANGE, width=2, dash="dash")))
    if stage == 3:
        for k, col in ((B, GREY), (Cn, GREY), (A, GREEN)):
            fig.add_trace(go.Scatter(x=[N[k][0], q[0]], y=[N[k][1], q[1]], mode="lines",
                                     line=dict(color=col, width=5 if col == GREEN else 3, dash=None if col == GREEN else "dot")))
    if stage >= 4:
        fig.add_trace(go.Scatter(x=[N[A][0], q[0]], y=[N[A][1], q[1]], mode="lines", line=dict(color=GREEN, width=5)))
        fig.add_trace(go.Scatter(x=[q[0], N[Cn][0]], y=[q[1], N[Cn][1]], mode="lines", line=dict(color=GREEN, width=5)))
        if stage == 4:
            fig.add_trace(go.Scatter(x=[N[B][0], N[Cn][0]], y=[N[B][1], N[Cn][1]], mode="lines",
                                     line=dict(color=RED, width=4, dash="dash")))
    for k, s in labels.items():
        fig.add_annotation(x=N[k][0] - 0.07, y=N[k][1] + 0.06, text=s, showarrow=False, xanchor="right",
                           font=dict(size=22, color="black"))
    rd.panel(fig, lines, x=0.62, size=19)
    fig.update_layout(xaxis=dict(range=[X0, X1], dtick=0.5, title="x (m)", showgrid=False, domain=[0, 0.58], constrain="domain"),
                      yaxis=dict(range=[Y0, Y1], dtick=0.5, title="y (m)", showgrid=False, scaleanchor="x", constrain="domain"))
    dk.layout(fig, 1300, 700, title, margin=dict(l=70, r=20, t=80, b=60))
    return fig


cost = lambda k, c, d: (f"{k}: {c:.3f} + {d:.3f} = {c + d:.3f}", "black")
figs = [
    frame(0, "RRT*, sample 119", [("sample: (2.410, 3.212)", ORANGE), ("green: the route to the door so far,", GREEN),
                                  (f"{g0:.3f} m", GREEN)]),
    frame(1, "steer as in RRT", [("nearest node: B, 0.259 m away", "black"), ("closer than 0.5 m, so the sample", "black"),
                                 ("itself is the new node", "black")]),
    frame(2, "the nodes within r = 0.5 m", [("inside the dashed circle:", "black"), ("A, B and C", "black")]),
    frame(3, "choose the parent: the cheapest route from the start",
          [("cost from the start through each:", "black"), ("(node's cost + edge length, m)", "black"),
           cost("A", cA, dA), cost("B", cB, dB), cost("C", cC, dC), ("", "black"),
           ("A is cheapest, though B is nearest", GREEN), (f"new node's cost: {new:.3f}", GREEN)]),
    frame(4, "rewire: does a neighbour get cheaper through the new node?",
          [("C now: 5.211 through B", "black"), (f"C through the new node:", "black"), (f"{new:.3f} + {dC:.3f} = {new + dC:.3f}", GREEN),
           ("cheaper: C's parent becomes the new node", GREEN), ("(red dashed: the edge B to C is dropped)", RED)]),
    frame(5, "the route to the door shortens", [("C saves", "black"), (f"{cC:.3f} − {new + dC:.3f} = {cC - new - dC:.3f} m", GREEN),
                                               ("so does every node after C:", "black"),
                                               (f"route {g0:.3f} → {g1:.3f} m", GREEN)]),
]
holds = [10, 10, 10, 18, 18, 30]
make_gif(figs, here / "rewire", fps=2, holds=holds, keys=[1, 3, 4, 5], cols=2, width=1000)
