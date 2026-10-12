"""The door's numbers in metres as heights: each free cell of the room grid becomes a column as tall as its distance to
the door (3.414 at S, 0 at G, 11.12 at the far corner by the cabinet); blocked cells stay flat and grey. The camera
tilts from a side view down to straight above, and the last frames show the same map flat, each cell coloured by its
height with the number written in it: the colour code of the later figures. Run -> valley.gif, valley_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from drawkit import VSCALE, axes, heat, layout, numbers, outline, sg
from gifkit import FONT, make_gif
from gridplan import CELLS, GOAL, START, cost_to_go
from searchkit import BLOCKED, C, NX, NY

here = Path(__file__).parent
V = cost_to_go()
VMAX = max(V.values())
assert round(V[START], 3) == 3.414 and V[GOAL] == 0 and round(VMAX, 2) == 11.12
SCALE = VSCALE
ZS = 0.25                                                        # drawn height: 0.25 per metre of distance


def colour(v):
    t = v / VMAX
    stops = [(s, tuple(int(c[k:k + 2], 16) for k in (1, 3, 5))) for s, c in SCALE]
    for (s0, c0), (s1, c1) in zip(stops, stops[1:]):
        if t <= s1:
            u = (t - s0) / (s1 - s0)
            return "rgb(%d,%d,%d)" % tuple(round(a + u * (b - a)) for a, b in zip(c0, c1))
    return SCALE[-1][1]


def columns():
    """One Mesh3d per colour group would be heavy; one Mesh3d with a colour per face is enough."""
    xs, ys, zs, I, J, K, fc = [], [], [], [], [], [], []

    def quad(p, col):
        n = len(xs)
        for x, y, z in p:
            xs.append(x), ys.append(y), zs.append(z)
        I.extend([n, n]), J.extend([n + 1, n + 2]), K.extend([n + 2, n + 3]), fc.extend([col, col])

    for j in range(NY):
        for i in range(NX):
            x0, x1, y0, y1 = i * C, (i + 1) * C, j * C, (j + 1) * C
            if BLOCKED[j, i]:
                quad([(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], "rgb(138,138,138)")
                continue
            z, col = V[(i, j)] * ZS, colour(V[(i, j)])
            side = "rgb(%d,%d,%d)" % tuple(int(int(v) * 0.82) for v in col[4:-1].split(","))
            quad([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], col)
            for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
                quad([(a[0], a[1], 0), (b[0], b[1], 0), (b[0], b[1], z), (a[0], a[1], z)], side)
    return go.Mesh3d(x=xs, y=ys, z=zs, i=I, j=J, k=K, facecolor=fc, flatshading=True, hoverinfo="skip",
                     lighting=dict(ambient=1.0, diffuse=0.18, specular=0.0))


MESH = columns()


def tag(text, x, y, z):
    return go.Scatter3d(x=[x], y=[y], z=[z], mode="text", text=[f"<b>{text}</b>"], textfont=dict(size=22),
                        hoverinfo="skip")


def frame3d(t, title):
    """t from 0 (side view) to 1 (straight above)."""
    eye = dict(x=0.35 * (1 - t), y=-2.0 * (1 - t) - 0.002, z=1.25 + 0.45 * t)
    sx, sy = (START[0] + 0.5) * C, (START[1] + 0.5) * C
    gx, gy = (GOAL[0] + 0.5) * C, (GOAL[1] + 0.5) * C
    fig = go.Figure([MESH, tag("S", sx, sy, V[START] * ZS + 0.25), tag("G", gx, gy, 0.3)])
    fig.update_layout(template="simple_white", width=900, height=640, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5, xanchor="center", font_size=23),
                      margin=dict(l=0, r=0, t=70, b=0),
                      scene=dict(xaxis=dict(range=[0, 7], title=dict(text="x (m)", font_size=16), showbackground=False,
                                            tickvals=list(range(8)), tickfont_size=14),
                                 yaxis=dict(range=[0, 4], title=dict(text="y (m)", font_size=16), showbackground=False,
                                            tickvals=list(range(5)), tickfont_size=14),
                                 zaxis=dict(range=[0, VMAX * ZS + 0.3], title="", showticklabels=False,
                                            showbackground=False, showgrid=False),
                                 aspectmode="manual", aspectratio=dict(x=1.75, y=1.0, z=0.7),
                                 camera=dict(eye=eye, up=dict(x=0, y=t, z=1 - t), center=dict(x=0, y=0, z=-0.1),
                                             projection=dict(type="perspective" if t < 0.999 else "orthographic"))))
    return fig


def flat(show_numbers):
    fig = go.Figure()
    heat(fig, V, SCALE, VMAX)
    if show_numbers:
        numbers(fig, V, fmt="{:.2f}", size=16, dy=0.08)
    outline(fig, START, width=4)
    sg(fig, dy=-0.15, size=16)
    axes(fig)
    t = ("seen from above: colour = height = distance to the door" if not show_numbers else
         "the same map flat, with each cell's distance in metres")
    return layout(fig, t, width=900, height=640)


steps = np.linspace(0, 1, 14)
figs = [frame3d(t, "each cell's distance to the door as a height: a valley" if t < 0.5 else
                "tilting down to look from straight above") for t in steps]
figs += [flat(False), flat(True)]
holds = [12] + [2] * (len(steps) - 2) + [8, 8, 30]
make_gif(figs, here / "valley", fps=6, holds=holds, keys=[0, 9, 14, 15], cols=2, width=760)
