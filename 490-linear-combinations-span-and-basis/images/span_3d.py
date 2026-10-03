"""Span in 3D: two independent vectors span a plane through the origin; a third vector on that plane adds
nothing (dependent), a third vector off it unlocks all of 3D space (independent)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
v1, v2 = np.array([2, 0, 1]), np.array([0, 2, 1])          # span: all (2a, 2b, a + b), the plane z = (x + y) / 2
on, off = v1 + v2, np.array([0, 0, 2.5])                     # [2, 2, 2] lies on it, [0, 0, 2.5] does not
assert np.linalg.matrix_rank(np.column_stack([v1, v2, on])) == 2
assert np.linalg.matrix_rank(np.column_stack([v1, v2, off])) == 3
g = np.linspace(-2.5, 2.5, 21)
X, Y = np.meshgrid(g, g)

fig = go.Figure()
fig.add_trace(go.Surface(x=X, y=Y, z=(X + Y) / 2, colorscale=[[0, "#AFC4E0"], [1, "#AFC4E0"]], opacity=0.7,
                         showscale=False, name="span of v1 and v2"))


def arrow(v, colour, name, dash="solid"):
    fig.add_trace(go.Scatter3d(x=[0, v[0]], y=[0, v[1]], z=[0, v[2]], mode="lines", name=name,
                               line=dict(color=colour, width=9, dash=dash)))
    fig.add_trace(go.Cone(x=[v[0]], y=[v[1]], z=[v[2]], u=[v[0]], v=[v[1]], w=[v[2]], sizemode="absolute",
                          sizeref=0.35, anchor="tip", colorscale=[[0, colour], [1, colour]], showscale=False,
                          showlegend=False))


arrow(v1, "#4C78A8", "v1 = [2, 0, 1]")
arrow(v2, "#4C78A8", "v2 = [0, 2, 1]")
arrow(on, "#54A24B", "[2, 2, 2] = v1 + v2: on the plane, dependent")
arrow(off, "#E45756", "[0, 0, 2.5]: off the plane, independent")
fig.update_layout(template="simple_white", width=900, height=650, font=dict(family="Latin Modern Roman", size=16),
                  title=dict(text="Two vectors span a plane; a third vector either lies on it or leaves it", x=0.5),
                  scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z", aspectmode="cube",
                             xaxis=dict(range=[-2.5, 2.5], tickfont=dict(size=12)), yaxis=dict(range=[-2.5, 2.5], tickfont=dict(size=12)),
                             zaxis=dict(range=[-3, 3], tickfont=dict(size=12)),
                             camera=dict(eye=dict(x=0.4, y=-2.2, z=0.6))),
                  legend=dict(x=0.0, y=1.0), margin=dict(l=0, r=0, t=60, b=0))
fig.write_image(here / "span_3d.png", scale=2)
fig.write_image(here / "span_3d.pdf")
