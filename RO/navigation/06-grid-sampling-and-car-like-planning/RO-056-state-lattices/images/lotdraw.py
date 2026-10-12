"""Drawing helpers for the parking lot figures (no output when run on its own): the lot with its walls, parked cars
(grey), the target bay (dashed), optional 1 m grid cells, the car's body, paths and labels. Plotly, Latin Modern."""
import math

import numpy as np
import plotly.graph_objects as go
from carkit import BLOCKED, GOAL, LOT_H, LOT_W, NX, NY, PARKED, START, TARGET_X, body_corners
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED

FONT = dict(family="Latin Modern Roman", size=20)
CAR_FILL = "rgba(84,162,75,0.35)"


def _kw(rc):
    return dict(row=rc[0], col=rc[1]) if rc else {}


def lot(fig, rc=None, grid=False, cells=None, xr=(0, LOT_W), yr=(0, LOT_H)):
    """cells: dict (i, j) -> colour, drawn as filled 1 m squares centred on whole metres."""
    kw = _kw(rc)
    if grid:                                                        # blocked cells light grey, cell borders thin
        z = np.where(BLOCKED, 1.0, np.nan)
        fig.add_trace(go.Heatmap(z=z, x0=0, dx=1, y0=0, dy=1, zmin=0, zmax=1, showscale=False, hoverinfo="skip",
                                 colorscale=[[0, "#E4E4E4"], [1, "#E4E4E4"]]), **kw)
        gx, gy = [], []
        for v in np.arange(0.5, LOT_W, 1.0):
            gx += [v, v, None]
            gy += [0, LOT_H, None]
        for v in np.arange(0.5, LOT_H, 1.0):
            gx += [0, LOT_W, None]
            gy += [v, v, None]
        fig.add_trace(go.Scatter(x=gx, y=gy, mode="lines", line=dict(color="#D0D0D0", width=1), hoverinfo="skip"),
                      **kw)
    if cells:
        for (i, j), col in cells.items():
            fig.add_shape(type="rect", x0=i - 0.5, x1=i + 0.5, y0=j - 0.5, y1=j + 0.5, line=dict(width=0),
                          fillcolor=col, layer="below", opacity=1, **kw)
    for x0, x1, y0, y1 in PARKED:
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1, line=dict(color="#555555", width=1.5),
                      fillcolor="#9A9A9A", opacity=1, **kw)
    fig.add_shape(type="rect", x0=TARGET_X - 1.25, x1=TARGET_X + 1.25, y0=19.0, y1=24.0,
                  line=dict(color=ORANGE, width=2.5, dash="dash"), fillcolor="rgba(0,0,0,0)", opacity=1,
                  **kw)
    fig.add_shape(type="rect", x0=0, x1=LOT_W, y0=0, y1=LOT_H, line=dict(color="black", width=5),
                  fillcolor="rgba(0,0,0,0)", opacity=1, **kw)


def car(fig, pose, rc=None, colour=GREEN, fill=CAR_FILL, width=2.5, arrow=True):
    cs = body_corners(pose)
    xs, ys = zip(*(cs + [cs[0]]))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", fill="toself", fillcolor=fill,
                             line=dict(color=colour, width=width), hoverinfo="skip"), **_kw(rc))
    if arrow:                                                       # a short arrow from the rear axle forward
        x, y, th = pose
        fig.add_trace(go.Scatter(x=[x, x + 2.2 * math.cos(th)], y=[y, y + 2.2 * math.sin(th)], mode="lines",
                                 line=dict(color=colour, width=3), hoverinfo="skip"), **_kw(rc))
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(color=colour, size=7),
                                 hoverinfo="skip"), **_kw(rc))


def path(fig, pts, rc=None, colour=BLUE, width=4, dash=None, mode="lines", size=6):
    p = np.asarray(pts)
    fig.add_trace(go.Scatter(x=p[:, 0], y=p[:, 1], mode=mode, line=dict(color=colour, width=width, dash=dash),
                             marker=dict(color=colour, size=size), hoverinfo="skip"), **_kw(rc))


def label(fig, x, y, text, rc=None, size=18, colour="black", anchor="center"):
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="text", text=[text], textposition="middle " + anchor
                             if anchor != "center" else "middle center",
                             textfont=dict(size=size, color=colour, family=FONT["family"]), hoverinfo="skip"),
                  **_kw(rc))


def axes(fig, rc=None, xr=(0, LOT_W), yr=(0, LOT_H), ticks=True, pad=0.4):
    kw = _kw(rc)
    xname = "x" if not rc else fig.get_subplot(*rc).xaxis.plotly_name.replace("axis", "")
    fig.update_xaxes(range=[xr[0] - pad, xr[1] + pad], showgrid=False, zeroline=False, showline=False,
                     tickvals=[v for v in range(0, 25, 4) if xr[0] <= v <= xr[1]] if ticks else [],
                     showticklabels=ticks, tickfont=dict(size=15, color=GREY), constrain="domain", **kw)
    fig.update_yaxes(range=[yr[0] - pad, yr[1] + pad], showgrid=False, zeroline=False, showline=False,
                     tickvals=[v for v in range(0, 25, 4) if yr[0] <= v <= yr[1]] if ticks else [],
                     showticklabels=ticks, tickfont=dict(size=15, color=GREY), scaleanchor=xname, scaleratio=1,
                     constrain="domain", **kw)


def layout(fig, title, width=900, height=900, margin=None, subtitle=None):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False, font=FONT,
                      plot_bgcolor="white", title=dict(text=title, x=0.5, xanchor="center", font_size=23),
                      margin=margin or dict(l=30, r=30, t=110 if subtitle else 80, b=30))
    if subtitle:
        fig.add_annotation(x=0.5, y=1.0, xref="paper", yref="paper", text=subtitle, showarrow=False,
                           xanchor="center", yanchor="bottom", font=dict(size=18))
    return fig


__all__ = ["lot", "car", "path", "label", "axes", "layout", "START", "GOAL", "BLUE", "GREEN", "GREY", "ORANGE",
           "PURPLE", "RED"]
