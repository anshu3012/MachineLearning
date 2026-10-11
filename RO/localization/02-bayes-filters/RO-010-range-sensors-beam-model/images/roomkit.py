"""Draw the Note's room in Plotly for the animations (no output when run on its own):
the 5 m x 4 m room with grey floor and walls, the blue robot with its orange heading arrow, the orange person."""
import numpy as np

from beammodel import ROOM
from gifkit import BLUE, FONT, GREY, ORANGE

FLOOR, ROBOT_FILL = "#F3F3F3", "#DBE4EE"      # cgrey!8 and cblue!20 of the TikZ figures
PERSON = (3.12, 2.0, 0.12)                     # centre x, y and radius (m): its near edge is 1.00 m ahead of pose A
C_NS = 0.299792458                             # speed of light, m per nanosecond


def axes(fig, ax="", xr=(-0.35, 5.35), yr=(-0.35, 4.35), dom=(0.0, 0.6), ydom=(0.0, 1.0), ticks=True, titles=True):
    """Equal-scale axes x{ax}, y{ax} for a room view; ticks every metre on the room's sides."""
    t = dict(tickmode="array", tickvals=list(range(6)), ticks="", showline=False, zeroline=False, showgrid=False,
             tickfont=dict(color=GREY, size=18))
    fig.update_layout(**{f"xaxis{ax}": dict(range=xr, domain=dom, anchor=f"y{ax}", constrain="domain", **t,
                                             showticklabels=ticks, title=dict(text="x (m)" if titles else "",
                                             font=dict(color=GREY, size=18), standoff=4)),
                         f"yaxis{ax}": dict(range=yr, domain=ydom, anchor=f"x{ax}", constrain="domain",
                                             scaleanchor=f"x{ax}", scaleratio=1, **{**t, "tickvals": list(range(5))},
                                             showticklabels=ticks, title=dict(text="y (m)" if titles else "",
                                             font=dict(color=GREY, size=18), standoff=4))})


def room(fig, ax=""):
    fig.add_shape(type="rect", x0=0, y0=0, x1=ROOM[0], y1=ROOM[1], xref=f"x{ax}", yref=f"y{ax}",
                  layer="below", opacity=1,
                  fillcolor=FLOOR, line=dict(color=GREY, width=6))


def robot(fig, x, y, th=0.0, ax="", label=None, arrow=0.42):
    fig.add_shape(type="rect", x0=x - 0.16, x1=x + 0.16, y0=y - 0.14, y1=y + 0.14, xref=f"x{ax}", yref=f"y{ax}",
                  fillcolor=ROBOT_FILL, line=dict(color=BLUE, width=3), opacity=1)
    fig.add_annotation(x=x + arrow * np.cos(th), y=y + arrow * np.sin(th), ax=x, ay=y, xref=f"x{ax}", yref=f"y{ax}",
                       axref=f"x{ax}", ayref=f"y{ax}", text="", showarrow=True, arrowhead=2, arrowsize=1,
                       arrowwidth=4, arrowcolor=ORANGE)
    if label:
        fig.add_annotation(x=x - 0.05, y=y - 0.2, xref=f"x{ax}", yref=f"y{ax}", text=label, showarrow=False,
                           xanchor="right", yanchor="top", font=dict(color=BLUE, size=FONT["size"] - 2))


def person(fig, ax="", label=True):
    cx, cy, r = PERSON
    fig.add_shape(type="circle", x0=cx - r, x1=cx + r, y0=cy - r, y1=cy + r, xref=f"x{ax}", yref=f"y{ax}",
                  fillcolor=ORANGE, line=dict(color=ORANGE, width=1), opacity=1)
    if label:
        fig.add_annotation(x=cx + 0.05, y=cy + 0.18, xref=f"x{ax}", yref=f"y{ax}", text="person", showarrow=False,
                           xanchor="left", yanchor="bottom", font=dict(color=ORANGE, size=FONT["size"] - 2))


def text(fig, x, y, s, color="black", size=None, anchor="left", ref=("paper", "paper"), **kw):
    """One line of text; in paper coordinates unless ref names data axes."""
    fig.add_annotation(x=x, y=y, xref=ref[0], yref=ref[1], text=s, showarrow=False, xanchor=anchor, yanchor="middle",
                       font=dict(color=color, size=size or FONT["size"] - 2), **kw)


def beam_view(fig, dom=(0.0, 0.48)):
    """The room, the robot at pose A and the stretch beyond the forward wall up to 5 m from the robot (x = 7),
    for readings that can land anywhere from 0 to 5 m."""
    axes(fig, xr=(-0.35, 7.6), yr=(-0.35, 4.9), dom=dom, titles=False)
    room(fig)
    fig.add_shape(type="line", x0=7, x1=7, y0=1.3, y1=2.7, line=dict(color=GREY, width=3, dash="dot"), opacity=1)
    text(fig, 7, 3.2, "5 m from<br>the robot", GREY, size=17, ref=("x", "y"), anchor="center")
    text(fig, 3.6, 2.4, "wall 3 m away", GREY, size=18, ref=("x", "y"), anchor="center")
    robot(fig, 2.0, 2.0)
