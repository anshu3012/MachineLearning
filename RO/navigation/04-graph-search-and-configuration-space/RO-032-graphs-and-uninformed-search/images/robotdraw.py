"""Shared drawing helper for this Note's Plotly figures: a differential-drive robot seen from above, and the
kinematic model used to move it (no output when run on its own)."""
import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, ORANGE

R_WHEEL, L = 0.05, 0.2                                      # wheel radius and wheel separation (m), as in the Note


def step(q, v, w, dt):
    """One Euler step of the kinematic model: x' = v cos(th), y' = v sin(th), th' = w."""
    x, y, th = q
    return (x + v * np.cos(th) * dt, y + v * np.sin(th) * dt, th + w * dt)


def _poly(pts, x, y, th):
    c, s = np.cos(th), np.sin(th)
    p = np.array(pts, dtype=float)
    return x + c * p[:, 0] - s * p[:, 1], y + s * p[:, 0] + c * p[:, 1]


def robot(q, scale=1.0, color=BLUE, opacity=1.0, arrow=True):
    """Traces of the robot at pose q = (x, y, th): body, two wheels and a heading arrow. scale enlarges the drawing."""
    x, y, th = q
    k = scale
    body = [(-0.15 * k, -0.1 * k), (0.11 * k, -0.1 * k), (0.11 * k, 0.1 * k), (-0.15 * k, 0.1 * k), (-0.15 * k, -0.1 * k)]
    wheel = lambda sgn: [(-0.05 * k, sgn * 0.1 * k), (0.05 * k, sgn * 0.1 * k), (0.05 * k, sgn * 0.125 * k),
                         (-0.05 * k, sgn * 0.125 * k), (-0.05 * k, sgn * 0.1 * k)]
    out = []
    bx, by = _poly(body, x, y, th)
    out.append(go.Scatter(x=bx, y=by, mode="lines", fill="toself", line=dict(color=color, width=2),
                          fillcolor="rgba(76,120,168,0.18)", opacity=opacity, hoverinfo="skip"))
    for sgn in (1, -1):
        wx, wy = _poly(wheel(sgn), x, y, th)
        out.append(go.Scatter(x=wx, y=wy, mode="lines", fill="toself", line=dict(color="black", width=1),
                              fillcolor="black", opacity=opacity, hoverinfo="skip"))
    if arrow:
        ax, ay = _poly([(0, 0), (0.2 * k, 0)], x, y, th)
        out.append(go.Scatter(x=ax, y=ay, mode="lines+markers", line=dict(color=ORANGE, width=4), opacity=opacity,
                              marker=dict(symbol="arrow", size=[0, 14 * min(k, 1.5)], angleref="previous",
                                          color=ORANGE), hoverinfo="skip"))
    return out
