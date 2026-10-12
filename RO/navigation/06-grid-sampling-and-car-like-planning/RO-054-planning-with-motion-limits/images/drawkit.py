"""Shared Plotly drawing for this Note's figures (no output when run on its own): the room in RO-037's colours with
the door closed, the grown obstacles, the disk robot, the phase plane of the straight drive and the layout helpers.
Colours: the robot's path green, the planned route black dotted, rejected or colliding motions red, the region of
inevitable collision orange, the door band dark red, the goal region purple."""
import math

import numpy as np
import plotly.graph_objects as go
from shapely.geometry import Point

import motionkit as m
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED
from robotdraw import robot

PINK = "#E377C2"
WALL = "#4D4D4D"
DOOR = "#8C3B2E"
FOOT = "#222222"
COBS_FILL = "rgba(245,133,24,0.22)"
ICS_FILL = "rgba(245,133,24,0.35)"
DOOR_FILL = "rgba(140,59,46,0.45)"


def _kw(row, col):
    return dict(row=row, col=col) if row else {}


def poly_trace(xs, ys, fill, line, width=2, dash=None, opacity=1.0):
    return go.Scatter(x=list(xs), y=list(ys), mode="lines", fill="toself", fillcolor=fill, opacity=opacity,
                      line=dict(color=line, width=width, dash=dash), hoverinfo="skip")


def outline(geom):
    """x, y lists of a shapely polygon or multipolygon's outlines, separated by None."""
    xs, ys = [], []
    polys = getattr(geom, "geoms", [geom])
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            x, y = ring.xy
            xs += list(x) + [None]
            ys += list(y) + [None]
    return xs, ys


def geom_trace(geom, fill, line, width=2, dash=None):
    xs, ys = outline(geom)
    return poly_trace(xs, ys, fill, line, width, dash)


def room(fig, row=None, col=None, grown=False, door=True):
    """Walls as dark bands, the furniture in its RO-009 colours, the door closed (dark red bar)."""
    kw = _kw(row, col)
    t = 0.12
    for x0, y0, x1, y1 in [(-t, -t, m.W + t, 0), (-t, -t, 0, m.H + t), (m.W, -t, m.W + t, m.H + t),
                           (-t, m.H, 3.0, m.H + t), (4.2, m.H, m.W + t, m.H + t)]:
        fig.add_trace(poly_trace([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], WALL, WALL, 1), **kw)
    if door:
        fig.add_trace(poly_trace([3.0, 4.2, 4.2, 3.0, 3.0], [m.H, m.H, m.H + t, m.H + t, m.H], DOOR, DOOR, 1), **kw)
    if grown:
        g = m.GROWN.union(m.box(-1, -1, m.W + 1, m.H + 1).difference(m.INNER)).intersection(
            m.box(-0.12, -0.12, m.W + 0.12, m.H + 0.12)).difference(m.OBST)
        fig.add_trace(geom_trace(g, COBS_FILL, ORANGE, 1), **kw)
    tx, ty = zip(*(m.TABLE + [m.TABLE[0]]))
    fig.add_trace(poly_trace(tx, ty, "#C3D1E3", BLUE, 2), **kw)
    cab = m.box(*[m.CAB[0][i] for i in (0, 2, 1, 3)]).union(m.box(*[m.CAB[1][i] for i in (0, 2, 1, 3)]))
    fig.add_trace(geom_trace(cab, "#E8D6E3", PURPLE), **kw)
    for (px, py), col in zip(m.POLES.values(), [PINK, GREEN]):
        fig.add_trace(geom_trace(Point(px, py).buffer(m.POLE_R, quad_segs=32), col, col, 1), **kw)


def disk(fig, x, y, th, row=None, col=None, body=True, color=FOOT, width=3, opacity=1.0, scale=1.0):
    """The disk footprint (dashed circle of radius 0.25 m) with the RO-001 robot drawn inside."""
    kw = _kw(row, col)
    g = Point(x, y).buffer(m.R_BODY, quad_segs=32)
    fig.add_trace(geom_trace(g, "rgba(0,0,0,0.06)", color, width, "dash"), **kw)
    if body:
        for tr in robot((x, y, th), scale=scale, opacity=opacity):
            fig.add_trace(tr, **kw)


