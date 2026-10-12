"""The square of joint angles glued into a torus. The square holds every (theta1, theta2) from 0 to 2 pi. First its
orange edges, theta2 = 0 and theta2 = 2 pi (the same angle of joint 2), are rolled together: a tube. Then the tube
is stretched and bent until its blue ends, theta1 = 0 and theta1 = 2 pi, meet: a torus. Cutting the torus along the
two coloured lines runs the film backwards. The red point is the arm at (30, 60) degrees throughout.
Run: python glue_torus.py -> glue_torus.gif, glue_torus_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE, RED, make_gif

here = Path(__file__).parent
R, r = 2.0, 0.8                                              # the torus at the end: as in circles_torus.py
T1, T2 = np.radians(30), np.radians(60)


def shape(u, v, a, b):
    """Point (theta1 = u, theta2 = v) after rolling by a (0 flat, 1 a tube) and bending by b (0 straight, 1 a ring).
    The line v = pi stays fixed while rolling; arc lengths along the rolled direction are kept."""
    al = a * (v - np.pi)
    if a < 1e-6:
        w, z = 0 * v, r * (v - np.pi)
    else:
        rho = r / a
        w, z = rho - rho * np.cos(al), rho * np.sin(al)
    L = 2 * np.pi * r + b * (2 * np.pi * R - 2 * np.pi * r)  # length along theta1: the square's side, then 2 pi R
    s = (u - np.pi) / (2 * np.pi) * L
    if b < 1e-6:
        return w, s, z
    Rb = L / (2 * np.pi * b)
    rin = Rb - r
    phi = s / Rb
    return (rin + w) * np.cos(phi) - rin + b * (R - r), (rin + w) * np.sin(phi), z


# at the end the shape is the torus ((R + r cos v) cos(u - pi), (R + r cos v) sin(u - pi), -r sin v)
for uu, vv in ((0.3, 1.1), (2.0, 4.0)):
    x, y, z = shape(uu, vv, 1, 1)
    assert np.allclose((x, y, z), ((R + r * np.cos(vv)) * np.cos(uu - np.pi), (R + r * np.cos(vv)) * np.sin(uu - np.pi),
                                   -r * np.sin(vv)))


E0, E1 = np.array([1.35, -0.9, 1.0]), np.array([-0.7, -1.5, -0.9])


def frame(a, b, title):
    fig = go.Figure()
    U, V = np.meshgrid(np.linspace(0, 2 * np.pi, 61), np.linspace(0, 2 * np.pi, 41))
    X, Y, Z = shape(U, V, a, b)
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, surfacecolor=np.cos(V) + 0.6 * np.sin(V), cmin=-1.6, cmax=1.6,
                             colorscale=[[0, "rgb(160,183,210)"], [1, "rgb(225,233,243)"]], showscale=False,
                             opacity=1.0, lighting=dict(ambient=1.0, diffuse=0.0, specular=0.0)))
    t = np.linspace(0, 2 * np.pi, 120)
    for vv in (0, 2 * np.pi):                                # theta2 = 0 and 2 pi: orange
        x, y, z = shape(t, vv + 0 * t, a, b)
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color=ORANGE, width=9)))
    for uu in (0, 2 * np.pi):                                # theta1 = 0 and 2 pi: blue
        x, y, z = shape(uu + 0 * t, t, a, b)
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(color=BLUE, width=9)))
    p = np.array(shape(np.array(T1), np.array(T2), a, b), dtype=float)
    du = np.array(shape(np.array(T1 + 1e-4), np.array(T2), a, b), dtype=float) - p
    dv = np.array(shape(np.array(T1), np.array(T2 + 1e-4), a, b), dtype=float) - p
    nrm = np.cross(du, dv)
    nrm /= np.linalg.norm(nrm)
    eye = E0 + (0.5 * a + 0.5 * b) * (E1 - E0)
    p = p + 0.12 * nrm * np.sign(np.dot(nrm, eye))          # lift the marker off the surface, towards the viewer
    fig.add_trace(go.Scatter3d(x=[p[0]], y=[p[1]], z=[p[2]], mode="markers", marker=dict(size=10, color=RED)))
    fig.add_annotation(x=0.5, y=0.02, xref="paper", yref="paper", showarrow=False, font=dict(size=21, color=RED),
                       text="red point: the arm at (θ1, θ2) = (30°, 60°)")
    eye = E0 + (0.5 * a + 0.5 * b) * (E1 - E0)               # the camera turns while the square rolls and bends
    notes = []
    if a == 0 and b == 0:                                    # name the four edges of the flat square
        for (uu, vv, txt, col) in ((0, np.pi, "θ1 = 0  ", BLUE), (2 * np.pi, np.pi, "  θ1 = 2π", BLUE),
                                   (1.5 * np.pi, 0, "θ2 = 0", ORANGE), (np.pi, 2 * np.pi, "θ2 = 2π", ORANGE)):
            x, y, z = shape(np.array(uu), np.array(vv), 0, 0)
            notes.append(dict(x=float(x), y=float(y), z=float(z) + (0.35 if vv > 6 else -0.35 if vv == 0 else 0),
                              text=txt, showarrow=False, font=dict(size=21, color=col),
                              xanchor="right" if uu == 0 else "left" if uu > 6 else "center"))
    hide = dict(visible=False, range=[-3.2, 3.2])
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=760, showlegend=False,
                      margin=dict(l=0, r=0, t=120, b=0), title=dict(x=0.5, y=0.96, text=title),
                      scene=dict(xaxis=hide, yaxis=hide, zaxis=dict(visible=False, range=[-3.2, 3.2]),
                                 aspectmode="cube", annotations=notes,
                                 camera=dict(eye=dict(zip('xyz', eye)))))
    return fig


figs, holds = [], []
figs.append(frame(0, 0, "the square of joint angles: θ1 along, θ2 across, each from 0 to 2π<br>"
                        "<span style='font-size:19px'>orange edges: θ2 = 0 and 2π; blue edges: θ1 = 0 and 2π</span>"))
holds.append(6)
for a in (0.2, 0.4, 0.6, 0.8, 0.95, 1.0):
    figs.append(frame(a, 0, "roll it until the orange edges meet:<br>θ2 = 0 and θ2 = 2π are the same angle, so glue them"))
    holds.append(1)
holds[-1] = 5
for b in (0.15, 0.3, 0.5, 0.7, 0.85, 0.95, 1.0):
    figs.append(frame(1, b, "stretch and bend the tube until the blue ends meet:<br>θ1 = 0 and θ1 = 2π are the same angle"))
    holds.append(1)
figs.append(frame(1, 1, "a torus, seen from below: every point is one configuration of the arm,<br>and no edge is left"))
holds.append(12)
make_gif(figs, here / "glue_torus", fps=2, holds=holds, keys=[0, 6, 10, len(figs) - 1], cols=2, width=760)
