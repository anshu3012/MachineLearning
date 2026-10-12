"""Applying the four-action plan, one action at a time. Left: the room, with the robot driving each move along a
shortest route of 0.5 m grid cells and the cup where the facts say it is. Right: the 8 facts, black when true and
grey when false; for each action, its precondition is checked (blue), then its delete list is removed (red) and its
add list added (green). The last frame holds the goal fact cup-at door. Routes (8-connected cells, as for Dijkstra
and A*): start -> table 0.707 m, table -> door 2.707 m, 3.414 m in all. Run: python plan_apply.py -> plan_apply.gif, plan_apply_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from robotdraw import robot
from roommap import CAB, POLES, POLE_R, TABLE
from taskplan import ACTIONS, CELL, CUP, FACTS, GOAL, INIT, SPOT, apply, applicable, bfs, grid_route

here = Path(__file__).parent
PLAN = bfs()[0]
assert PLAN == ["move start table", "pick-up table", "move table door", "put-down door"]
ACT = {a[0]: a for a in ACTIONS}
LEN = {"move start table": grid_route(CELL["start"], CELL["table"])[0],
       "move table door": grid_route(CELL["table"], CELL["door"])[0]}
ROUTE = {"move start table": grid_route(CELL["start"], CELL["table"])[1],
         "move table door": grid_route(CELL["table"], CELL["door"])[1]}
assert [round(v, 3) for v in LEN.values()] == [0.707, 2.707] and round(sum(LEN.values()), 3) == 3.414


def path_of(name):
    """Route as points in metres: the robot's spot, then the centres of the route's cells (the robot at the start
    stands on the corner of its cell, so it first steps to the cell's centre)."""
    a, b = name.split()[1:]
    pts = [SPOT[a]] + [((i + 0.5) * 0.5, (j + 0.5) * 0.5) for i, j in ROUTE[name]]
    pts = [p for k, p in enumerate(pts) if k == 0 or not np.allclose(p, pts[k - 1])]
    assert np.allclose(pts[-1], SPOT[b])
    return np.array(pts)


def along(pts, t):
    """Point and heading at fraction t of the polyline pts."""
    seg = np.diff(pts, axis=0)
    L = np.hypot(*seg.T)
    d = t * L.sum()
    k = min(np.searchsorted(np.cumsum(L), d, side="right"), len(L) - 1)
    d0 = np.cumsum(L)[k] - L[k]
    p = pts[k] + seg[k] * (d - d0) / L[k]
    return p, np.arctan2(seg[k][1], seg[k][0])


def partial(pts, t):
    """The polyline pts up to fraction t of its length."""
    cum = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    p, _ = along(pts, t)
    return np.vstack([pts[cum < t * cum[-1] - 1e-9], p])


def room(fig):
    fig.add_shape(type="rect", x0=0, y0=0, x1=7, y1=4, line=dict(width=0), fillcolor="white", layer="below")
    for g in np.arange(0.5, 7, 0.5):
        fig.add_shape(type="line", x0=g, x1=g, y0=0, y1=4, line=dict(color="#E6E6E6", width=1), layer="below")
    for g in np.arange(0.5, 4, 0.5):
        fig.add_shape(type="line", x0=0, x1=7, y0=g, y1=g, line=dict(color="#E6E6E6", width=1), layer="below")
    for xs, ys in (([3.0, 0, 0, 7, 7, 4.2], [4, 4, 0, 0, 4, 4]),):
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="black", width=6)))
    tx, ty = zip(*(TABLE + [TABLE[0]]))
    fig.add_trace(go.Scatter(x=tx, y=ty, mode="lines", fill="toself", line=dict(color=BLUE, width=3),
                             fillcolor="rgba(76,120,168,0.22)"))
    fig.add_trace(go.Scatter(x=[5.6, 7, 7, 6.4, 6.4, 5.6, 5.6], y=[4, 4, 2.4, 2.4, 3.4, 3.4, 4], mode="lines",
                             fill="toself", line=dict(color=PURPLE, width=3), fillcolor="rgba(178,121,162,0.22)"))
    for (px, py), c in zip(POLES.values(), ("#E377C2", GREEN)):
        fig.add_shape(type="circle", x0=px - POLE_R, x1=px + POLE_R, y0=py - POLE_R, y1=py + POLE_R,
                      fillcolor=c, line=dict(color=c, width=2), opacity=1)
    for p, (x, y) in SPOT.items():
        fig.add_shape(type="circle", x0=x - 0.25, x1=x + 0.25, y0=y - 0.25, y1=y + 0.25,
                      fillcolor="rgba(0,0,0,0)", line=dict(color=GREEN, width=3, dash="dash"), opacity=1)
    fig.add_annotation(x=1.55, y=0.6, text="start", showarrow=False, font=dict(size=21, color=GREEN))
    fig.add_annotation(x=2.2, y=2.15, text="table", showarrow=False, font=dict(size=21, color=GREEN))
    fig.add_annotation(x=3.2, y=3.75, text="door", showarrow=False, font=dict(size=21, color=GREEN), xanchor="right")


