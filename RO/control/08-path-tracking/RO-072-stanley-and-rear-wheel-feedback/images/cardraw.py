"""Plotly drawing helpers for the path-tracking figures: the course, the car seen from above and arcs
(no output when run on its own)."""
import numpy as np
import plotly.graph_objects as go

from trackkit import L, S_END, course

BODY_BACK, BODY_FRONT, HALF_W = 0.75, 3.25, 0.9   # m: body 4.0 m long, 1.8 m wide, rear axle 0.75 m from the back (RO-055)
WHEEL = 0.7                                       # m, drawn wheel length


def course_trace(s_from=-2.0, s_to=S_END + 2.0, width=6, color="#BBBBBB", name="course", showlegend=False):
    s = np.linspace(s_from, s_to, 600)
    x, y, _, _ = course(s)
    return go.Scatter(x=x, y=y, mode="lines", line=dict(color=color, width=width), name=name, showlegend=showlegend,
                      hoverinfo="skip")


def rot(th, px, py):
    return np.cos(th) * px - np.sin(th) * py, np.sin(th) * px + np.cos(th) * py


def car_traces(x, y, th, delta, color, opacity=1.0, body=True):
    """The car as a body outline, its rear wheel and its steered front wheel (one wheel per axle, the bicycle)."""
    out = []
    if body:
        bx = np.array([-BODY_BACK, BODY_FRONT, BODY_FRONT, -BODY_BACK, -BODY_BACK])
        by = np.array([-HALF_W, -HALF_W, HALF_W, HALF_W, -HALF_W])
        rx, ry = rot(th, bx, by)
        out.append(go.Scatter(x=x + rx, y=y + ry, mode="lines", line=dict(color=color, width=2), fill="toself",
                              fillcolor="rgba(255,255,255,0.6)", opacity=opacity, showlegend=False, hoverinfo="skip"))
        ax, ay = rot(th, np.array([0, L]), np.array([0, 0]))
        out.append(go.Scatter(x=x + ax, y=y + ay, mode="lines", line=dict(color=color, width=1.5, dash="dot"),
                              opacity=opacity, showlegend=False, hoverinfo="skip"))
    for px, ang in ((0.0, 0.0), (L, delta)):
        wx, wy = rot(ang, np.array([-WHEEL / 2, WHEEL / 2]), np.array([0, 0]))
        wx, wy = wx + px, wy
        gx, gy = rot(th, wx, wy)
        out.append(go.Scatter(x=x + gx, y=y + gy, mode="lines", line=dict(color="black", width=6), opacity=opacity,
                              showlegend=False, hoverinfo="skip"))
    out.append(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(color=color, size=9, line=dict(color="black",
                          width=1)), opacity=opacity, showlegend=False, hoverinfo="skip"))
    return out


def arc_points(x, y, th, kappa, length, n=60):
    """Points along the arc of curvature kappa that leaves (x, y) along heading th, for the given arc length."""
    s = np.linspace(0, length, n)
    if abs(kappa) < 1e-9:
        return x + s * np.cos(th), y + s * np.sin(th)
    return (x + (np.sin(th + kappa * s) - np.sin(th)) / kappa, y + (np.cos(th) - np.cos(th + kappa * s)) / kappa)


def arc_length_to(kappa, chord):
    """Arc length of a circle of curvature kappa between two points a chord apart."""
    if abs(kappa) < 1e-9:
        return chord
    return 2 / abs(kappa) * np.arcsin(min(1.0, abs(kappa) * chord / 2))


def circle_points(cx, cy, r, n=120):
    a = np.linspace(0, 2 * np.pi, n)
    return cx + r * np.cos(a), cy + r * np.sin(a)
