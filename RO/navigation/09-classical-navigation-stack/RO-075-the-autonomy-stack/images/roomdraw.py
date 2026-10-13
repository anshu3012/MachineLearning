"""Drawing helpers for this Note's room figures (no output when run on its own): the part of the room around the
drive, the table (grey) with the band the robot's centre must keep out of (dashed: 0.25 m, the disk's radius),
the top wall with the door, and the robot as a disk with a line for its heading."""
import math

import numpy as np
import plotly.graph_objects as go
from gifkit import GREY
from trajkit import CORNER, R_BODY, TABLE

XR, YR = (1.3, 4.6), (0.45, 4.25)


def room(fig, rc=None, band=True):
    kw = dict(row=rc[0], col=rc[1]) if rc else {}
    t = list(TABLE) + [TABLE[0]]
    fig.add_trace(go.Scatter(x=[p[0] for p in t], y=[p[1] for p in t], fill="toself", fillcolor="#D9D9D9",
                             line=dict(color="#9A9A9A", width=2), mode="lines", hoverinfo="skip"), **kw)
    if band:
        from shapely.geometry import Polygon
        g = Polygon(TABLE).buffer(R_BODY, quad_segs=24).exterior.coords
        fig.add_trace(go.Scatter(x=[p[0] for p in g], y=[p[1] for p in g], mode="lines", hoverinfo="skip",
                                 line=dict(color="#9A9A9A", width=1.5, dash="dot")), **kw)
    for a, b in ((XR[0], 3.0), (4.2, XR[1])):
        fig.add_trace(go.Scatter(x=[a, b], y=[4.0, 4.0], mode="lines", line=dict(color="black", width=6),
                                 hoverinfo="skip"), **kw)
    fig.add_annotation(x=3.6, y=4.13, text="door", showarrow=False, font=dict(size=17, color=GREY), **kw)
    fig.add_annotation(x=4.3, y=1.7, text="table", showarrow=False, font=dict(size=18, color="#555555"), **kw)


def robot(fig, x, y, th, color, rc=None, fill="rgba(255,255,255,0.6)", width=3):
    kw = dict(row=rc[0], col=rc[1]) if rc else {}
    t = np.linspace(0, 2 * math.pi, 40)
    fig.add_trace(go.Scatter(x=x + R_BODY * np.cos(t), y=y + R_BODY * np.sin(t), mode="lines", fill="toself",
                             fillcolor=fill, line=dict(color=color, width=width), hoverinfo="skip"), **kw)
    fig.add_trace(go.Scatter(x=[x, x + R_BODY * math.cos(th)], y=[y, y + R_BODY * math.sin(th)], mode="lines",
                             line=dict(color=color, width=width + 1), hoverinfo="skip"), **kw)


def axes(fig, rc=None):
    kw = dict(row=rc[0], col=rc[1]) if rc else {}
    fig.update_xaxes(range=list(XR), visible=False, **kw)
    fig.update_yaxes(range=list(YR), visible=False, scaleanchor="x" if not rc or rc == (1, 1) else
                     f"x{(rc[0] - 1) * 2 + rc[1]}", **kw)


PERSON_FILL, PERSON_LINE = "#F2B8C6", "#C2185B"


def person(fig, c, r, rc=None, label=True):
    """The person the map does not have: a disk."""
    kw = dict(row=rc[0], col=rc[1]) if rc else {}
    t = np.linspace(0, 2 * math.pi, 60)
    fig.add_trace(go.Scatter(x=c[0] + r * np.cos(t), y=c[1] + r * np.sin(t), mode="lines", fill="toself",
                             fillcolor=PERSON_FILL, line=dict(color=PERSON_LINE, width=2), hoverinfo="skip"), **kw)
    if label:
        fig.add_annotation(x=c[0], y=c[1], text="person", showarrow=False, font=dict(size=16, color=PERSON_LINE),
                           **kw)


def route(fig, pts, rc=None, color=GREY):
    """The global plan: the A* route through cell centres (dashed, a dot at each centre)."""
    kw = dict(row=rc[0], col=rc[1]) if rc else {}
    fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="lines+markers", line=dict(color=color, width=2.5,
                             dash="dash"), marker=dict(size=7, color=color), hoverinfo="skip"), **kw)


def band(fig, P, color, rc=None, size=9, width=2.5, ticks=True):
    """A timed elastic band: its poses (dots, with a short line for the heading) joined in order."""
    kw = dict(row=rc[0], col=rc[1]) if rc else {}
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines+markers", line=dict(color=color, width=width),
                             marker=dict(size=size, color=color), hoverinfo="skip"), **kw)
    if ticks:
        L = 0.09
        xs, ys = [], []
        for x, y, th in P:
            xs += [x, x + L * math.cos(th), None]
            ys += [y, y + L * math.sin(th), None]
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=2), hoverinfo="skip"), **kw)


def zoom(fig, xr, yr, rc=None):
    kw = dict(row=rc[0], col=rc[1]) if rc else {}
    fig.update_xaxes(range=list(xr), visible=False, **kw)
    fig.update_yaxes(range=list(yr), visible=False, scaleanchor="x" if not rc or rc == (1, 1) else
                     f"x{(rc[0] - 1) * 2 + rc[1]}", **kw)