def frame(title, state, pose, cup, trail=(), act=None, stage=None):
    """stage: None (plain state), 'pre' (precondition checked) or 'done' (delete and add lists shown)."""
    fig = go.Figure()
    room(fig)
    for pts in trail:
        fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="lines+markers", line=dict(color=ORANGE, width=4),
                                 marker=dict(size=6, color=ORANGE)))
    for tr in robot((pose[0], pose[1], pose[2]), scale=1.4):
        fig.add_trace(tr)
    fig.add_trace(go.Scatter(x=[cup[0]], y=[cup[1]], mode="markers", marker=dict(size=17, color=ORANGE,
                                                                               line=dict(color="black", width=2))))
    # the facts
    fig.add_annotation(x=7.7, y=4.5, text="<b>facts</b>  (black: true, grey: false)", showarrow=False,
                       xanchor="left", font=dict(size=21))
    pre, add, de = (act[1], act[2], act[3]) if act else (set(), set(), set())
    for k, f in enumerate(FACTS):
        y = 4.0 - 0.41 * k
        on = f in state
        col, mark, note = ("black", "■", "") if on else ("#AAAAAA", "□", "")
        if stage == "pre" and f in pre:
            col, note = BLUE, "  needed: true ✓"
        if stage == "done" and f in de:
            col, mark, note = RED, "□", "  deleted"
        if stage == "done" and f in add:
            col, mark, note = GREEN, "■", "  added"
        fig.add_annotation(x=7.75, y=y, text=f"{mark} {f}{note}", showarrow=False, xanchor="left",
                           font=dict(size=23, color=col))
    if act:
        lines = [f"<b>{act[0]}</b>", f"precondition: {', '.join(sorted(pre))}",
                 f"add: {', '.join(sorted(add))}", f"delete: {', '.join(sorted(de))}"]
        fig.add_annotation(x=7.7, y=0.62, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                           align="left", font=dict(size=19), bgcolor="#F4F4F4", bordercolor=GREY, borderpad=6)
    fig.update_layout(template="simple_white", font=FONT, width=1350, height=640, showlegend=False,
                      margin=dict(l=10, r=10, t=60, b=10), title=dict(x=0.5, text=title),
                      xaxis=dict(visible=False, range=[-0.2, 13.7]),
                      yaxis=dict(visible=False, range=[-1.25, 4.8], scaleanchor="x"))
    return fig


figs, holds, keys = [], [], []
s, pose, cup, trail = INIT, (2.0, 1.0, np.radians(30)), CUP, []
figs.append(frame("start state: robot-at start, cup-at table, hand-empty", s, pose, cup))
holds.append(4)
keys.append(0)
for k, name in enumerate(PLAN, 1):
    a = ACT[name]
    assert applicable(s, a)
    figs.append(frame(f"action {k}: {name}; is its precondition true?", s, pose, cup, trail, a, "pre"))
    holds.append(4)
    if name in ROUTE:
        pts = path_of(name)
        for t in (0.25, 0.5, 0.75, 1.0):
            p, h = along(pts, t)
            pose = (p[0], p[1], h)
            moved = trail + [partial(pts, t)]
            c = (pose[0], pose[1]) if "holding-cup" in s else cup
            figs.append(frame(f"action {k}: {name}; driving a shortest route, {LEN[name]:.3f} m",
                              s, pose, c, moved, a, "pre"))
            holds.append(1)
        trail = trail + [pts]
    s_new = apply(s, a)
    if name.startswith("pick-up"):
        cup = (pose[0], pose[1])
    elif name.startswith("put-down"):
        cup = (pose[0] + 0.05, pose[1] + 0.32)
    elif "holding-cup" in s_new:
        cup = (pose[0], pose[1])
    figs.append(frame(f"action {k}: {name}; delete list removed, add list added", s_new, pose, cup, trail, a,
                      "done"))
    holds.append(5)
    keys.append(len(figs) - 1)
    s = s_new
assert GOAL <= s and s == frozenset({"robot-at door", "cup-at door", "hand-empty"})
figs.append(frame("goal reached: cup-at door is true after 4 actions", s, pose, cup, trail))
holds.append(12)
keys = [0, keys[1], keys[2], len(figs) - 1]
make_gif(figs, here / "plan_apply", fps=2, holds=holds, keys=keys, cols=2, width=1000)
