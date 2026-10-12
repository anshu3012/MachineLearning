"""Animation: RRT-Connect (seed 38). One tree grows from the start under the table (4.0, 0.5, blue), one from the doorway
centre (3.6, 4.0, purple). Each round, one tree takes one RRT step (at most 0.5 m) towards a random sample (orange
star); if it added a node, the other tree CONNECTs: it steps towards that new node again and again until it reaches it
or is blocked. Then the trees swap roles. In round 27 the purple tree reaches the blue tree's new node in 5 steps:
the trees meet, and the route is 5.40 m.
Run -> rrt_connect.gif, rrt_connect_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import drawkit as dk
import rrt
import rrtdraw as rd
from gifkit import GREEN, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
full = rrt.rrt_connect(np.random.default_rng(38), log=True)
Pfull = rrt.connect_path(full)
assert full["samples"] == 27 and round(rrt.length(Pfull), 2) == 5.40 and full["events"][-1]["added_b"] == 5
L_star, P_star = rrt.shortest_route()


def state(n):
    """Trees after round n (rerun: the random numbers are the same)."""
    if n == 0:
        return dict(Ts=([rrt.START], [-1]), Tg=([rrt.GOAL], [-1]), events=[])
    return rrt.rrt_connect(np.random.default_rng(38), n_max=n, log=True)


def frame(n, last=False):
    s, prev = state(n), state(n - 1) if n else None
    fig = rd.base()
    for T, col in ((s["Ts"], rd.TREE), (s["Tg"], PURPLE)):
        fig.add_trace(rd.tree_trace(np.array(T[0]), T[1], color=col, width=2))
        fig.add_trace(rd.nodes_trace(np.array(T[0]), color=col, size=6))
    lines = [(f"round {n}", "black")] if n else [("two trees: one at each end", "black")]
    if n:
        e = s["events"][-1]
        grow, other = ("blue", "purple") if e["a_is_start"] else ("purple", "blue")
        fig.add_trace(go.Scatter(x=[e["q_rand"][0]], y=[e["q_rand"][1]], mode="markers",
                                 marker=dict(symbol="star", size=18, color=ORANGE, line=dict(color="white", width=1))))
        lines += [(f"{grow}: one step to the sample", "black"),
                  (("a node added" if e["added_a"] else "blocked: nothing added"), "black")]
        if e["added_a"]:
            lines += [(f"{other} connects: {e['added_b']} step" + ("s" if e["added_b"] != 1 else ""), "black")]
    nb, npur = len(s["Ts"][0]), len(s["Tg"][0])
    lines += [("", "black"), (f"blue: {nb} node" + ("s" if nb > 1 else "") + f", purple: {npur}", "black")]
    if last:
        fig.add_trace(go.Scatter(x=Pfull[:, 0], y=Pfull[:, 1], mode="lines", line=dict(color=GREEN, width=5)))
        fig.add_trace(go.Scatter(x=P_star[:, 0], y=P_star[:, 1], mode="lines", line=dict(color="black", width=3, dash="dash")))
        lines += [("", "black"), ("the trees meet after 27 rounds", GREEN), (f"route {rrt.length(Pfull):.2f} m (green)", GREEN),
                  (f"shortest {L_star:.2f} m (dashed)", "black")]
    dk.point(fig, *rrt.START, "black", None, size=12)
    dk.point(fig, *rrt.GOAL, "black", None, size=12)
    rd.panel(fig, lines)
    return rd.finish(fig, "RRT-Connect: two trees, and the other tree runs to each new node" if not last else
                     "the trees meet: the route runs from the start to the door")


figs = [frame(n) for n in range(0, 28)] + [frame(27, last=True)]
holds = [8] + [3] * 26 + [8, 30]
make_gif(figs, here / "rrt_connect", fps=4, holds=holds, keys=[0, 3, 27, 28], cols=2, width=1000)
