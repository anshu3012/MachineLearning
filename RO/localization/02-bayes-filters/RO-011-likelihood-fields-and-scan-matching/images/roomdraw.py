"""Plotly helpers: the room outline, the box and the robot marker (no output when run on its own)."""
import numpy as np
import plotly.graph_objects as go

from fieldmodel import BOX
from gifkit import BLUE, GREY, ORANGE


def room_shapes(fig, row=None, col=None, color=GREY):
    kw = dict(row=row, col=col) if row else {}
    fig.add_shape(type="rect", x0=0, x1=5, y0=0, y1=4, line=dict(color=color, width=4), fillcolor="rgba(0,0,0,0)", **kw)
    fig.add_shape(type="rect", x0=BOX[0], x1=BOX[1], y0=BOX[2], y1=BOX[3], line=dict(color=color, width=3),
                  fillcolor="rgba(107,107,107,0.35)", **kw)


def robot_marker(pose, color=BLUE, size=0.18):
    x, y, th = pose
    c, s = np.cos(th), np.sin(th)
    pts = np.array([[size, 0], [-0.6 * size, 0.55 * size], [-0.6 * size, -0.55 * size], [size, 0]])
    return go.Scatter(x=x + c * pts[:, 0] - s * pts[:, 1], y=y + s * pts[:, 0] + c * pts[:, 1], mode="lines",
                      fill="toself", line=dict(color=color, width=2), fillcolor=color, hoverinfo="skip")
