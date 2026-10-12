"""Shared Plotly drawing for this Note's planner figures (no output when run on its own): the room seen in the disk
robot's C-space (obstacles grown by 0.25 m in light grey, the furniture in its RO-009 colours), trees as lines,
and a text panel on the right."""
import numpy as np
import plotly.graph_objects as go

import cspace as c
import drawkit as dk

COBS = c.cobs_disk()
VIEW = c.box(-0.1, -0.1, 7.1, 4.1)
TREE = "#4C78A8"


def base(fig=None, row=None, col=None):
    fig = fig or go.Figure()
    kw = dict(row=row, col=col) if row else {}
    fig.add_trace(dk.geom_trace(COBS.intersection(VIEW), "rgba(200,200,200,1)", "rgba(150,150,150,1)", 1), **kw)
    dk.room(fig, row=row, col=col)
    return fig


def tree_trace(nodes, parent, color=TREE, width=2, upto=None, row=None):
    """All edges of a tree (parent index per node) as one line trace with gaps."""
    xs, ys = [], []
    n = len(nodes) if upto is None else upto
    for k in range(1, n):
        p = parent[k]
        if p < 0:
            continue
        xs += [nodes[p][0], nodes[k][0], None]
        ys += [nodes[p][1], nodes[k][1], None]
    return go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=width), hoverinfo="skip")


def nodes_trace(nodes, color=TREE, size=6):
    N = np.asarray(nodes)
    return go.Scatter(x=N[:, 0], y=N[:, 1], mode="markers", marker=dict(size=size, color=color), hoverinfo="skip")


def panel(fig, lines, x=0.75, y0=0.92, dy=0.07, size=19):
    for i, (t, col) in enumerate(lines):
        fig.add_annotation(x=x, y=y0 - dy * i, xref="paper", yref="paper", xanchor="left", yanchor="top", text=t,
                           showarrow=False, font=dict(size=size, color=col))


def finish(fig, title, width=1300, height=620, domain=0.72):
    fig.update_layout(xaxis=dict(range=[-0.15, 7.15], dtick=1, title="x (m)", showgrid=False, domain=[0, domain],
                                 constrain="domain"),
                      yaxis=dict(range=[-0.15, 4.2], dtick=1, title="y (m)", showgrid=False, scaleanchor="x",
                                 constrain="domain"))
    dk.layout(fig, width, height, title, margin=dict(l=70, r=20, t=80, b=60))
    return fig
