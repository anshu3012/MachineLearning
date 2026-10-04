"""The flat cut, read back in 2D (Plotly), on the 34 points of the lift animation (seed 0). Left: each point's
height z = exp(-(x1^2 + x2^2)) against its distance r from the centre; the flat plane is the horizontal line halfway
between the lowest green and the highest red height. Right: the same cut in the original plane is the circle
r = sqrt(-ln z_cut), which puts every green point inside and every red point outside."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREEN, ORANGE, RED

here = Path(__file__).parent
rng = np.random.default_rng(0)
ang = rng.uniform(0, 2 * np.pi, 34)
inner = np.c_[np.cos(ang[:14]), np.sin(ang[:14])] * rng.uniform(0.1, 0.7, 14)[:, None]
outer = np.c_[np.cos(ang[14:]), np.sin(ang[14:])] * rng.uniform(1.5, 1.9, 20)[:, None]
zf = lambda P: np.exp(-(P ** 2).sum(1))
zg, zr = zf(inner), zf(outer)
cut = (zg.min() + zr.max()) / 2
rc = np.sqrt(-np.log(cut))
assert zg.min() > zr.max() and np.all(np.hypot(*inner.T) < rc) and np.all(np.hypot(*outer.T) > rc)
fig = make_subplots(1, 2, horizontal_spacing=0.12, subplot_titles=[f"height z against distance r: cut at z = {cut:.2f}",
                                                                   f"the same cut in the plane: a circle of radius {rc:.2f}"])
fig.update_annotations(font_size=21)
rr = np.linspace(0, 2, 200)
fig.add_trace(go.Scatter(x=rr, y=np.exp(-rr ** 2), mode="lines", line=dict(color="#999", width=2)), 1, 1)
for P, c in ((inner, GREEN), (outer, RED)):
    fig.add_trace(go.Scatter(x=np.hypot(*P.T), y=zf(P), mode="markers", marker=dict(size=11, color=c, line=dict(color="black", width=1))), 1, 1)
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers", marker=dict(size=11, color=c, line=dict(color="black", width=1))), 1, 2)
fig.add_trace(go.Scatter(x=[0, 2], y=[cut, cut], mode="lines", line=dict(color=ORANGE, width=4)), 1, 1)
t = np.linspace(0, 2 * np.pi, 300)
fig.add_trace(go.Scatter(x=rc * np.cos(t), y=rc * np.sin(t), mode="lines", line=dict(color=ORANGE, width=4)), 1, 2)
fig.update_xaxes(title="distance from the centre, r", range=[0, 2], row=1, col=1)
fig.update_yaxes(title="height z", range=[0, 1.05], row=1, col=1)
fig.update_xaxes(title="x₁", range=[-2.1, 2.1], row=1, col=2)
fig.update_yaxes(title="x₂", range=[-2.1, 2.1], scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1200, height=600, font=FONT, showlegend=False, margin=dict(l=70, r=20, t=60, b=70))
fig.write_image(here / "back_to_2d.png", scale=2)
