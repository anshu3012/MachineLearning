"""Ray casting as an animation. The grid map of the room has 0.5 m cells, drawn
coarse for clarity (the Note's code walks in 1 mm steps); the ring of dark cells around the room is the wall.
From pose A (2, 2, 0) the forward ray checks one cell after another: six free cells, then it enters a wall cell
and stops after 3.0 m. From pose B (3, 2, 0): four free cells, stop after 2.0 m. A counter shows the distance
walked. Both rays start at y = 2; they are drawn in different rows so both show.
Run -> raycast_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import raycast
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, make_gif
from roomkit import text

here = Path(__file__).parent
CELL = 0.5
WALL, LINE = "#979797", "#C4C4C4"
POSES = [("A", (2.0, 2.0, 0.0), 2.75, BLUE, "#BCCCE0"), ("B", (3.0, 2.0, 0.0), 1.25, GREEN, "#C6E2C2")]


def wall_cells():
    xs = np.arange(-0.5, 5.5, CELL)
    ys = np.arange(0.0, 4.0, CELL)
    return [(x, -0.5) for x in xs] + [(x, 4.0) for x in xs] + [(-0.5, y) for y in ys] + [(5.0, y) for y in ys]


def frame(state, title):
    """state: for each pose already started, (cells checked, stopped?)."""
    fig = go.Figure()
    for x, y in wall_cells():
        fig.add_shape(type="rect", x0=x, x1=x + CELL, y0=y, y1=y + CELL, fillcolor=WALL, line=dict(width=0),
                      layer="below", opacity=1)
    for g in np.arange(-0.5, 5.51, CELL):
        fig.add_shape(type="line", x0=g, x1=g, y0=-0.5, y1=4.5, line=dict(color=LINE, width=1), opacity=1)
    for g in np.arange(-0.5, 4.51, CELL):
        fig.add_shape(type="line", x0=-0.5, x1=5.5, y0=g, y1=g, line=dict(color=LINE, width=1), opacity=1)
    lines = []
    for (name, pose, row, col, fill), (n, stop) in zip(POSES, state):
        x0 = pose[0]
        for i in range(n):
            fig.add_shape(type="rect", x0=x0 + i * CELL, x1=x0 + (i + 1) * CELL, y0=row - 0.25, y1=row + 0.25,
                          fillcolor=fill, line=dict(width=0), opacity=1)
        cur = x0 + (n - 1) * CELL if not stop else 5.0
        if n or stop:
            fig.add_shape(type="rect", x0=cur, x1=cur + CELL, y0=row - 0.25, y1=row + 0.25, opacity=1,
                          fillcolor=WALL if stop else fill, line=dict(color=ORANGE, width=5))
        reach = min(x0 + n * CELL, 5.0)
        if reach > x0:
            fig.add_annotation(x=reach, y=row, ax=x0, ay=row, xref="x", yref="y", axref="x", ayref="y", text="",
                               showarrow=True, arrowhead=2, arrowwidth=4, arrowcolor=col)
        fig.add_trace(go.Scatter(x=[x0], y=[row], mode="markers", marker=dict(size=16, color=col)))
        text(fig, x0 - 0.1, row + 0.42, f"pose {name} ({x0:g}, 2, 0)", col, ref=("x", "y"), anchor="left",
             bgcolor="white")
        lines.append((f"pose {name}", col, 24))
        lines.append((f"distance walked: {reach - x0:.1f} m", "black", 22))
        if stop:
            lines.append((f"expected range z* = {reach - x0:.1f} m", col, 22))
        lines.append(("", "black", 10))
    for j, (s, col, size) in enumerate(lines):
        text(fig, 0.75, 0.92 - 0.085 * j, s, col, size=size)
    text(fig, 0.37, -0.09, "orange box: the cell being checked; dark grey: wall cells", GREY, size=17,
         anchor="center")
    text(fig, 0.37, -0.15, "both rays start at y = 2, drawn in different rows so both show", GREY, size=17,
         anchor="center")
    fig.update_xaxes(range=[-0.6, 5.6], tickvals=list(range(6)), domain=[0, 0.72], showline=False, ticks="",
                     tickfont=dict(color=GREY, size=18))
    fig.update_yaxes(range=[-0.6, 4.6], visible=False, scaleanchor="x", scaleratio=1, constrain="domain")
    fig.update_layout(template="simple_white", width=1100, height=640, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=70, b=110), title=dict(text=title, x=0.5, font_size=22))
    return fig


figs, holds, keys = [], [], []
done = []
for (name, pose, row, col, fill), zs in zip(POSES, (3.0, 2.0)):
    nfree = int(round(zs / CELL))
    figs.append(frame(done + [(0, False)], f"pose {name}: walk along the beam, one cell at a time"))
    holds.append(3)
    for n in range(1, nfree + 1):
        figs.append(frame(done + [(n, False)], f"pose {name}: cell {n} is free, keep walking"))
        holds.append(2)
    done = done + [(nfree, True)]
    figs.append(frame(done, f"pose {name}: the next cell is wall, stop after {zs:.1f} m"))
    holds.append(8)
    keys.append(len(figs) - 1)
figs.append(frame(done, "ray casting: from A the beam should read 3.0 m, from B 2.0 m"))
holds.append(14)
make_gif(figs, here / "raycast_anim", fps=3, holds=holds, keys=keys, cols=2, width=950)
assert [raycast(p, 0.0) for _, p, *_ in POSES] == [3.0, 2.0]   # the expected ranges of the forward beam
