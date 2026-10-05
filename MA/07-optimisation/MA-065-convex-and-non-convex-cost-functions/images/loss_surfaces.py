"""One dataset, two models, two loss surfaces and their contour maps (Plotly: 3-D surfaces on top, the same surfaces
seen from above, as contour maps, below; same colours, same marked points).
Data: 21 points x = -2, -1.8, ..., 2 with y = 1.5 tanh(2x).
Left: straight line y = m x + b, MSE over (m, b): a single convex bowl, one minimum.
Right: tiny neural network y = w2 tanh(w1 x), MSE over (w1, w2): two global minima, (2, 1.5) and (-2, -1.5),
both with loss 0, and a ridge between them (loss 1.71 at (0, 0))."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
GREEN, ORANGE = "#54A24B", "#F58518"
xs = np.linspace(-2, 2, 21)
ys = 1.5 * np.tanh(2 * xs)

mg, bg = np.linspace(-1.0, 3.0, 161), np.linspace(-2.0, 2.0, 161)
M, B = np.meshgrid(mg, bg)
lr = ((ys - M[..., None] * xs - B[..., None]) ** 2).mean(-1)
g1, g2 = np.linspace(-4, 4, 201), np.linspace(-3, 3, 201)
W1, W2 = np.meshgrid(g1, g2)
nn = ((ys - W2[..., None] * np.tanh(W1[..., None] * xs)) ** 2).mean(-1)
assert nn.min() < 0.01 and abs((ys ** 2).mean() - 1.7145) < 1e-3
k = np.unravel_index(lr.argmin(), lr.shape)
m_best, b_best = M[k], B[k]

fig = make_subplots(rows=2, cols=2, horizontal_spacing=0.1, vertical_spacing=0.06, row_heights=[0.5, 0.5],
                    specs=[[{"type": "scene"}, {"type": "scene"}], [{"type": "xy"}, {"type": "xy"}]],
                    subplot_titles=("straight line y = mx + b: the surface", "tiny network y = w2 tanh(w1 x): the surface",
                                    "the same surface from above: convex", "the same surface from above: non-convex"))
CS = dict(colorscale="Blues", reversescale=True, cmin=0, cmax=6)
LINES = dict(show=True, usecolormap=False, color="#2F4B7C", width=2, start=0.1, end=6, size=0.5, project=dict(z=True))
fig.add_trace(go.Surface(x=mg, y=bg, z=np.minimum(lr, 6), showscale=False, contours=dict(z=LINES), **CS,
                         lighting=dict(ambient=1, diffuse=0.1, specular=0)), 1, 1)
fig.add_trace(go.Surface(x=g1, y=g2, z=np.minimum(nn, 6), showscale=False, contours=dict(z=LINES), **CS,
                         lighting=dict(ambient=1, diffuse=0.1, specular=0)), 1, 2)
fig.add_trace(go.Scatter3d(x=[m_best], y=[b_best], z=[lr.min() + 0.1], mode="markers", marker=dict(size=6, color=GREEN)), 1, 1)
fig.add_trace(go.Scatter3d(x=[2, -2], y=[1.5, -1.5], z=[0.1, 0.1], mode="markers", marker=dict(size=6, color=GREEN)), 1, 2)
fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[1.71 + 0.1], mode="markers", marker=dict(size=6, color=ORANGE)), 1, 2)
fig.add_trace(go.Contour(x=mg, y=bg, z=lr, colorscale="Blues", reversescale=True, zmin=0, zmax=6, showscale=False, opacity=1,
                         contours=dict(start=0.1, end=6, size=0.5), line=dict(width=1)), 2, 1)
fig.add_trace(go.Contour(x=g1, y=g2, z=np.minimum(nn, 6), colorscale="Blues", reversescale=True, zmin=0, zmax=6, showscale=False, opacity=1,
                         contours=dict(start=0.1, end=6, size=0.5), line=dict(width=1)), 2, 2)
fig.add_trace(go.Scatter(x=[m_best], y=[b_best], mode="markers", marker=dict(size=13, color=GREEN)), 2, 1)
fig.add_trace(go.Scatter(x=[2, -2], y=[1.5, -1.5], mode="markers", marker=dict(size=13, color=GREEN)), 2, 2)
fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=11, color=ORANGE)), 2, 2)
for x, y, t, c, ref, ys in ((m_best, b_best, "one minimum", GREEN, 1, 22), (2, 1.5, "minimum, loss 0", GREEN, 2, -22),
                          (-2, -1.5, "minimum, loss 0", GREEN, 2, 22), (0, 0, "(0, 0): loss 1.71", ORANGE, 2, -22)):
    fig.add_annotation(x=x, y=y, text=t, showarrow=False, yshift=ys, font=dict(color=c, size=17), bgcolor="white",
                       xref="x" if ref == 1 else "x2", yref="y" if ref == 1 else "y2")
fig.update_xaxes(title_text="m", row=2, col=1)
fig.update_yaxes(title_text="b", row=2, col=1)
fig.update_xaxes(title_text="w1", row=2, col=2)
fig.update_yaxes(title_text="w2", row=2, col=2)
cam = dict(eye=dict(x=-1.3, y=-1.6, z=0.9), projection=dict(type="orthographic"))
for sc, (xt, yt) in (("scene", ("m", "b")), ("scene2", ("w1", "w2"))):
    fig.update_layout({sc: dict(xaxis=dict(title=xt, showbackground=False, tickfont=dict(size=13)), yaxis=dict(title=yt, showbackground=False, tickfont=dict(size=13)),
                                zaxis=dict(title="loss", range=[0, 6], showbackground=False, tickfont=dict(size=13)), camera=cam,
                                aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.7))})
fig.update_layout(template="simple_white", width=1150, height=980, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=60, r=20, t=50, b=55))
fig.write_image(here / "loss_surfaces.png", scale=2)
fig.write_image(here / "loss_surfaces.pdf")
print(round(m_best, 3), round(b_best, 3), round(lr.min(), 3))
