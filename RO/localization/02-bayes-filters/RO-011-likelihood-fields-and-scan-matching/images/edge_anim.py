"""Figure 2 as an animation. One beam (330 degrees, reading 1.86 m) from poses (2, y, 0) as the robot slides down
the room 1 cm at a time, from y = 1.70 to 1.40 m. Left (equal scale): the ray cast from the current pose, blue
while it meets the box (z* = 1.85 m), orange once it slips under the box's corner and meets the bottom wall
(z* = 3.04 m from y = 1.52); the green dot is where the reading 1.86 m ends. Right: the beam model's density of the
reading (red) and the likelihood field's (green), drawn up to the current y. The beam model jumps from 5.88 to
0.0218 between y = 1.53 and 1.52; the field falls smoothly. The last frame is the still: both beams and both curves.
Run -> edge_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from beamref import mixture
from fieldmodel import distance_grid, endpoints, field, lookup, make_map, raycast
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from roomdraw import robot_marker, room_shapes

here = Path(__file__).parent
occ, _, _ = make_map()
F = field(distance_grid(occ))
A, Z = np.radians(330), 1.86
YS = np.round(np.arange(1.40, 1.701, 0.005), 3)                 # the curves, as in the still
BEAM = np.array([mixture(Z, raycast(occ, (2, y, 0), A)) for y in YS])
FLD = np.array([lookup(F, *endpoints((2, y, 0), np.array([Z]), np.array([A])))[0] for y in YS])
STEPS = np.round(np.arange(1.70, 1.399, -0.01), 2)               # the robot's positions, 1 cm apart


def info(y):
    zs = raycast(occ, (2, y, 0), A)
    ex, ey = endpoints((2, y, 0), np.array([Z]), np.array([A]))
    return zs, mixture(Z, zs), lookup(F, ex, ey)[0], (ex[0], ey[0])


def span(color, s):
    return f"<span style='color:{color}'>{s}</span>"


def base(title):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.52, 0.48], horizontal_spacing=0.09,
                        subplot_titles=["the 330° beam from the robot", "density of the reading 1.86 m"])
    room_shapes(fig, 1, 1)
    fig.add_annotation(x=3.9, y=0.9, text="box", showarrow=False, font=dict(size=18), row=1, col=1)
    fig.update_xaxes(range=[1.5, 5.1], dtick=1, title="x (m)", constrain="domain", row=1, col=1)
    fig.update_yaxes(range=[-0.1, 2.45], dtick=0.5, title="y (m)", scaleanchor="x", constrain="domain", row=1, col=1)
    fig.update_xaxes(title="robot position y (m)", range=[1.4, 1.7], dtick=0.05, row=1, col=2)
    fig.update_yaxes(title="density (per m)", range=[0, 6.5], row=1, col=2)
    fig.add_annotation(x=1.62, y=5.4, text="beam model", showarrow=False, font=dict(color=RED, size=18),
                       xref="x2", yref="y2")
    fig.add_annotation(x=1.62, y=3.1, text="likelihood field", showarrow=False, font=dict(color=GREEN, size=18),
                       xref="x2", yref="y2")
    fig.update_layout(template="simple_white", width=1200, height=640, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=130, b=70), title=dict(text=title, x=0.5, font_size=21))
    fig.update_annotations(selector=dict(yref="paper"), font_size=20)
    return fig


def ray(fig, y, label_at):
    zs = raycast(occ, (2, y, 0), A)
    col = BLUE if zs < 1.9 else ORANGE
    fig.add_trace(go.Scatter(x=[2, 2 + zs * np.cos(A)], y=[y, y + zs * np.sin(A)], mode="lines+markers",
                             line=dict(color=col, width=3), marker=dict(size=9)), row=1, col=1)
    lx, ly = label_at
    fig.add_annotation(x=lx, y=ly, xanchor="left", showarrow=False, text=f"from y = {y:.2f}: z* = {zs:.2f} m",
                       font=dict(color=col, size=17), row=1, col=1)


def curves(fig, upto):
    keep = YS >= upto - 1e-9
    fig.add_trace(go.Scatter(x=YS[keep], y=BEAM[keep], mode="lines", line=dict(color=RED, width=3, shape="hv")),
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=YS[keep], y=FLD[keep], mode="lines", line=dict(color=GREEN, width=3)), row=1, col=2)


def frame(y):
    zs, b, f, (ex, ey) = info(y)
    what = "the ray meets the box" if zs < 1.9 else "the ray slips under the box, to the bottom wall"
    title = (f"robot at y = {y:.2f} m: {what}, z* = {zs:.2f} m<br>"
             f"density of the reading: {span(RED, f'beam model {b:.3g}')}, {span(GREEN, f'likelihood field {f:.2f}')}")
    fig = base(title)
    ray(fig, y, (2.2, 1.9) if zs < 1.9 else (1.6, 0.3))
    fig.add_trace(go.Scatter(x=[ex], y=[ey], mode="markers", marker=dict(color=GREEN, size=13,
                                                                          line=dict(color="white", width=2))), row=1, col=1)
    fig.add_annotation(x=2.2, y=2.25, xanchor="left", showarrow=False, text="green dot: where the reading 1.86 m ends",
                       font=dict(color=GREEN, size=17), row=1, col=1)
    fig.add_trace(robot_marker((2, y, 0), size=0.12), row=1, col=1)
    curves(fig, y)
    fig.add_trace(go.Scatter(x=[y, y], y=[b, f], mode="markers", marker=dict(color=[RED, GREEN], size=14),
                             cliponaxis=False), row=1, col=2)
    return fig


def final():
    fig = base("one centimetre, from y = 1.53 to 1.52 m: the beam model jumps from 5.88 to 0.0218<br>"
               "while the likelihood field changes smoothly")
    ray(fig, 1.52, (1.6, 0.3))
    ray(fig, 1.53, (2.2, 1.9))
    curves(fig, YS[0])
    return fig


figs, holds, keys = [], [], [0]
for y in STEPS:
    figs.append(frame(y))
    holds.append({1.70: 6, 1.53: 8, 1.52: 10}.get(y, 1))
    if y in (1.53, 1.52):
        keys.append(len(figs) - 1)
figs.append(final())
holds.append(24)
keys.append(len(figs) - 1)
make_gif(figs, here / "edge_anim", fps=4, holds=holds, keys=keys, cols=2, width=950)

# the numbers the Note quotes (Section 2.2 table and caption)
z53, b53, f53, _ = info(1.53)
z52, b52, f52, _ = info(1.52)
assert (f"{z53:.2f}", f"{z52:.2f}") == ("1.85", "3.04")
assert (round(b53, 2), round(b52, 4)) == (5.88, 0.0218) and round(5.88 / 0.0218) == 270
assert (round(f53, 2), round(f52, 2)) == (3.59, 3.54)
assert np.abs(np.diff(FLD)).max() < 0.25 < 5.8 < np.abs(np.diff(BEAM)).max()   # field: small steps; beam model: one jump
