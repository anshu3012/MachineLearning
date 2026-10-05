"""The surface of f(x, y) = x^3 + xy + y^2 next to its contour map (Plotly, still), before the Taylor-path animation.
Same square (0.3..1.7), same colours (Blues reversed: darker = lower), same path from (1, 1) to (1.5, 0.5) on both.
The contour lines are drawn on the surface and dropped to the floor. f(1, 1) = 3, f(1.5, 0.5) = 4.375.
Run: python taylor_surface.py -> taylor_surface.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, ORANGE

here = Path(__file__).parent
f = lambda x, y: x ** 3 + x * y + y ** 2
assert f(1, 1) == 3 and np.isclose(f(1.5, 0.5), 4.375)
g = np.linspace(0.3, 1.7, 141)
X, Y = np.meshgrid(g, g)
Z = f(X, Y)
ts = np.linspace(0, 0.5, 50)
px, py = 1 + ts, 1 - ts
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {"type": "xy"}]], column_widths=[0.55, 0.45], horizontal_spacing=0.06,
                    subplot_titles=["the surface f(x, y)", "seen from above: the contour map"])
fig.update_annotations(font_size=21)
fig.add_trace(go.Surface(x=g, y=g, z=Z, colorscale="Blues", reversescale=True, showscale=False, opacity=0.85,
                         contours_z=dict(show=True, start=0.5, end=8, size=0.5, color="#333333", width=2,
                                         project_z=True)), 1, 1)
fig.add_trace(go.Scatter3d(x=px, y=py, z=f(px, py) + 0.05, mode="lines", line=dict(color="black", width=6)), 1, 1)
fig.add_trace(go.Scatter3d(x=[1, 1.5], y=[1, 0.5], z=[3.05, 4.425], mode="markers+text", text=["f(1, 1) = 3", "f(1.5, 0.5) = 4.375"],
                           textposition=["top left", "top right"], textfont=dict(size=16),
                           marker=dict(size=6, color=[ORANGE, "black"])), 1, 1)
fig.update_scenes(xaxis=dict(title="x", range=[0.3, 1.7], tickvals=[0.5, 1, 1.5], tickfont=dict(size=14)), yaxis=dict(title="y", range=[0.3, 1.7], tickvals=[0.5, 1, 1.5], tickfont=dict(size=14)),
                  zaxis=dict(title="f", range=[0, 9], tickvals=[0, 3, 6, 9], tickfont=dict(size=14)), aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.8),
                  camera=dict(eye=dict(x=-1.55, y=-1.45, z=0.95), center=dict(x=0, y=0, z=-0.15)))
fig.add_trace(go.Contour(x=g, y=g, z=Z, colorscale="Blues", reversescale=True, showscale=False, opacity=0.6,
                         contours=dict(size=0.5), line=dict(width=0.5)), 1, 2)
fig.add_trace(go.Scatter(x=[1, 1.5], y=[1, 0.5], mode="lines", line=dict(color="black", dash="dot", width=2)), 1, 2)
fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers", marker=dict(size=14, color=ORANGE, line=dict(color="white", width=2))), 1, 2)
fig.update_xaxes(title="x", range=[0.3, 1.7], row=1, col=2)
fig.update_yaxes(title="y", range=[0.3, 1.7], scaleanchor="x", row=1, col=2)
fig.update_layout(template="simple_white", width=1250, height=600, font=FONT, showlegend=False,
                  margin=dict(l=0, r=30, t=60, b=60))
fig.write_image(here / "taylor_surface.png", scale=2)
