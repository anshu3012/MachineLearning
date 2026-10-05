"""How a contour map is made from a surface (Plotly 3-D frames). The bowl f(x1, x2) = x1^2 + x1 x2 + 2 x2^2, f(1, 1) = 4.
Horizontal planes cut the bowl at heights 2, 5, 8 and 11; each cut is a ring on the surface, and the ring drops to the
floor. Then the other rings of Figure 2 (gradient_arrows.py: levels 0.5, 2, ..., 14, same colours, same square) drop
too, and the camera tilts from a side view to straight above: the floor is now the contour map of Figure 2.
Run: python contour_build.py -> contour_build.gif, contour_build_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.colors import sample_colorscale
from gifkit import FONT, make_gif

here = Path(__file__).parent
f = lambda a, b: a ** 2 + a * b + 2 * b ** 2
assert f(1, 1) == 4
R = 2.2                                              # the square of Figure 2
g = np.linspace(-R, R, 60)
X, Y = np.meshgrid(g, g)
CMAX = f(R, R)                                       # Figure 2 spans the colours over 0..f(2.2, 2.2)
Z = np.minimum(f(X, Y), 14.5)                        # cut the corners so the bowl's rim is level
LEVELS = np.arange(0.5, 14.01, 1.5)                  # the contour lines of Figure 2
CUTS = [2.0, 5.0, 8.0, 11.0]                         # the slices shown one at a time
FLOOR = -6.0
TOP = 15.0
th = np.linspace(0, 2 * np.pi, 240)
lam, Q = np.linalg.eigh(np.array([[1, 0.5], [0.5, 2]]))     # f = x^T A x, so a level set is an ellipse


def ring(c):
    e = Q @ (np.sqrt(c / lam)[:, None] * np.vstack([np.cos(th), np.sin(th)]))
    e[:, (np.abs(e) > R).any(axis=0)] = np.nan       # clip to the square, as the contour map is
    return e


def colour(c):                                       # the colour Figure 2 gives height c (Blues, reversed)
    return sample_colorscale("Blues_r", [c / CMAX])[0]


def frame(rings, plane=None, eye=(1.0, -1.9, 0.45), surf_op=0.75, floor_op=0.0, title="", top=False):
    """rings: list of (level, z where the ring is drawn now)."""
    fig = go.Figure(go.Surface(x=X, y=Y, z=Z, colorscale="Blues", reversescale=True, cmin=0, cmax=CMAX,
                               showscale=False, opacity=surf_op, hoverinfo="skip"))
    fig.add_trace(go.Surface(x=g, y=g, z=FLOOR - 0.15 + 0 * X, surfacecolor=f(X, Y), colorscale="Blues", reversescale=True,
                             cmin=0, cmax=CMAX, showscale=False, opacity=max(floor_op, 0.08),
                             lighting=dict(ambient=1, diffuse=0, specular=0, fresnel=0)))
    if plane is not None:
        fig.add_trace(go.Surface(x=g, y=g, z=plane + 0 * X, colorscale=[[0, "#F58518"], [1, "#F58518"]],
                                 showscale=False, opacity=0.35))
    for c, z in rings:
        e = ring(c)
        fig.add_trace(go.Scatter3d(x=e[0], y=e[1], z=c + 0 * th, mode="lines", line=dict(color=colour(c), width=6)))
        if z < c:                                    # the copy that falls to the floor
            fig.add_trace(go.Scatter3d(x=e[0], y=e[1], z=max(z, FLOOR + 0.1) + 0 * th, mode="lines", line=dict(color=colour(c), width=6)))
    fig.add_trace(go.Scatter3d(x=[1, 1], y=[1, 1], z=[FLOOR, 4], mode="lines", line=dict(color="black", width=3, dash="dot")))
    fig.add_trace(go.Scatter3d(x=[1, 1], y=[1, 1], z=[4, FLOOR], mode="markers+text", marker=dict(size=[7, 6], color="black"),
                               text=["" if top else "f = 4", "(1, 1)"], textposition="middle right", textfont=dict(size=18)))
    fig.update_scenes(xaxis=dict(title="x1", range=[-R, R], tickvals=[-2, 0, 2], tickfont=dict(size=17)),
                      yaxis=dict(title="x2", range=[-R, R], tickvals=[-2, 0, 2], tickfont=dict(size=17)),
                      zaxis=dict(title="" if top else "f", range=[FLOOR - 0.3, TOP], tickvals=[] if top else [0, 4, 8, 12], tickfont=dict(size=17), showline=not top),
                      aspectmode="manual", aspectratio=dict(x=1.45, y=1.45, z=1.3),
                      camera=dict(eye=dict(zip("xyz", eye)), center=dict(x=0, y=0, z=-0.05),
                                  projection=dict(type="orthographic")))
    fig.update_layout(template="simple_white", width=900, height=720, font=FONT, showlegend=False,
                      margin=dict(l=0, r=0, t=60, b=0), title=dict(text=title, x=0.5, y=0.96, font=dict(size=24)))
    return fig


figs, holds, keys = [], [], []
figs.append(frame([], title="the bowl f(x1, x2); the dot is f(1, 1) = 4")); holds.append(12); keys.append(0)
done = []
for c in CUTS:
    t = f"cut the bowl at height f = {c:g}"
    figs.append(frame(done + [(c, c)], plane=c, title=t)); holds.append(6)
    if c == 5.0:
        keys.append(len(figs) - 1)
    for z in np.linspace(c, FLOOR, 5)[1:]:
        figs.append(frame(done + [(c, z)], title=f"the ring at height {c:g} drops to the floor")); holds.append(1)
    done.append((c, FLOOR)); holds[-1] = 4
allr = [(c, FLOOR) for c in LEVELS]
figs.append(frame(allr, title="every height 0.5, 2, 3.5, ..., 14 gets its ring")); holds.append(10); keys.append(len(figs) - 1)
N = 12
for k, s in enumerate(np.linspace(0, 1, N)):
    phi = np.radians(13 + (89.9 - 13) * s)           # camera height angle: side view -> straight above
    alpha = np.radians(28 * (1 - s))                 # and turn so that x1 ends pointing right
    r = 2.15
    eye = (r * np.sin(alpha) * np.cos(phi), -r * np.cos(alpha) * np.cos(phi), r * np.sin(phi))
    last = k == N - 1
    figs.append(frame(allr, eye=eye, surf_op=0.75 * (1 - s), floor_op=0.55 * s,
                      title="seen from straight above: the contour map" if last else "tilt the camera up", top=s > 0.75)); holds.append(1)
holds[-1] = 22; keys.append(len(figs) - 1)
make_gif(figs, here / "contour_build", fps=8, holds=holds, keys=keys)
