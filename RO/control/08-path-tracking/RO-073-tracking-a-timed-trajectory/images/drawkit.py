"""Drawing helpers shared by this Note's figure scripts (no output when run): a robot glyph and the timetable path."""
import numpy as np
import plotly.graph_objects as go
from trackkit import path_xy

GLYPH_R = 0.07          # m: radius of the drawn robot (a symbol, not the robot's 0.25 m size)


def robot(fig, pose, color, name=None, row=None, col=None, r=GLYPH_R, width=4, fill=0.35):
    """A circle with a line along the heading."""
    x, y, th = pose
    a = np.linspace(0, 2 * np.pi, 40)
    kw = dict(row=row, col=col) if row else {}
    fig.add_trace(go.Scatter(x=x + r * np.cos(a), y=y + r * np.sin(a), mode="lines", fill="toself",
                             line=dict(color=color, width=width), opacity=1, fillcolor=rgba(color, fill),
                             showlegend=name is not None, name=name or ""), **kw)
    fig.add_trace(go.Scatter(x=[x, x + 2 * r * np.cos(th)], y=[y, y + 2 * r * np.sin(th)], mode="lines",
                             line=dict(color=color, width=width), showlegend=False), **kw)


def rgba(hex_color, a):
    h = hex_color.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"


def timetable_path(fig, row=None, col=None, name="timetable's path"):
    px, py = path_xy()
    kw = dict(row=row, col=col) if row else {}
    fig.add_trace(go.Scatter(x=px, y=py, mode="lines", line=dict(color="#BBBBBB", width=10, simplify=False), name=name,
                             showlegend=name is not None), **kw)


def trail(fig, run, k, color, name=None, row=None, col=None, dash=None):
    kw = dict(row=row, col=col) if row else {}
    fig.add_trace(go.Scatter(x=run["x"][:k + 1], y=run["y"][:k + 1], mode="lines",
                             line=dict(color=color, width=3, dash=dash, simplify=False), showlegend=name is not None, name=name or ""),
                  **kw)
