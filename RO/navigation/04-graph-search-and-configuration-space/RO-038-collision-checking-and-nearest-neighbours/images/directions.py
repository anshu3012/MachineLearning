"""Figure: random directions. Top: 100,000 directions in the plane, as a rose of 10-degree bins. Left, a point drawn
evenly in the square [-1, 1] x [-1, 1] and scaled to length 1: directions near the diagonals come up 16.2 percent of
the time within 5 degrees, near the axes 8.6 percent, against a fair 11.1 percent. Right, a point from a normal
distribution in each coordinate: every direction equally often. Bottom: 1,500 points on the sphere from three
samplers. Uniform latitude angle: 28.7 percent fall in the two caps above |z| = 0.9 that hold 10 percent of the
surface. Uniform height (the bread slicer): 10.1 percent. The up arrow turned by Shoemake's random rotations: 10.0
percent. Run -> directions.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import collide as k
from gifkit import BLUE, FONT, GREEN, ORANGE, RED

here = Path(__file__).parent
S = k.sample_directions()
diag, axis = [45, 135, 225, 315], [0, 90, 180, 270]
sh = {n: round(k.near_share(S[n], c), 3) for n in ("square", "normal2") for c in (diag, axis) for _ in [0]}
assert round(k.near_share(S["square"], diag), 3) == 0.162 and round(k.near_share(S["square"], axis), 3) == 0.086
cap = {n: round(float(np.mean(np.abs(S[n][:, 2]) > 0.9)), 3) for n in ("latitude", "height", "rotated")}
assert cap == {"latitude": 0.287, "height": 0.101, "rotated": 0.100}
fig = make_subplots(rows=2, cols=3, specs=[[{"type": "polar"}, {"type": "polar"}, None],
                                           [{"type": "scene"}, {"type": "scene"}, {"type": "scene"}]],
                    row_heights=[0.45, 0.55], vertical_spacing=0.12,
                    subplot_titles=["square, then length 1", "normal, then length 1",
                                    f"uniform latitude: {cap['latitude'] * 100:.1f}% in the caps",
                                    f"uniform height: {cap['height'] * 100:.1f}% in the caps",
                                    f"Shoemake rotations: {cap['rotated'] * 100:.1f}% in the caps"])
for col, name, colr in [(1, "square", RED), (2, "normal2", GREEN)]:
    h, _ = np.histogram(S[name], bins=36, range=(0, 360))
    fig.add_trace(go.Barpolar(r=h / len(S[name]) * 100, theta=np.arange(5, 360, 10), width=[10] * 36,
                              marker_color=colr, opacity=0.8), row=1, col=col)
for col, name, colr in [(1, "latitude", RED), (2, "height", GREEN), (3, "rotated", GREEN)]:
    p = S[name][:1500]
    incap = np.abs(p[:, 2]) > 0.9
    fig.add_trace(go.Scatter3d(x=p[:, 0], y=p[:, 1], z=p[:, 2], mode="markers",
                               marker=dict(size=2.2, color=np.where(incap, ORANGE, BLUE))), row=2, col=col)
pol = dict(radialaxis=dict(range=[0, 4.6], tickvals=[2, 4], ticksuffix="%", tickfont=dict(size=13)),
           angularaxis=dict(tickfont=dict(size=13), dtick=45))
cam = dict(eye=dict(x=1.15, y=1.15, z=0.7))
sc = dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), aspectmode="cube",
          camera=cam)
fig.update_layout(polar=pol, polar2=pol, scene=sc, scene2=sc, scene3=sc, template="simple_white", font=FONT,
                  width=1350, height=1050, showlegend=False, margin=dict(l=30, r=30, t=70, b=20))
fig.add_annotation(x=0.84, y=0.86, xref="paper", yref="paper", align="left", showarrow=False, font=dict(size=18),
                   text=("within 5° of a diagonal:<br>square 16.2%, normal 11.1%<br><br>within 5° of an axis:<br>"
                         "square 8.6%, normal 11.1%<br><br>fair share: 11.1%"))
for a in fig.layout.annotations:
    if a.text and ("length 1" in a.text or "caps" in a.text):
        a.font.size = 20
        a.yshift = 22 if "length 1" in a.text else 0
fig.write_image(here / "directions.png")
