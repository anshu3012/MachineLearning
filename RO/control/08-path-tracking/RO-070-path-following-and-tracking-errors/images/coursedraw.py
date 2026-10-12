"""Drawing helpers for this Note's course figures (no output when run on its own): the test course, the car seen from
above (body, rear axle, front wheels at the steering angle), and the path-coordinate marks (nearest course point,
distance along the course, lateral error, heading error)."""
import re

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED
from trackkit import CAR_W, WHEELBASE, body, course_point, course_xy

XR, YR = (-2.5, 26.0), (-3.0, 24.0)


def _kw(rc):
    return dict(row=rc[0], col=rc[1]) if rc else {}


def minus(text):
    return re.sub(r"(?<![A-Za-z])-(?=\d)", "−", text)


def course(fig, rc=None, upto=None, color="#BDBDBD", width=10):
    """The course as a wide grey band with its centre line; upto: distance along it to draw thick (s so far)."""
    x, y = course_xy()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=color, width=width), hoverinfo="skip",
                             showlegend=False), **_kw(rc))
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color="white", width=1.5, dash="dash"),
                             hoverinfo="skip", showlegend=False), **_kw(rc))
    if upto is not None and upto > 0:
        s = np.linspace(0, upto, 200)
        p = np.array([course_point(v) for v in s])
        fig.add_trace(go.Scatter(x=p[:, 0], y=p[:, 1], mode="lines", line=dict(color=GREEN, width=5),
                                 hoverinfo="skip", showlegend=False), **_kw(rc))


def wheel(cx, cy, ang, length=0.7, width=0.25):
    c, s = np.cos(ang), np.sin(ang)
    pts = [(-length / 2, -width / 2), (length / 2, -width / 2), (length / 2, width / 2), (-length / 2, width / 2),
           (-length / 2, -width / 2)]
    return np.array([(cx + a * c - b * s, cy + a * s + b * c) for a, b in pts])


def car(fig, q, delta=0.0, color=BLUE, rc=None, fill="rgba(76,120,168,0.25)", width=2.5, wheels=True):
    """The car at pose q (rear axle middle, heading) with front wheels turned by delta."""
    kw = _kw(rc)
    b = body(q)
    fig.add_trace(go.Scatter(x=b[:, 0], y=b[:, 1], mode="lines", fill="toself", fillcolor=fill,
                             line=dict(color=color, width=width), hoverinfo="skip", showlegend=False), **kw)
    x, y, th = q
    c, s = np.cos(th), np.sin(th)
    if wheels:
        for side in (1, -1):
            off = side * (CAR_W / 2 - 0.2)
            rx, ry = x - s * off, y + c * off
            fx, fy = rx + WHEELBASE * c, ry + WHEELBASE * s
            for (wx, wy, a) in ((rx, ry, th), (fx, fy, th + delta)):
                w = wheel(wx, wy, a)
                fig.add_trace(go.Scatter(x=w[:, 0], y=w[:, 1], mode="lines", fill="toself", fillcolor="black",
                                         line=dict(color="black", width=1), hoverinfo="skip", showlegend=False), **kw)
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(color="black", size=7), hoverinfo="skip",
                             showlegend=False), **kw)


def arrow(fig, p0, p1, color, rc=None, width=3, dash=None, size=12):
    fig.add_trace(go.Scatter(x=[p0[0], p1[0]], y=[p0[1], p1[1]], mode="lines+markers",
                             line=dict(color=color, width=width, dash=dash), hoverinfo="skip", showlegend=False,
                             marker=dict(symbol="arrow", size=[0, size], angleref="previous", color=color)), **_kw(rc))


def arc(fig, c, r, a0, a1, color, rc=None, width=3, size=11):
    if abs(a1 - a0) < 2e-3:
        return
    t = np.linspace(a0, a1, 30)
    fig.add_trace(go.Scatter(x=c[0] + r * np.cos(t), y=c[1] + r * np.sin(t), mode="lines+markers",
                             line=dict(color=color, width=width), hoverinfo="skip", showlegend=False,
                             marker=dict(symbol="arrow", size=[0] * 29 + [size], angleref="previous", color=color)),
                  **_kw(rc))


def label(fig, x, y, text, color, rc=None, size=18, anchor="center"):
    fig.add_annotation(x=x, y=y, text=minus(text), showarrow=False, xanchor=anchor, font=dict(size=size, color=color),
                       bgcolor="rgba(255,255,255,0.85)", **_kw(rc))


def trail(fig, xs, ys, color, rc=None, width=3, dash=None):
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=width, dash=dash),
                             hoverinfo="skip", showlegend=False), **_kw(rc))


def frenet_marks(fig, q, s, e, the, rc=None, r_arc=2.2):
    """The nearest course point (orange), the lateral error from it to the rear axle (purple), the course's
    tangent there (dotted orange) and the heading error arc from the tangent to the car's heading (red)."""
    px, py, pth, _ = course_point(s)
    kw = _kw(rc)
    fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers", marker=dict(color=ORANGE, size=13,
                             line=dict(color="black", width=1)), hoverinfo="skip", showlegend=False), **kw)
    if abs(e) > 0.05:
        arrow(fig, (px, py), (q[0], q[1]), PURPLE, rc, width=4, size=12)
    t = (np.cos(pth), np.sin(pth))
    fig.add_trace(go.Scatter(x=[px - 1.0 * t[0], px + 4.2 * t[0]], y=[py - 1.0 * t[1], py + 4.2 * t[1]], mode="lines",
                             line=dict(color=ORANGE, width=2.5, dash="dot"), hoverinfo="skip", showlegend=False), **kw)
    fig.add_trace(go.Scatter(x=[q[0], q[0] + 4.2 * t[0]], y=[q[1], q[1] + 4.2 * t[1]], mode="lines",
                             line=dict(color=GREY, width=2, dash="dot"), hoverinfo="skip", showlegend=False), **kw)
    arc(fig, (q[0], q[1]), r_arc, pth, pth + the, RED, rc, width=4, size=12)


def axes(fig, rc=None, xr=XR, yr=YR):
    kw = _kw(rc)
    fig.update_xaxes(range=list(xr), showgrid=True, gridcolor="#EEEEEE", dtick=5, zeroline=False,
                     title=dict(text="x (m)", standoff=4), **kw)
    fig.update_yaxes(range=list(yr), showgrid=True, gridcolor="#EEEEEE", dtick=5, zeroline=False, scaleanchor="x",
                     scaleratio=1, title=dict(text="y (m)", standoff=4), **kw)


__all__ = ["course", "car", "arrow", "arc", "label", "trail", "frenet_marks", "axes", "minus", "XR", "YR",
           "BLUE", "GREEN", "GREY", "ORANGE", "PURPLE", "RED"]
