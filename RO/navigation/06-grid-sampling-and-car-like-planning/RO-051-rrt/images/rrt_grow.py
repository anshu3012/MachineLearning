"""Animation: RRT growing from the robot's start under the table, (4.0, 0.5), to the doorway centre (3.6, 4.0), in the
disk robot's C-space (light grey: obstacles grown by 0.25 m). Samples 1 to 4 are shown stage by stage: a random sample
(orange star), its nearest tree node (circled), steer at most 0.5 m towards it, the edge checked at 11 points 0.05 m
apart, then the new node added (green) or thrown away (red cross). Sample 1: (1.395, 0.354), nearest the start, 2.609 m
away, new node (3.501, 0.472). Sample 2 lands near the door; its new node (3.46, 0.97) is inside the table's band:
rejected. Then one sample per frame. Sample 67 is the goal itself (goal bias 5 percent); the tree reaches the door
with 41 nodes after 67 samples (28 rejected) and 465 collision checks; the route is 6.08 m (shortest: 4.55 m, dashed).
Run -> rrt_grow.gif, rrt_grow_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import drawkit as dk
import rrt
import rrtdraw as rd
from gifkit import GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
rrt.Counter.checks = 0
res = rrt.rrt(np.random.default_rng(22), log=True)
checks = rrt.Counter.checks
ev, nodes, parent = res["events"], res["nodes"], res["parent"]
P = rrt.path_from(nodes, parent, res["goal"])
L_star, P_star = rrt.shortest_route()
assert res["samples"] == 67 and len(nodes) == 41 and sum(not e["ok"] for e in ev) == 28 and checks == 465
assert round(rrt.length(P), 2) == 6.08 and round(L_star, 2) == 4.55
e1, e2 = ev[0], ev[1]
assert np.allclose(e1["q_rand"], (1.395, 0.354), atol=5e-4) and np.allclose(e1["q_new"], (3.501, 0.472), atol=5e-4)
assert round(float(np.hypot(*(e1["q_rand"] - rrt.START))), 3) == 2.609 and not e2["ok"]
assert np.allclose(e2["q_new"], (3.46, 0.97), atol=5e-3) and ev[-1]["goal_sample"]
acc = np.cumsum([e["ok"] for e in ev])          # nodes added after each sample (goal node not counted here)


def frame(i, stage, title):
    """State after sample i - 1, then sample i at a stage: 0 sample, 1 nearest, 2 steer + check, 3 result."""
    e = ev[i - 1]
    n_before = 1 + (acc[i - 2] if i > 1 else 0)
    fig = rd.base()
    fig.add_trace(rd.tree_trace(nodes, parent, upto=n_before))
    fig.add_trace(rd.nodes_trace(nodes[:n_before]))
    q_near = nodes[e["near"]]
    if stage >= 1:
        fig.add_trace(go.Scatter(x=[q_near[0], e["q_rand"][0]], y=[q_near[1], e["q_rand"][1]], mode="lines",
                                 line=dict(color=ORANGE, width=2, dash="dot")))
        fig.add_trace(go.Scatter(x=[q_near[0]], y=[q_near[1]], mode="markers",
                                 marker=dict(size=20, color="rgba(0,0,0,0)", line=dict(color=ORANGE, width=3))))
    if stage >= 2:
        col = GREEN if e["ok"] else RED
        t = np.linspace(0, 1, 11)[:, None]
        pts = q_near + t * (e["q_new"] - q_near)
        ok = rrt.free_pts(pts)
        fig.add_trace(go.Scatter(x=[q_near[0], e["q_new"][0]], y=[q_near[1], e["q_new"][1]], mode="lines",
                                 line=dict(color=col, width=4)))
        if stage == 2:
            fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="markers",
                                     marker=dict(size=7, color=[GREEN if o else RED for o in ok])))
        fig.add_trace(go.Scatter(x=[e["q_new"][0]], y=[e["q_new"][1]], mode="markers",
                                 marker=dict(size=13 if e["ok"] else 16, color=col, symbol="circle" if e["ok"] else "x")))
    fig.add_trace(go.Scatter(x=[e["q_rand"][0]], y=[e["q_rand"][1]], mode="markers",
                             marker=dict(symbol="star", size=20, color=ORANGE, line=dict(color="white", width=1))))
    dk.point(fig, *rrt.START, "black", None, size=12)
    dk.point(fig, *rrt.GOAL, "black", None, size=12)
    n_now = n_before + (1 if (stage == 3 and e["ok"]) else 0)
    rej = sum(not x["ok"] for x in ev[:i - (0 if stage == 3 else 1)])
    lines = [(f"sample {i}" + (" (the goal itself)" if e["goal_sample"] else ""), "black"),
             (f"tree: {n_now} node" + ("s" if n_now > 1 else ""), "black"), (f"rejected so far: {rej}", "black"), ("", "black")]
    words = {0: [("orange star: a random sample", ORANGE)],
             1: [("circled: the nearest node", ORANGE), (f"{np.hypot(*(e['q_rand'] - q_near)):.3f} m away", ORANGE)],
             2: [("steer: at most 0.5 m towards it;", "black"), ("check the edge at 11 points", "black")],
             3: [("free: add the node and edge", GREEN) if e["ok"] else ("blocked: throw it away", RED)]}
    rd.panel(fig, lines + words[stage])
    return rd.finish(fig, title)


figs, holds, keys = [], [], []
for i in (1, 2, 3, 4):
    for stage, name in enumerate(("a random sample", "its nearest node", "steer and check", "add or reject")):
        figs.append(frame(i, stage, f"sample {i}: {name}"))
        holds.append(5 if i <= 2 else 3)
        if (i, stage) in ((1, 2), (2, 3)):
            keys.append(len(figs) - 1)
for i in range(5, res["samples"] + 1):
    figs.append(frame(i, 3, "one sample per frame"))
    holds.append(2)
    if i == 35:
        keys.append(len(figs) - 1)
# last frame: the route through the tree and the shortest route
fig = rd.base()
fig.add_trace(rd.tree_trace(nodes, parent))
fig.add_trace(rd.nodes_trace(nodes))
fig.add_trace(go.Scatter(x=P_star[:, 0], y=P_star[:, 1], mode="lines", line=dict(color="black", width=3, dash="dash")))
fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines+markers", line=dict(color=GREEN, width=5),
                         marker=dict(size=8, color=GREEN)))
dk.point(fig, *rrt.START, "black", None, size=12)
dk.point(fig, *rrt.GOAL, "black", None, size=12)
rd.panel(fig, [("reached the door after", "black"), (f"{res['samples']} samples, {len(nodes)} nodes", "black"),
               ("(28 samples rejected)", "black"), (f"{checks} collision checks", "black"), ("", "black"),
               (f"green: the route, {rrt.length(P):.2f} m", GREEN), (f"dashed: the shortest, {L_star:.2f} m", "black")])
figs.append(rd.finish(fig, "the route: follow the parents from the door back to the start"))
holds.append(30)
keys.append(len(figs) - 1)
make_gif(figs, here / "rrt_grow", fps=6, holds=holds, keys=keys, cols=2, width=1000)
