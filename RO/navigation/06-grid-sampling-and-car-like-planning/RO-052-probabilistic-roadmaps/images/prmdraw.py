"""Shared Plotly drawing for this Note's roadmap figures (no output when run on its own): the room in C-space (the
obstacles grown by the robot's radius, orange), milestones, edges, routes and a text panel on the right."""
import numpy as np
import plotly.graph_objects as go
from shapely.geometry import box

import cspace as c
import drawkit as dk
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED

VIEW = box(-0.2, -0.2, 7.2, 4.3)
EDGE = "rgba(76,120,168,0.55)"          # roadmap edges: light blue
MILE = BLUE                             # milestones
ROUTE = GREEN
QUERY = PURPLE
COMP = [BLUE, "#E377C2", "#17BECF", "#8C564B", "#BCBD22"]     # one colour per piece of the roadmap


def base(world, room=True):
    """A figure with the room's obstacle region (orange) for the robot of `world` and the furniture on top."""
    fig = go.Figure()
    fig.add_trace(dk.geom_trace(world.cobs.intersection(VIEW).difference(c.obstacles()), dk.COBS_FILL, ORANGE, 1.5))
    if room:
        dk.room(fig)
    return fig


def segs(fig, pairs, color=EDGE, width=1.5, dash=None):
    """Many straight edges as one trace: pairs is a list of ((x0, y0), (x1, y1))."""
    if not pairs:
        return
    xs, ys = [], []
    for a, b in pairs:
        xs += [a[0], b[0], None]
        ys += [a[1], b[1], None]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=width, dash=dash),
                             hoverinfo="skip"))


def dots(fig, pts, color=MILE, size=8, symbol="circle", line="white"):
    if len(pts) == 0:
        return
    P = np.asarray(pts)
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers",
                             marker=dict(color=color, size=size, symbol=symbol, line=dict(color=line, width=1)),
                             hoverinfo="skip"))


def route(fig, P, color=ROUTE, width=5):
    P = np.asarray(P)
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines", line=dict(color=color, width=width),
                             hoverinfo="skip"))


def place(fig, q, text, color="black", pos="top center", size=14):
    dk.point(fig, q[0], q[1], color, text, pos=pos, size=size, tsize=19)


def panel(fig, lines, x=0.665, top=0.95, step=0.075, size=19):
    """Text lines on the right of the room: list of (text, colour)."""
    for i, (s, col) in enumerate(lines):
        fig.add_annotation(x=x, y=top - step * i, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           text=s, showarrow=False, font=dict(size=size, color=col))


def finish(fig, title, w=1300, h=640, full=False):
    """Room axes on the left 62 percent (or the full width), equal scale."""
    fig.layout.xaxis.update(range=[-0.2, 7.2], dtick=1, title="x (m)", domain=[0, 1 if full else 0.62],
                            constrain="domain", showgrid=False)
    fig.layout.yaxis.update(range=[-0.2, 4.3], dtick=1, title="y (m)", scaleanchor="x", constrain="domain",
                            showgrid=False)
    dk.layout(fig, w, h, title, margin=dict(l=70, r=20, t=80, b=60))
    return fig
