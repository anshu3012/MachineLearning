"""Drawing helpers for this Note's floor figures (no output when run on its own): the wall with the charging dock,
the robot as a disk of radius 0.25 m with its two wheels and a line for its heading, the dock pose, and the
quantities the controllers use (the distance rho, the angles alpha and beta, the distance e from a line)."""
import re

import numpy as np
import plotly.graph_objects as go
from drivekit import GOAL, R_ROBOT, WALL_Y
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED

XR, YR = (1.0, 5.8), (0.55, 4.15)
DOCK_X = (3.3, 3.9)


def _kw(rc):
    return dict(row=rc[0], col=rc[1]) if rc else {}


def floor(fig, rc=None, wall=True):
    """The wall at y = 3.75 m with the dock on it."""
    kw = _kw(rc)
    if not wall:
        return
    fig.add_trace(go.Scatter(x=[XR[0], XR[1]], y=[WALL_Y, WALL_Y], mode="lines", line=dict(color="black", width=6),
                             hoverinfo="skip", showlegend=False), **kw)
    x0, x1 = DOCK_X
    fig.add_trace(go.Scatter(x=[x0, x1, x1, x0, x0], y=[WALL_Y, WALL_Y, WALL_Y + 0.16, WALL_Y + 0.16, WALL_Y],
                             fill="toself", fillcolor="#FBD7B0", line=dict(color=ORANGE, width=2), mode="lines",
                             hoverinfo="skip", showlegend=False), **kw)
    fig.add_annotation(x=x1 + 0.08, y=WALL_Y + 0.1, text="dock", showarrow=False, xanchor="left",
                       font=dict(size=18, color=ORANGE), **kw)


def robot(fig, q, color=BLUE, rc=None, fill="rgba(255,255,255,0.75)", width=3, name=None):
    """The robot at pose q = (x, y, th): a disk, its two wheels 0.2 m apart, a line for its heading."""
    kw = _kw(rc)
    x, y, th = q
    t = np.linspace(0, 2 * np.pi, 48)
    fig.add_trace(go.Scatter(x=x + R_ROBOT * np.cos(t), y=y + R_ROBOT * np.sin(t), mode="lines", fill="toself",
                             fillcolor=fill, line=dict(color=color, width=width), hoverinfo="skip",
                             showlegend=name is not None, name=name or ""), **kw)
    c, s = np.cos(th), np.sin(th)
    for side in (1, -1):
        pts = np.array([(-0.05, side * 0.085), (0.05, side * 0.085), (0.05, side * 0.115), (-0.05, side * 0.115),
                        (-0.05, side * 0.085)])
        fig.add_trace(go.Scatter(x=x + c * pts[:, 0] - s * pts[:, 1], y=y + s * pts[:, 0] + c * pts[:, 1],
                                 mode="lines", fill="toself", fillcolor="black", line=dict(color="black", width=1),
                                 hoverinfo="skip", showlegend=False), **kw)
    fig.add_trace(go.Scatter(x=[x, x + R_ROBOT * c], y=[y, y + R_ROBOT * s], mode="lines",
                             line=dict(color=color, width=width + 1), hoverinfo="skip", showlegend=False), **kw)


def goal(fig, g=GOAL, rc=None, label="dock pose", color=ORANGE):
    """The goal pose: a dashed outline of the robot with an arrow for the wanted heading."""
    kw = _kw(rc)
    x, y, th = g
    t = np.linspace(0, 2 * np.pi, 48)
    fig.add_trace(go.Scatter(x=x + R_ROBOT * np.cos(t), y=y + R_ROBOT * np.sin(t), mode="lines",
                             line=dict(color=color, width=2, dash="dash"), hoverinfo="skip", showlegend=False), **kw)
    arrow(fig, (x, y), (x + 0.4 * np.cos(th), y + 0.4 * np.sin(th)), color, rc, width=3)
    if label:
        fig.add_annotation(x=x + 0.3, y=y - 0.12, text=label, showarrow=False, xanchor="left",
                           font=dict(size=17, color=color), **kw)


def arrow(fig, p0, p1, color, rc=None, width=3, dash=None, size=13):
    kw = _kw(rc)
    fig.add_trace(go.Scatter(x=[p0[0], p1[0]], y=[p0[1], p1[1]], mode="lines+markers",
                             line=dict(color=color, width=width, dash=dash), hoverinfo="skip", showlegend=False,
                             marker=dict(symbol="arrow", size=[0, size], angleref="previous", color=color)), **kw)


