"""Bug 1 (top) and Bug 2 (bottom) in the room with no map: the robot's centre (black dot) starts at (2, 1) and heads
for the middle of the doorway, (3.6, 4.0). The robot is drawn as its centre, so the box (brown) and the table (grey
outline) are grown by its radius, 0.25 m (pale grey band); the gap between them is narrower than the robot, so the
two grown shapes form one obstacle, 11.702 m round. Dashed: the start–goal line, the straight line from start to door. Both
hit the obstacle at H, 0.850 m from the start, and turn left. Bug 1 goes once round the whole obstacle, remembering
the point nearest the door (C, 0.755 m from it), goes back to C the shorter way, 3.604 m, and leaves: 16.912 m. Bug 2
leaves as soon as it meets the start–goal line again nearer the door (L, 1.417 m from it, against 2.550 m at H): 4.885 m.
Run -> bugs.gif, bugs_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from drawkit import axes, furniture, layout, title_at
from gifkit import BLUE, GREEN, ORANGE, PURPLE, make_gif
from plotly.subplots import make_subplots
from replan import BOX_M, BUG_GOAL, BUG_START, bug_paths

here = Path(__file__).parent
B = bug_paths()
assert round(B["perimeter"], 3) == 11.702 and round(B["len1"], 3) == 16.912 and round(B["len2"], 3) == 4.885
assert round(math.dist(BUG_START, B["hit"]), 3) == 0.850 and round(B["close_dist"], 3) == 0.755
assert round(B["s_close"], 3) == 3.604 and round(math.dist(B["exit"], BUG_GOAL), 3) == 1.417
assert round(math.dist(B["hit"], BUG_GOAL), 3) == 2.550 and round(B["d"], 3) == 3.4
assert B["len1"] <= B["d"] + 1.5 * B["perimeter"] and B["len2"] <= B["d"] + 0.5 * 2 * B["perimeter"]
STEP = 0.35


def resample(p):
    """Points along the route p every STEP metres, with the distance travelled at each."""
    seg = [math.dist(a, b) for a, b in zip(p, p[1:])]
    cum = np.concatenate([[0], np.cumsum(seg)])
    out = []
    for s in np.append(np.arange(0, cum[-1], STEP), cum[-1]):
        k = min(int(np.searchsorted(cum, s, side="right")) - 1, len(seg) - 1)
        u = (s - cum[k]) / seg[k] if seg[k] else 0
        out.append(((p[k][0] + u * (p[k + 1][0] - p[k][0]), p[k][1] + u * (p[k + 1][1] - p[k][1])), s))
    return out, cum


R1, C1 = resample(B["bug1"])
R2, C2 = resample(B["bug2"])
OB = np.array(B["obstacle"].exterior.coords)


def mark(fig, r, xy, text, pos, colour):
    fig.add_trace(go.Scatter(x=[xy[0]], y=[xy[1]], mode="markers+text", text=[f"<b>{text}</b>"], textposition=pos,
                             marker=dict(size=13, color=colour, line=dict(color="white", width=1.5)),
                             textfont=dict(size=19, color=colour), hoverinfo="skip"), row=r, col=1)


def panel(fig, r, pts, full, n, title, extra):
    fig.add_trace(go.Scatter(x=OB[:, 0], y=OB[:, 1], fill="toself", fillcolor="#E4E4E4", mode="lines",
                             line=dict(color="#9A9A9A", width=2), hoverinfo="skip"), row=r, col=1)
    x0, x1, y0, y1 = BOX_M
    fig.add_trace(go.Scatter(x=[x0, x1, x1, x0, x0], y=[y0, y0, y1, y1, y0], fill="toself", fillcolor="#8C6D4F",
                             mode="lines", line=dict(color="#8C6D4F", width=1), hoverinfo="skip"), row=r, col=1)
    furniture(fig, (r, 1))
    fig.add_trace(go.Scatter(x=[BUG_START[0], BUG_GOAL[0]], y=[BUG_START[1], BUG_GOAL[1]], mode="lines",
                             line=dict(color=PURPLE, width=2.5, dash="dash"), hoverinfo="skip"), row=r, col=1)
    s = pts[n][1]
    route_pts, cum = full
    done = [p for p, c in zip(route_pts, cum) if c <= s + 1e-9] + [pts[n][0]]
    fig.add_trace(go.Scatter(x=[p[0] for p in done], y=[p[1] for p in done], mode="lines",
                             line=dict(color=BLUE, width=4), hoverinfo="skip"), row=r, col=1)
    if s >= math.dist(BUG_START, B["hit"]) - 1e-9:
        mark(fig, r, B["hit"], "H", "bottom right", ORANGE)
    for xy, text, pos, col, at in extra:
        if s >= at - 1e-9:
            mark(fig, r, xy, text, pos, col)
    fig.add_trace(go.Scatter(x=[done[-1][0]], y=[done[-1][1]], mode="markers",
                             marker=dict(size=16, color="#222222", line=dict(color="white", width=2)),
                             hoverinfo="skip"), row=r, col=1)
    fig.add_trace(go.Scatter(x=[BUG_GOAL[0] + 0.42], y=[BUG_GOAL[1] - 0.14], mode="text", text=["<b>door</b>"],
                             textfont=dict(size=17), hoverinfo="skip"), row=r, col=1)
    axes(fig, (r, 1))
    return f"{title}: {s:.2f} m driven"


def frame(n):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.08)
    n1, n2 = min(n, len(R1) - 1), min(n, len(R2) - 1)
    hit = math.dist(BUG_START, B["hit"])
    t1 = panel(fig, 1, R1, (B["bug1"], C1), n1, "Bug 1", [(B["close"], "C", "top left", GREEN, hit + B["s_close"])])
    t2 = panel(fig, 2, R2, (B["bug2"], C2), n2, "Bug 2", [(B["exit"], "L", "middle left", GREEN, hit + B["s_leave"])])
    if n1 == len(R1) - 1:
        t1 = f"Bug 1: round the whole obstacle, back to C, out: {B['len1']:.3f} m"
    if n2 == len(R2) - 1:
        t2 = f"Bug 2: leaves at L, on the start–goal line nearer the door: {B['len2']:.3f} m"
    title_at(fig, t1, 1.0, size=19)
    title_at(fig, t2, 0.47, size=19)
    layout(fig, "no map: head for the door, follow what you hit", width=900, height=1080,
           margin=dict(l=30, r=30, t=110, b=30))
    return fig.update_layout(plot_bgcolor="white")


N = len(R1)
figs = [frame(n) for n in range(N)]
holds = [10] + [2] * (N - 2) + [30]
holds[len(R2) - 1] = 14
make_gif(figs, here / "bugs", fps=6, holds=holds, keys=[4, len(R2) - 1, 30, N - 1], cols=2, width=700)
