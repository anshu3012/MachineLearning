"""Shared Plotly drawing for this Note's figures (no output when run on its own): the side view of the arm, the cup,
the bottle and the table, and the arm's C-space coloured by what each blocked configuration hits."""
import numpy as np
import plotly.graph_objects as go

import manip as m
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED

TABLE_FILL, TABLE_LINE = "#D9D9D9", "#7F7F7F"
BOTTLE_FILL, BOTTLE_LINE = "#B7DDB0", GREEN
CUP_FILL, CUP_LINE = "rgba(245,133,24,0.55)", ORANGE
LINK1, LINK2 = BLUE, ORANGE
# C-space colours: free, table or robot top, bottle, cup
CS_COLORS = ["#FFFFFF", "#BDBDBD", "#9DD49A", "#F8B878"]


def poly(fig, geom, fill, line, width=2, dash=None, **kw):
    x, y = geom.exterior.xy
    fig.add_trace(go.Scatter(x=list(x), y=list(y), mode="lines", fill="toself", fillcolor=fill,
                             line=dict(color=line, width=width, dash=dash), hoverinfo="skip"), **kw)


def scene(fig, cup_x=None, spot_b=True, **kw):
    """Table (and the robot's top level with it), the bottle, the cup standing at cup_x, and spot B dashed."""
    poly(fig, m.box(-0.30, -0.22, 0.62, m.TOP), TABLE_FILL, TABLE_LINE, **kw)
    fig.add_trace(go.Scatter(x=[0.05, 0.05], y=[-0.22, m.TOP], mode="lines", line=dict(color=TABLE_LINE, width=1.5,
                                                                                         dash="dot"),
                             hoverinfo="skip"), **kw)
    poly(fig, m.bottle(), BOTTLE_FILL, BOTTLE_LINE, **kw)
    if spot_b:
        poly(fig, m.cup_at(m.B_X), "rgba(0,0,0,0)", GREY, 1.5, "dash", **kw)
    if cup_x is not None:
        poly(fig, m.cup_at(cup_x), CUP_FILL, CUP_LINE, **kw)
    for x, t in ((-0.12, "robot's top"), (0.18, "A"), (0.33, "bottle"), (0.42, "B"), (0.54, "table")):
        fig.add_trace(go.Scatter(x=[x], y=[-0.15], mode="text", text=[t], textfont=dict(size=16, color="#4D4D4D"),
                                 hoverinfo="skip"), **kw)


def arm(fig, q, cup=False, color1=LINK1, color2=LINK2, width=7, opacity=1.0, bad=False, **kw):
    """The arm at joint angles q (degrees); with cup=True the cup hangs from the hand (red if it overlaps)."""
    (ex, ey), (hx, hy) = m.fk(*q)
    if cup:
        poly(fig, m.held_cup((hx, hy)), "rgba(228,87,86,0.55)" if bad else CUP_FILL, RED if bad else CUP_LINE, **kw)
    fig.add_trace(go.Scatter(x=[0, ex], y=[0, ey], mode="lines", line=dict(color=color1, width=width),
                             opacity=opacity, hoverinfo="skip"), **kw)
    fig.add_trace(go.Scatter(x=[ex, hx], y=[ey, hy], mode="lines", line=dict(color=color2, width=width),
                             opacity=opacity, hoverinfo="skip"), **kw)
    fig.add_trace(go.Scatter(x=[0, ex], y=[0, ey], mode="markers", opacity=opacity, hoverinfo="skip",
                             marker=dict(size=13, color="white", line=dict(color="black", width=2.5))), **kw)
    fig.add_trace(go.Scatter(x=[hx], y=[hy], mode="markers", marker=dict(size=9, color="black"), opacity=opacity,
                             hoverinfo="skip"), **kw)


def scene_axes(fig, row=None, col=None, xr=(-0.25, 0.6), yr=(-0.2, 0.52)):
    kw = dict(row=row, col=col) if row else {}
    fig.update_xaxes(range=list(xr), dtick=0.1, title="x (m)", showgrid=False, constrain="domain", **kw)
    fig.update_yaxes(range=list(yr), dtick=0.1, title="y (m)", showgrid=False, constrain="domain", **kw)


def cspace(fig, mode, **kw):
    g, C = m.cause_grid(mode, 1.0)
    cs = []
    for k, col in enumerate(CS_COLORS):
        cs += [[k / 4, col], [(k + 1) / 4, col]]
    fig.add_trace(go.Heatmap(x=g, y=g, z=C, zmin=-0.5, zmax=3.5, colorscale=cs, showscale=False, hoverinfo="skip"),
                  **kw)
    return C


def cs_axes(fig, row=None, col=None, ytitle=True):
    kw = dict(row=row, col=col) if row else {}
    fig.update_xaxes(range=[-180, 180], dtick=90, title="joint 1 (degrees)", showgrid=False, constrain="domain", **kw)
    fig.update_yaxes(range=[-180, 180], dtick=90, title="joint 2 (degrees)" if ytitle else None, showgrid=False, **kw)


def point(fig, q, color, text=None, pos="top center", size=13, **kw):
    fig.add_trace(go.Scatter(x=[q[0]], y=[q[1]], mode="markers+text" if text else "markers",
                             marker=dict(size=size, color=color, line=dict(color="black", width=1.5)),
                             text=[text] if text else None, textposition=pos, textfont=dict(size=17, color="black"),
                             hoverinfo="skip"), **kw)


def cs_path(fig, path, color, width=4, **kw):
    """A joint-space path, cut where it wraps across the edge of the square."""
    P = np.asarray(path)
    xs, ys = [P[0, 0]], [P[0, 1]]
    for a, b in zip(P, P[1:]):
        if abs(b[0] - a[0]) > 180 or abs(b[1] - a[1]) > 180:
            xs.append(None)
            ys.append(None)
        xs.append(b[0])
        ys.append(b[1])
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=width), hoverinfo="skip"), **kw)


def layout(fig, w, h, title=None, margin=None):
    fig.update_layout(template="simple_white", width=w, height=h, font=FONT, showlegend=False,
                      margin=margin or dict(l=80, r=30, t=90 if title else 40, b=70),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=22)) if title else None)
