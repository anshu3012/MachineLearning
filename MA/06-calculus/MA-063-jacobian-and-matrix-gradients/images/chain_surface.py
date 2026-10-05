"""The surface of f(x, y) = x y^2 and the path x = 2t, y = t + 1 climbing it (Plotly 3-D frames), before the contour map
of chain_path.py. Same square (x 0..3.4, y 0.6..2.6), same contour heights (2, 4, ..., 20), same colours (darker =
lower). The point climbs to t = 1, where it sits at (2, 2) with height f = 8. The contour lines drop to the floor, and the
camera tilts from a side view to straight above: the floor is then the contour map of the next figure.
Run: python chain_surface.py -> chain_surface.gif, chain_surface_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.colors import sample_colorscale
from gifkit import FONT, make_gif

here = Path(__file__).parent
f = lambda x, y: x * y ** 2
path = lambda t: (2 * t, t + 1)
assert f(*path(1)) == 8
X0, X1, Y0, Y1 = 0, 3.4, 0.6, 2.6
gx, gy = np.linspace(X0, X1, 60), np.linspace(Y0, Y1, 60)
GX, GY = np.meshgrid(gx, gy)
CMAX = f(X1, Y1)
LEVELS = np.arange(2, 20.1, 2)
FLOOR, TOP = -9.0, 23.5
ys = np.linspace(Y0, Y1, 200)


def level(c):                                        # f = c  <=>  x = c / y^2
    x = c / ys ** 2
    return np.where(x <= X1, x, np.nan), ys


def colour(c):
    return sample_colorscale("Blues_r", [c / CMAX])[0]


def frame(t, drop=None, eye=(1.9, -1.5, 0.55), surf_op=0.8, floor_op=0.0, title="", top=False):
    """t: how far the point has climbed. drop: None = no contour lines, else 0..1 = how far they have fallen."""
    fig = go.Figure(go.Surface(x=gx, y=gy, z=f(GX, GY), colorscale="Blues", reversescale=True, cmin=0, cmax=CMAX,
                               showscale=False, opacity=surf_op, hoverinfo="skip"))
    fig.add_trace(go.Surface(x=gx, y=gy, z=FLOOR - 0.2 + 0 * GX, surfacecolor=f(GX, GY), colorscale="Blues",
                             reversescale=True, cmin=0, cmax=CMAX, showscale=False, opacity=max(floor_op, 0.08),
                             lighting=dict(ambient=1, diffuse=0, specular=0, fresnel=0)))
    if drop is not None:
        for c in LEVELS:
            lx, ly = level(c)
            fig.add_trace(go.Scatter3d(x=lx, y=ly, z=c + 0 * ly, mode="lines", line=dict(color=colour(c), width=5)))
            if drop > 0:
                z = c + (FLOOR + 0.1 - c) * drop
                fig.add_trace(go.Scatter3d(x=lx, y=ly, z=z + 0 * ly, mode="lines", line=dict(color=colour(c), width=5)))
    ts = np.linspace(0, t, 60)
    px, py = path(ts)
    fig.add_trace(go.Scatter3d(x=px, y=py, z=f(px, py) + 0.15, mode="lines", line=dict(color="black", width=8)))
    if drop:                                         # the path's shadow on the floor: the dotted path of the map
        fig.add_trace(go.Scatter3d(x=px, y=py, z=FLOOR + 0.1 + 0 * px, mode="lines",
                                   line=dict(color="#6B6B6B", width=5, dash="dot")))
    x, y = path(t)
    fig.add_trace(go.Scatter3d(x=[x, x], y=[y, y], z=[FLOOR, f(x, y)], mode="lines",
                               line=dict(color="black", width=3, dash="dot")))
    lab = f"t = {t:g}, f = {f(x, y):g}" if t == 1 else ""
    fig.add_trace(go.Scatter3d(x=[x, x], y=[y, y], z=[f(x, y) + 0.15, FLOOR + 0.1], mode="markers+text",
                               marker=dict(size=[8, 6], color="black"), text=["" if top else lab, "(2, 2)" if t == 1 else ""],
                               textposition="middle right", textfont=dict(size=19)))
    fig.update_scenes(xaxis=dict(title="x", range=[X0, X1], tickvals=[0, 1, 2, 3], tickfont=dict(size=17)),
                      yaxis=dict(title="y", range=[Y0, Y1], tickvals=[1, 1.5, 2, 2.5], tickfont=dict(size=17)),
                      zaxis=dict(title="" if top else "f", range=[FLOOR - 0.4, TOP], tickvals=[] if top else [0, 8, 16],
                                 tickfont=dict(size=17), showline=not top),
                      aspectmode="manual", aspectratio=dict(x=1.9, y=1.15, z=1.2),
                      camera=dict(eye=dict(zip("xyz", eye)), center=dict(x=0, y=0, z=-0.05),
                                  projection=dict(type="orthographic")))
    fig.update_layout(template="simple_white", width=900, height=700, font=FONT, showlegend=False,
                      margin=dict(l=0, r=0, t=60, b=0), title=dict(text=title, x=0.5, y=0.96, font=dict(size=23)))
    return fig


figs, holds, keys = [], [], []
figs.append(frame(0, title="f(x, y) = x·y²: a sheet that rises and bends upward")); holds.append(12); keys.append(0)
for t in (0.25, 0.5, 0.75, 1.0):
    x, y = path(t)
    figs.append(frame(t, title=f"the path climbs: t = {t:g}, (x, y) = ({x:g}, {y:g}), f = {f(x, y):g}"))
    holds.append(3)
holds[-1] = 12; keys.append(len(figs) - 1)
figs.append(frame(1, drop=0, title="lines of equal height 2, 4, ..., 20 on the sheet")); holds.append(10)
for d in (0.33, 0.67, 1.0):
    figs.append(frame(1, drop=d, title="the lines drop to the floor")); holds.append(1)
holds[-1] = 8; keys.append(len(figs) - 1)
N = 12
e0 = np.array([1.9, -1.5, 0.55])
r, a0 = np.hypot(*e0[:2]), np.arctan2(e0[1], e0[0])
for k, s in enumerate(np.linspace(0, 1, N)):
    phi = np.arctan2(e0[2], r) + (np.radians(89.9) - np.arctan2(e0[2], r)) * s
    a = a0 + (-np.pi / 2 - a0) * s                  # turn so that x ends pointing right, y up
    R = np.hypot(r, e0[2])
    eye = (R * np.cos(phi) * np.cos(a), R * np.cos(phi) * np.sin(a), R * np.sin(phi))
    last = k == N - 1
    figs.append(frame(1, drop=1, eye=eye, surf_op=0.8 * (1 - s), floor_op=0.55 * s, top=s > 0.75,
                      title="seen from straight above: the contour map" if last else "tilt the camera up"))
    holds.append(1)
holds[-1] = 20; keys.append(len(figs) - 1)
make_gif(figs, here / "chain_surface", fps=8, holds=holds, keys=keys)