def ghost(fig, x, y, th, row=None, col=None):
    """A pale robot: where a plan assumed the robot would be."""
    kw = _kw(row, col)
    g = Point(x, y).buffer(m.R_BODY, quad_segs=32)
    fig.add_trace(geom_trace(g, "rgba(0,0,0,0.02)", "#AAAAAA", 2, "dot"), **kw)
    for tr in robot((x, y, th), opacity=0.3):
        fig.add_trace(tr, **kw)


def line(fig, xs, ys, color=GREEN, width=4, dash=None, row=None, col=None, mode="lines", opacity=1.0):
    fig.add_trace(go.Scatter(x=list(xs), y=list(ys), mode=mode, line=dict(color=color, width=width, dash=dash),
                             opacity=opacity, hoverinfo="skip"), **_kw(row, col))


def point(fig, x, y, color, text=None, pos="top center", size=14, row=None, col=None, tsize=18, symbol="circle"):
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text" if text else "markers",
                             marker=dict(size=size, color=color, symbol=symbol, line=dict(color="white", width=1.5)),
                             text=[text] if text else None, textposition=pos,
                             textfont=dict(size=tsize, color=color), hoverinfo="skip"), **_kw(row, col))


def arrow(fig, x, y, th, length=0.35, color=ORANGE, width=4, row=None, col=None, size=14):
    fig.add_trace(go.Scatter(x=[x, x + length * math.cos(th)], y=[y, y + length * math.sin(th)], mode="lines+markers",
                             line=dict(color=color, width=width),
                             marker=dict(symbol="arrow", size=[0, size], angleref="previous", color=color),
                             hoverinfo="skip"), **_kw(row, col))


def text(fig, x, y, s, color="black", size=18, row=None, col=None, xanchor="center", bg="white"):
    fig.add_annotation(x=x, y=y, text=s, showarrow=False, xanchor=xanchor, font=dict(size=size, color=color),
                       bgcolor=bg, **_kw(row, col))


def room_axes(fig, row=None, col=None, xr=(-0.25, 7.25), yr=(-0.25, 4.35), titles=True, anchor="x"):
    kw = _kw(row, col)
    fig.update_xaxes(range=list(xr), dtick=1, title="x (m)" if titles else None, showgrid=False, **kw)
    fig.update_yaxes(range=list(yr), dtick=1, title="y (m)" if titles else None, showgrid=False,
                     scaleanchor=anchor, **kw)


# ---------------------------------------------------------------- the phase plane of the straight drive
S_MAX, V_MAX_PLOT = 3.4, 0.7


def ics_boundary(n=200):
    """s, v of the edge of the region of inevitable collision: s + v^2 / (2 a) = S_DOOR."""
    v = np.linspace(0, V_MAX_PLOT, n)
    return m.S_DOOR - v * v / (2 * m.A_MAX), v


def phase_regions(fig, row=None, col=None, ics=True, door=True):
    kw = _kw(row, col)
    if door:
        fig.add_trace(poly_trace([m.S_DOOR, S_MAX, S_MAX, m.S_DOOR, m.S_DOOR], [0, 0, V_MAX_PLOT, V_MAX_PLOT, 0],
                                 DOOR_FILL, DOOR, 1), **kw)
    if ics:
        s, v = ics_boundary()
        fig.add_trace(poly_trace(list(s) + [m.S_DOOR, m.S_DOOR], list(v) + [V_MAX_PLOT, 0], ICS_FILL, ORANGE, 2),
                      **kw)
    fig.add_trace(go.Scatter(x=[0, S_MAX], y=[m.V_TOP, m.V_TOP], mode="lines", line=dict(color=GREY, width=2,
                             dash="dash"), hoverinfo="skip"), **kw)


def phase_axes(fig, row=None, col=None, xr=(0, S_MAX), yr=(-0.02, V_MAX_PLOT)):
    kw = _kw(row, col)
    fig.update_xaxes(range=list(xr), dtick=0.5, title="position s along the line (m)", showgrid=False, **kw)
    fig.update_yaxes(range=list(yr), dtick=0.1, title="speed v (m/s)", showgrid=False, **kw)


def layout(fig, w, h, title=None, margin=None, size=22):
    fig.update_layout(template="simple_white", width=w, height=h, font=FONT, showlegend=False,
                      margin=margin or dict(l=80, r=30, t=90 if title else 30, b=70),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=size)) if title else None)
    return fig