def arc(fig, c, r, a0, a1, color, rc=None, width=3, size=12):
    """An arc of radius r round c from angle a0 to a1 (rad), with an arrowhead at a1."""
    kw = _kw(rc)
    if abs(a1 - a0) < 1e-3:
        return
    t = np.linspace(a0, a1, 30)
    fig.add_trace(go.Scatter(x=c[0] + r * np.cos(t), y=c[1] + r * np.sin(t), mode="lines+markers",
                             line=dict(color=color, width=width), hoverinfo="skip", showlegend=False,
                             marker=dict(symbol="arrow", size=[0] * 29 + [size], angleref="previous", color=color)),
                  **kw)


def minus(text):
    """A true minus sign before a number (Plotly prints the ASCII hyphen)."""
    return re.sub(r"(?<![A-Za-z])-(?=\d)", "\u2212", text)


def label(fig, x, y, text, color, rc=None, size=18, anchor="center"):
    fig.add_annotation(x=x, y=y, text=minus(text), showarrow=False, xanchor=anchor, font=dict(size=size, color=color),
                       bgcolor="rgba(255,255,255,0.8)", **_kw(rc))


def trail(fig, xs, ys, color, rc=None, width=3, dash=None, name=None):
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=width, dash=dash),
                             hoverinfo="skip", showlegend=name is not None, name=name or ""), **_kw(rc))


def polar_marks(fig, q, rho, alpha, beta, rc=None, g=GOAL, show_beta=True, r_arc=0.6, labels=True, min_rho=0.8):
    """rho as a dashed line from the robot to the goal, alpha as an arc at the robot from its heading (dotted) to
    the line of sight, beta as an arc at the goal between the line of sight and the goal heading, drawn on the
    floor side of the goal (both lines continued backwards through the goal, which gives the same angle).
    alpha and beta are in rad and printed in degrees; the arcs are left out within min_rho of the goal."""
    x, y, th = q
    los = th + alpha
    if rho > 0.05:
        trail(fig, [x, g[0]], [y, g[1]], GREY, rc, width=2.5, dash="dash")
    fig.add_trace(go.Scatter(x=[x, x + 0.75 * np.cos(th)], y=[y, y + 0.75 * np.sin(th)], mode="lines",
                             line=dict(color=BLUE, width=2.5, dash="dot"), hoverinfo="skip", showlegend=False),
                  **_kw(rc))
    if rho <= min_rho:
        return
    arc(fig, (x, y), r_arc, th, los, RED, rc, width=4, size=14)
    if labels:
        mx, my = (x + g[0]) / 2, (y + g[1]) / 2
        nx, ny = -np.sin(los), np.cos(los)
        label(fig, mx + 0.3 * nx, my + 0.3 * ny, f"ρ = {rho:.2f} m", GREY, rc, size=18)
        a = th - np.sign(alpha if alpha != 0 else 1) * 0.5
        label(fig, x + 0.95 * np.cos(a), y + 0.95 * np.sin(a), f"α = {np.degrees(alpha):.1f}°", RED, rc, size=18)
    if show_beta:
        back = los + np.pi
        fig.add_trace(go.Scatter(x=[g[0], g[0] + 0.7 * np.cos(g[2] + np.pi)], y=[g[1], g[1] + 0.7 * np.sin(g[2] + np.pi)],
                                 mode="lines", line=dict(color=PURPLE, width=2, dash="dot"), hoverinfo="skip",
                                 showlegend=False), **_kw(rc))
        arc(fig, (g[0], g[1]), 0.5, back, back + beta, PURPLE, rc, width=4, size=14)
        if labels:
            b = g[2] + np.pi + np.sign(beta if beta != 0 else 1) * 0.45
            label(fig, g[0] + 0.85 * np.cos(b), g[1] + 0.85 * np.sin(b), f"β = {np.degrees(beta):.1f}°", PURPLE, rc,
                  size=18)


def axes(fig, rc=None, xr=XR, yr=YR):
    kw = _kw(rc)
    fig.update_xaxes(range=list(xr), showgrid=True, gridcolor="#EEEEEE", dtick=1, zeroline=False,
                     title=dict(text="x (m)", standoff=4), **kw)
    anchor = "x" if not rc or rc == (1, 1) else "x"
    fig.update_yaxes(range=list(yr), showgrid=True, gridcolor="#EEEEEE", dtick=1, zeroline=False,
                     scaleanchor=anchor, scaleratio=1, title=dict(text="y (m)", standoff=4), **kw)


__all__ = ["floor", "robot", "goal", "arrow", "arc", "label", "minus", "trail", "polar_marks", "axes", "XR", "YR",
           "BLUE", "GREEN", "GREY", "ORANGE", "PURPLE", "RED"]
