"""The probability surface behind the 'unsure band' of separable_growth.gif: p = sigma(w0 + w1 x1 + w2 x2) for the
weights after 50,000 epochs on the perfectly separated points. Left: the surface; right: the same surface seen from
above with the contour lines p = 0.1, 0.5, 0.9 and the points (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from surface_tilt import surface_traces, scene

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=16)
sig = lambda z: 1 / (1 + np.exp(-z))
Xs, ys = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                             n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=20)
w = np.array([8.20, 6.52, 0.37])
XR, YR = [-4.6, 3.0], [-3.4, 2.6]
gx, gy = np.linspace(*XR, 120), np.linspace(*YR, 120)
P = sig(w[0] + w[1] * gx[None, :] + w[2] * gy[:, None])
CS = [[0, "#C9DAEC"], [0.5, "#FFFFFF"], [1, "#CDE6C6"]]
tr, zf = surface_traces(gx, gy, P, (0.1, 0.9, 0.4), colorscale=CS)
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {}]], horizontal_spacing=0.08,
                    subplot_titles=("the surface: height = p", "the same surface seen from above"))
for t in tr:
    fig.add_trace(t, 1, 1)
fig.update_scenes(scene(gx, gy, P, zf, "x₁", "x₂", "p", (-1.7, -1.7, 1.0), 3), row=1, col=1)
fig.add_trace(go.Contour(x=gx, y=gy, z=P, colorscale=CS, zmin=0, zmax=1, showscale=False,
                         contours=dict(start=0.1, end=0.9, size=0.4, showlabels=True), line=dict(width=1.5, color="#555")), 1, 2)
for k, c in ((1, "#54A24B"), (0, "#4C78A8")):
    fig.add_trace(go.Scatter(x=Xs[ys == k, 0], y=Xs[ys == k, 1], mode="markers",
                             marker=dict(color=c, size=8, line=dict(color="white", width=1))), 1, 2)
fig.update_xaxes(title="x₁", range=XR, row=1, col=2)
fig.update_yaxes(title="x₂", range=YR, row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=500, showlegend=False, font=FONT,
                  margin=dict(l=10, r=20, t=50, b=60))
fig.update_annotations(font_size=18)
fig.write_image(here / "surface_panel.png", scale=2)
fig.write_image(here / "surface_panel.pdf")
print("p at (0,0) =", round(float(sig(w[0])), 4))
