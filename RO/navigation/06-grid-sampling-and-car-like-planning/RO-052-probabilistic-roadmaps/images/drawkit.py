"""Shared Plotly drawing for this Note's figures (no output when run on its own): the room, its obstacles, grown
obstacles (C-obstacles), the disk footprint and the board, in one colour code used by every figure."""
import numpy as np
import plotly.graph_objects as go

import cspace as c
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED
from robotdraw import robot

PINK = "#E377C2"
WALL = "#4D4D4D"
COBS_FILL, COBS_LINE = "rgba(245,133,24,0.28)", ORANGE
FOOT = "#222222"


def poly_trace(xs, ys, fill, line, width=2, dash=None, opacity=1.0):
    return go.Scatter(x=xs, y=ys, mode="lines", fill="toself", fillcolor=fill, opacity=opacity,
                      line=dict(color=line, width=width, dash=dash), hoverinfo="skip")


def geom_trace(geom, fill, line, width=2, dash=None):
    xs, ys = c.outline(geom)
    return poly_trace(xs, ys, fill, line, width, dash)


def room(fig, row=None, col=None, walls=True):
    """Furniture in its RO-009 colours and the walls as dark bands, the doorway open."""
    kw = dict(row=row, col=col) if row else {}
    if walls:
        t = 0.12
        for x0, y0, x1, y1 in [(-t, -t, c.W + t, 0), (-t, -t, 0, c.H + t), (c.W, -t, c.W + t, c.H + t),
                               (-t, c.H, c.DOOR[0], c.H + t), (c.DOOR[1], c.H, c.W + t, c.H + t)]:
            fig.add_trace(poly_trace([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], WALL, WALL, 1), **kw)
    tx, ty = zip(*(c.TABLE + [c.TABLE[0]]))
    fig.add_trace(poly_trace(tx, ty, "#C3D1E3", BLUE, 2), **kw)
    cab = c.furniture()[1].union(c.furniture()[2])
    fig.add_trace(geom_trace(cab, "#E8D6E3", PURPLE), **kw)
    for (px, py), col in zip(c.POLES.values(), [PINK, GREEN]):
        fig.add_trace(geom_trace(c.circle(px, py, c.POLE_R), col, col, 1), **kw)


def disk(fig, x, y, th, row=None, col=None, body=True, color=FOOT, width=3):
    """The disk footprint (dashed circle of radius 0.25 m) with the RO-001 robot drawn inside."""
    kw = dict(row=row, col=col) if row else {}
    g = c.circle(x, y, c.R)
    fig.add_trace(geom_trace(g, "rgba(0,0,0,0.06)", color, width, "dash"), **kw)
    if body:
        for tr in robot((x, y, th), scale=1.0):
            fig.add_trace(tr, **kw)


def board_trace(x, y, th, color=FOOT, fill="rgba(140,86,75,0.45)", width=2):
    P = [(x + a, y + b) for a, b in c.board(th)]
    px, py = zip(*(P + [P[0]]))
    return poly_trace(px, py, fill, color, width)


def point(fig, x, y, color, text=None, pos="top center", size=14, row=None, col=None, tsize=18):
    kw = dict(row=row, col=col) if row else {}
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text" if text else "markers",
                             marker=dict(size=size, color=color, line=dict(color="white", width=1.5)),
                             text=[text] if text else None, textposition=pos,
                             textfont=dict(size=tsize, color=color), hoverinfo="skip"), **kw)


def axes(fig, xr, yr, row=None, col=None, dtick=1, title=True):
    kw = dict(row=row, col=col) if row else {}
    fig.update_xaxes(range=xr, dtick=dtick, title="x (m)" if title else None, showgrid=False, **kw)
    fig.update_yaxes(range=yr, dtick=dtick, title="y (m)" if title else None, showgrid=False,
                     scaleanchor="x" if not row else None, **kw)


def layout(fig, w, h, title=None, margin=None):
    fig.update_layout(template="simple_white", width=w, height=h, font=FONT, showlegend=False,
                      margin=margin or dict(l=80, r=30, t=90 if title else 30, b=70),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=22)) if title else None)
