"""Animation: the kinodynamic RRT growing in the room (seed 4, a run with a typical node count). Each iteration
samples a pose (red cross with its heading; 1 in 10 samples is the goal pose itself), takes the tree node nearest to
it by RO-038's distance (metres plus 0.25 m per radian), simulates the three primitives from that node for 0.75 s
(grey), and keeps the one whose end comes closest to the sample: green if its swept path stays in free space (added
to the tree), red if it would hit an obstacle grown by 0.25 m (thrown away). The first 12 iterations are shown one
per frame, then 15 per frame. After 221 iterations (147 thrown away) a node lands in the goal region, within 0.25 m
and 25 degrees of (3.6, 3.5) facing 90 degrees; the tree has 75 nodes and the path to the goal (blue) is 8 primitives,
3.0 m, every one of them drivable at 0.5 m/s. Run -> rrt_anim.gif, rrt_anim_frames.png"""
import math
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

import drawkit as k
import motionkit as m
from gifkit import BLUE, GREEN, PURPLE, RED, make_gif

here = Path(__file__).parent
R = m.kino_rrt(seed=4)
LOG = R["log"]
assert R["reached"] and len(R["nodes"]) == 75 and len(LOG) == 221 and sum(not e["ok"] for e in LOG) == 147
assert len(R["path"]) - 1 == 8 and R["length"] == 3.0
G = m.DOOR_POSE


def frame(it, detail=True, final=False):
    """State after iteration `it` (0 = only the start); detail draws iteration `it`'s sample and candidates."""
    fig = make_subplots(rows=1, cols=1)
    k.room(fig, grown=True)
    a = np.linspace(0, 2 * math.pi, 60)
    k.line(fig, G[0] + 0.25 * np.cos(a), G[1] + 0.25 * np.sin(a), color=PURPLE, width=2, dash="dash")
    k.arrow(fig, G[0], G[1], G[2], length=0.3, color=PURPLE, width=3, size=12)
    k.text(fig, G[0] + 0.32, G[1] - 0.05, "goal region", color=PURPLE, size=17, xanchor="left",
           bg="rgba(255,255,255,0.85)")
    xs, ys = [], []
    for e in LOG[:it]:
        if e["new"] is not None:
            tr = R["trajs"][e["new"]]
            xs += list(tr[:, 0]) + [None]
            ys += list(tr[:, 1]) + [None]
    k.line(fig, xs, ys, color=GREEN, width=2.5)
    nodes = [R["nodes"][0]] + [R["nodes"][e["new"]] for e in LOG[:it] if e["new"] is not None]
    k.line(fig, [p[0] for p in nodes], [p[1] for p in nodes], color=GREEN, mode="markers", width=1)
    fig.data[-1].marker = dict(size=6, color=GREEN)
    if detail and 1 <= it <= len(LOG) and not final:
        e = LOG[it - 1]
        sx, sy, sth = e["sample"]
        near = R["nodes"][e["near"]]
        k.line(fig, [near[0], sx], [near[1], sy], color="#999999", width=1.5, dash="dot")
        for name, tr in e["cands"].items():
            if name != e["best"]:
                k.line(fig, tr[:, 0], tr[:, 1], color="#888888", width=3)
        tr = e["cands"][e["best"]]
        k.line(fig, tr[:, 0], tr[:, 1], color=GREEN if e["ok"] else RED, width=6)
        k.point(fig, sx, sy, RED, size=14, symbol="x")
        k.arrow(fig, sx, sy, sth, length=0.25, color=RED, width=3, size=11)
        k.point(fig, near[0], near[1], "black", size=10)
    if final:
        pts = np.vstack([R["trajs"][i] for i in R["path"][1:]])
        k.line(fig, pts[:, 0], pts[:, 1], color=BLUE, width=7)
    k.disk(fig, *m.START, color="#222222", width=2, body=False)
    k.arrow(fig, m.START[0], m.START[1], m.START[2], length=0.3, color="black", width=4)
    k.room_axes(fig)
    n_nodes = len(nodes)
    n_rej = sum(not e["ok"] for e in LOG[:it])
    if final:
        title = "goal region reached: 75 nodes, path of 8 primitives, 3.0 m (blue)"
    elif it == 0:
        title = "the tree starts at (2, 1) facing 30°, driving at 0.5 m/s"
    elif detail:
        e = LOG[it - 1]
        what = "goal sample" if e["kind"] == "goal" else "random sample"
        title = (f"iteration {it}: {what}; nearest node (black); {e['best']} comes closest, "
                 + ("free: added" if e["ok"] else "collides with an obstacle: rejected"))
    else:
        title = f"after {it} iterations: {n_nodes} nodes, {n_rej} motions rejected"
    return k.layout(fig, 1150, 720, title, margin=dict(l=70, r=30, t=70, b=60), size=20)


its = list(range(0, 13)) + list(range(25, len(LOG), 15)) + [len(LOG)]
figs, holds = [], []
for it in its:
    figs.append(frame(it, detail=it <= 12))
    holds.append(8 if it == 0 else 6 if it <= 12 else 3)
figs.append(frame(len(LOG), final=True))
holds.append(28)
make_gif(figs, here / "rrt_anim", fps=4, holds=holds, keys=[1, 7, 16, len(figs) - 1], cols=2, width=1000)
