"""Animation: a bounding-volume hierarchy over the room's 25 bodies (4 pieces of furniture and 21 wall panels about
1 m long). Build, top down: the root box holds everything; each box is split into two halves of equal count, sorting
by box centre along x, then y, then x, ... Query: the robot with its centre at (3.5, 3.2) (its box dashed red)
descends from the root; a box that misses the robot's box is not opened. 9 box tests reach the table, the one body
left for the narrow phase, instead of 25. Left: the boxes in the room; right: the same boxes as a tree.
Run -> bvh.gif, bvh_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import collide as k
import cspace as c
import drawkit as dk
from gifkit import GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
items = [(n, k.aabb(g)) for n, g in k.all_bodies().items()]
root = k.build_bvh(items)
qbox = k.aabb(k.robot(c.TEST))
log = []
hits = k.query_bvh(root, qbox, log)
assert len(items) == 25 and len(log) == 9 and hits == ["table"]

# tree layout: leaves left to right, a parent above the middle of its children
nodes, leaves = [], []


def lay(n, d=0):
    n["depth"] = d
    nodes.append(n)
    if "name" in n:
        n["x"] = len(leaves)
        leaves.append(n)
    else:
        for kid in n["kids"]:
            lay(kid, d + 1)
        n["x"] = sum(kid["x"] for kid in n["kids"]) / 2


lay(root)
DEPTH = max(n["depth"] for n in nodes)
SHORT = {"table": "table", "cabinet": "cabinet", "pink pole": "pink", "green pole": "green"}
LEVEL = [ORANGE, "#B279A2", "#4C78A8", "#9D755D", "#17BECF", "#6B6B6B"]


def frame(title, level=None, tested=(), lines=()):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.04,
                        subplot_titles=["boxes in the room", "the same boxes as a tree"])
    dk.room(fig, 1, 1)
    status = {id(n): h for n, h in tested}
    show = [n for n in nodes if (level is not None and n["depth"] <= level and n["depth"] == min(level, n["depth"])
                                 and ("name" in n or n["depth"] == level))]
    if level is not None:                                    # build: boxes of this level (and leaves above it)
        for n in nodes:
            if n["depth"] == level or ("name" in n and n["depth"] < level):
                x0, y0, x1, y1 = n["box"]
                fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=dict(color=LEVEL[n["depth"]], width=3),
                              fillcolor="rgba(0,0,0,0)", opacity=1, layer="above", row=1, col=1)
    for n, h in tested:
        x0, y0, x1, y1 = n["box"]
        fig.add_shape(type="rect", x0=x0 - 0.04, y0=y0 - 0.04, x1=x1 + 0.04, y1=y1 + 0.04,
                      line=dict(color=GREEN if h else RED, width=4), fillcolor="rgba(0,0,0,0)", opacity=1,
                      layer="above", row=1, col=1)
    if tested or level is None:
        dk.disk(fig, *c.TEST, 0.0, row=1, col=1, body=False, color=RED)
        fig.add_shape(type="rect", x0=qbox[0], y0=qbox[1], x1=qbox[2], y1=qbox[3], line=dict(color=RED, width=2,
                      dash="dot"), fillcolor="rgba(0,0,0,0)", opacity=1, layer="above", row=1, col=1)
    for n in nodes:                                           # tree edges and nodes
        if "kids" in n:
            for kid in n["kids"]:
                vis = level is None or kid["depth"] <= level
                fig.add_trace(go.Scatter(x=[n["x"], kid["x"]], y=[-n["depth"], -kid["depth"]], mode="lines",
                                         line=dict(color="#BBBBBB" if vis else "#EEEEEE", width=2), hoverinfo="skip"),
                              row=1, col=2)
    for n in nodes:
        vis = level is None or n["depth"] <= level
        if id(n) in status:
            col = GREEN if status[id(n)] else RED
        else:
            col = LEVEL[n["depth"]] if (level is not None and vis) else ("#DDDDDD" if not vis else "#BBBBBB")
        lab = SHORT.get(n.get("name"), "")
        fig.add_trace(go.Scatter(x=[n["x"]], y=[-n["depth"]], mode="markers+text" if lab and vis else "markers",
                                 marker=dict(size=15 if "kids" in n else 11, color=col, line=dict(color="white", width=1)),
                                 text=[lab], textposition="bottom center", textfont=dict(size=15, color="black"),
                                 hoverinfo="skip"), row=1, col=2)
    for i, (s, col) in enumerate(lines):
        fig.add_annotation(x=0.52, y=0.12 - 0.07 * i, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           text=s, showarrow=False, font=dict(size=18, color=col))
    fig.update_xaxes(range=[-0.3, 7.3], dtick=1, title="x (m)", row=1, col=1)
    fig.update_yaxes(range=[-0.3, 4.4], dtick=1, title="y (m)", scaleanchor="x", row=1, col=1)
    fig.update_xaxes(range=[-1, len(leaves)], visible=False, row=1, col=2)
    fig.update_yaxes(range=[-DEPTH - 2.2, 0.6], visible=False, row=1, col=2)
    dk.layout(fig, 1400, 640, title, margin=dict(l=70, r=20, t=90, b=60))
    fig.update_annotations(font_size=20, selector=dict(text="boxes in the room"))
    fig.update_annotations(font_size=20, selector=dict(text="the same boxes as a tree"))
    return fig


figs, holds = [], []
for lv in range(DEPTH + 1):
    axis = "x" if lv % 2 == 0 else "y"
    figs.append(frame("build: one box round all 25 bodies" if lv == 0 else
                      f"build level {lv}: each box split into two halves, sorted along {'y' if axis == 'x' else 'x'}",
                      level=lv))
    holds.append(4)
for i in range(1, len(log) + 1):
    n, h = log[i - 1]
    what = n.get("name", "a box")
    figs.append(frame(f"query, test {i}: {what} " + ("overlaps the robot's box: open it" if h and "kids" in n else
                      "overlaps: narrow phase" if h else "misses: skip everything inside"), tested=log[:i],
                      lines=[(f"box tests: {i} (brute force: 25)", "black")]))
    holds.append(3)
d = c.Polygon(c.TABLE).distance(c.Point(*c.TEST))
figs.append(frame("9 box tests leave one body: the table, 0.2 m away: collision", tested=log,
                  lines=[("box tests: 9 instead of 25", "black"), (f"narrow phase: table at {d:.1f} m < 0.25 m", RED)]))
holds.append(14)
make_gif(figs, here / "bvh", fps=2, holds=holds, keys=[1, 3, DEPTH + 4, len(figs) - 1], cols=2, width=1050)
