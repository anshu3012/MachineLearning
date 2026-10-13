"""Shared Plotly drawing for this Note's figures (no output when run on its own), adapted from RO-053's armdraw.py:
the side view of the arm, the table, the cup (orange), the bottle (green) and spot B (dashed)."""
import plotly.graph_objects as go

import tampkit as t
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED

TABLE_FILL, TABLE_LINE = "#D9D9D9", "#7F7F7F"
FILL = {"cup": "rgba(245,133,24,0.55)", "bottle": "#B7DDB0"}
LINE = {"cup": ORANGE, "bottle": GREEN}
BAD_FILL = "rgba(228,87,86,0.55)"


def poly(fig, geom, fill, line, width=2, dash=None, **kw):
    x, y = geom.exterior.xy
    fig.add_trace(go.Scatter(x=list(x), y=list(y), mode="lines", fill="toself", fillcolor=fill,
                             line=dict(color=line, width=width, dash=dash), hoverinfo="skip"), **kw)


def scene(fig, world, spot_b=True, bad=(), labels=True, **kw):
    """Table, robot's top, spot B dashed, and every standing object of `world` (red if its name is in `bad`)."""
    poly(fig, t.box(-0.30, -0.22, 0.62, t.TOP), TABLE_FILL, TABLE_LINE, **kw)
    fig.add_trace(go.Scatter(x=[0.05, 0.05], y=[-0.22, t.TOP], mode="lines",
                             line=dict(color=TABLE_LINE, width=1.5, dash="dot"), hoverinfo="skip"), **kw)
    if spot_b:
        poly(fig, t.standing("cup", t.B_X), "rgba(0,0,0,0)", GREY, 1.5, "dash", **kw)
    for o, x in world.at.items():
        poly(fig, t.standing(o, x), BAD_FILL if o in bad else FILL[o], RED if o in bad else LINE[o], **kw)
    if labels:
        for x, s in ((-0.12, "robot's top"), (0.18, "A"), (0.42, "B"), (0.55, "table")):
            fig.add_trace(go.Scatter(x=[x], y=[-0.15], mode="text", text=[s], hoverinfo="skip",
                                     textfont=dict(size=16, color="#4D4D4D")), **kw)


def standing_bad(fig, o, x, **kw):
    """Object o drawn standing at x in red: a placement that overlaps something."""
    poly(fig, t.standing(o, x), BAD_FILL, RED, 2.5, **kw)


def arm(fig, q, held=None, width=7, opacity=1.0, **kw):
    """The arm at joint angles q (degrees); a held object hangs below the hand."""
    (ex, ey), (hx, hy) = t.fk(*q)
    if held:
        poly(fig, t.hanging(held, (hx, hy)), FILL[held], LINE[held], **kw)
    fig.add_trace(go.Scatter(x=[0, ex], y=[0, ey], mode="lines", line=dict(color=BLUE, width=width),
                             opacity=opacity, hoverinfo="skip"), **kw)
    fig.add_trace(go.Scatter(x=[ex, hx], y=[ey, hy], mode="lines", line=dict(color="#C46A10", width=width),
                             opacity=opacity, hoverinfo="skip"), **kw)
    fig.add_trace(go.Scatter(x=[0, ex], y=[0, ey], mode="markers", opacity=opacity, hoverinfo="skip",
                             marker=dict(size=13, color="white", line=dict(color="black", width=2.5))), **kw)
    fig.add_trace(go.Scatter(x=[hx], y=[hy], mode="markers", marker=dict(size=9, color="black"), opacity=opacity,
                             hoverinfo="skip"), **kw)


def hand_trace(fig, path, color=GREY, width=2.5, dash="dot", **kw):
    """The hand's track along a joint-space path."""
    P = t.densify(path, 1.0)
    xs, ys = [], []
    for q in P:
        _, (hx, hy) = t.fk(*q)
        xs.append(float(hx))
        ys.append(float(hy))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=width, dash=dash),
                             hoverinfo="skip"), **kw)


def axes(fig, row=None, col=None, xr=(-0.25, 0.62), yr=(-0.2, 0.52)):
    kw = dict(row=row, col=col) if row else {}
    fig.update_xaxes(range=list(xr), dtick=0.1, title="x (m)", showgrid=False, constrain="domain", **kw)
    fig.update_yaxes(range=list(yr), dtick=0.1, title="y (m)", showgrid=False, constrain="domain", **kw)


def layout(fig, w, h, title=None, margin=None):
    fig.update_layout(template="simple_white", width=w, height=h, font=FONT, showlegend=False,
                      margin=margin or dict(l=80, r=30, t=90 if title else 40, b=70),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=22)) if title else None)
