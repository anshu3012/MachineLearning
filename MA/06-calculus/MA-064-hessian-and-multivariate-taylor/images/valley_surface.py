"""The curved valley f(x, y) = (1 - x)^2 + 5(y - x^2)^2 as a surface next to the contour map of the optimiser race
(Plotly, still). Same square, same colours (Greys reversed on log10 f: darker = lower), same start (-1.2, 1) and
minimum (1, 1), f(1, 1) = 0. The floor of the valley follows the curve y = x^2.
Run: python valley_surface.py -> valley_surface.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, RED

here = Path(__file__).parent
f = lambda x, y: (1 - x) ** 2 + 5 * (y - x ** 2) ** 2
assert f(1, 1) == 0 and np.isclose(f(-1.2, 1), 5.808)
gx, gy = np.linspace(-1.6, 1.6, 200), np.linspace(-0.7, 1.9, 200)
X, Y = np.meshgrid(gx, gy)
Z = np.log10(f(X, Y) + 1e-3)                          # the race's map colours log10 f
CLIP = 20
sx, sy = np.linspace(-1.6, 1.6, 240), np.linspace(-0.7, 1.9, 240)
SX, SY = np.meshgrid(sx, sy)
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {"type": "xy"}]], column_widths=[0.55, 0.45], horizontal_spacing=0.05,
                    subplot_titles=["the surface: a curved valley", "seen from above: the contour map"])
fig.update_annotations(font_size=21)
fig.add_trace(go.Surface(x=sx, y=sy, z=np.where(f(SX, SY) <= CLIP, f(SX, SY), np.nan), surfacecolor=np.log10(f(SX, SY) + 1e-3),
                         colorscale="Greys", reversescale=True, cmin=Z.min(), cmax=Z.max(), showscale=False, opacity=0.95), 1, 1)
vx = np.linspace(-1.3, 1.3, 60)
fig.add_trace(go.Scatter3d(x=vx, y=vx ** 2, z=f(vx, vx ** 2) + 0.1, mode="lines", line=dict(color="#4C78A8", width=5, dash="dash")), 1, 1)
fig.add_trace(go.Scatter3d(x=[-1.2, 1], y=[1, 1], z=[f(-1.2, 1) + 0.3, 0.3], mode="markers+text", text=["start", "minimum (1, 1)"],
                           textposition=["top center", "top right"], textfont=dict(size=16),
                           marker=dict(size=[6, 7], color=["black", RED], symbol=["circle", "diamond"])), 1, 1)
fig.update_scenes(xaxis=dict(title="x", range=[-1.6, 1.6], tickvals=[-1, 0, 1], tickfont=dict(size=14)), yaxis=dict(title="y", range=[-0.7, 1.9], tickvals=[0, 1], tickfont=dict(size=14)),
                  zaxis=dict(title="f", range=[0, CLIP], tickvals=[0, 10, 20], tickfont=dict(size=14)), aspectmode="manual", aspectratio=dict(x=1.2, y=1, z=0.7),
                  camera=dict(eye=dict(x=0.5, y=-1.6, z=1.5), center=dict(x=0, y=0, z=-0.15)))
fig.add_trace(go.Contour(x=gx, y=gy, z=Z, colorscale="Greys", reversescale=True, showscale=False,
                         contours=dict(start=-2, end=2.5, size=0.25), line=dict(width=0.6), opacity=0.45), 1, 2)
fig.add_trace(go.Scatter(x=vx, y=vx ** 2, mode="lines", line=dict(color="#4C78A8", width=3, dash="dash")), 1, 2)
fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers", marker=dict(symbol="star", size=18, color=RED)), 1, 2)
fig.add_trace(go.Scatter(x=[-1.2], y=[1], mode="markers", marker=dict(size=11, color="black")), 1, 2)
fig.update_xaxes(title="x", range=[-1.6, 1.6], row=1, col=2)
fig.update_yaxes(title="y", range=[-0.7, 1.9], row=1, col=2)
fig.update_layout(template="simple_white", width=1250, height=600, font=FONT, showlegend=False,
                  margin=dict(l=0, r=30, t=60, b=60))
fig.write_image(here / "valley_surface.png", scale=2)
