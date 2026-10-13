"""Shared drawing for this Note's room figures (no output when run on its own): costmap grids as coloured cells,
the plan, the robot, the person, on the part of the room RO-058's roomdraw.py shows (copied)."""
import math

import numpy as np
import plotly.graph_objects as go

import nav2sim as N
import roomdraw as rd
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED

# costmap colours: free white; inflated cost from pale yellow (1) to dark orange (252); 253 purple; 254 black
COST_SCALE = [[0.0, "#FFFFFF"], [0.004, "#FFF3C4"], [0.5, "#F8B24A"], [0.99, "#B5470B"], [0.993, "#7B4FA0"],
              [0.997, "#7B4FA0"], [1.0, "#000000"]]


def cost_cells(fig, cost, ox, oy, show_unknown=False, **kw):
    """A costmap grid as cells; 255 (unknown) drawn light grey if asked, else white."""
    c = cost.astype(float).copy()
    unk = c == N.NO_INFO
    c[unk] = 0
    ny, nx = c.shape
    xs = ox + (np.arange(nx) + 0.5) * N.RES
    ys = oy + (np.arange(ny) + 0.5) * N.RES
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=c, zmin=0, zmax=254, colorscale=COST_SCALE, showscale=False,
                             hoverinfo="skip"), **kw)
    if show_unknown and unk.any():
        fig.add_trace(go.Heatmap(x=xs, y=ys, z=np.where(unk, 1.0, np.nan), zmin=0, zmax=1,
                                 colorscale=[[0, "#E6E6E6"], [1, "#E6E6E6"]], showscale=False, hoverinfo="skip"), **kw)


def lethal_cells(fig, lethal, ox, oy, color="#000000", **kw):
    ny, nx = lethal.shape
    xs = ox + (np.arange(nx) + 0.5) * N.RES
    ys = oy + (np.arange(ny) + 0.5) * N.RES
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=np.where(lethal, 1.0, np.nan), zmin=0, zmax=1,
                             colorscale=[[0, color], [1, color]], showscale=False, hoverinfo="skip"), **kw)


def outline(fig, color="#7F7F7F", width=1.5, **kw):
    """The room's walls, table, cabinet and poles as thin outlines (the true geometry)."""
    D = N.D
    for a, b in D.WALLS:
        fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color=color, width=width),
                                 hoverinfo="skip"), **kw)
    t = list(D.TABLE) + [D.TABLE[0]]
    fig.add_trace(go.Scatter(x=[p[0] for p in t], y=[p[1] for p in t], mode="lines",
                             line=dict(color=color, width=width), hoverinfo="skip"), **kw)


def plan(fig, P, color=BLUE, width=3, dash=None, **kw):
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines", line=dict(color=color, width=width, dash=dash),
                             hoverinfo="skip"), **kw)


def robot(fig, pose, color="black", **kw):
    rc = (kw["row"], kw["col"]) if "row" in kw else None
    rd.robot(fig, pose[0], pose[1], pose[2], color, rc=rc)


def person(fig, label=True, **kw):
    rc = (kw["row"], kw["col"]) if "row" in kw else None
    rd.person(fig, N.D.PERSON, N.D.PERSON_R, rc=rc, label=label)


def goal(fig, **kw):
    g = N.GOAL
    fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="star", size=16, color=GREEN,
                             line=dict(color="black", width=1)), hoverinfo="skip"), **kw)
    fig.add_trace(go.Scatter(x=[g[0], g[0] + 0.25 * math.cos(g[2])], y=[g[1], g[1] + 0.25 * math.sin(g[2])],
                             mode="lines", line=dict(color=GREEN, width=3), hoverinfo="skip"), **kw)


def view(fig, xr=(1.3, 4.6), yr=(0.45, 4.25), **kw):
    fig.update_xaxes(range=list(xr), visible=False, **kw)
    fig.update_yaxes(range=list(yr), visible=False, **kw)


def layout(fig, w, h, title=None, margin=None):
    fig.update_layout(template="simple_white", width=w, height=h, font=FONT, showlegend=False,
                      margin=margin or dict(l=20, r=20, t=80 if title else 20, b=20),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=21)) if title else None)
