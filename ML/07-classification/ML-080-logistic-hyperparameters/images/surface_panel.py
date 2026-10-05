"""The probability surface behind c_boundary.gif, for C = 100 and C = 0.01 (same 300 points). Top: the surface
p = P(class 1) over (x1, x2); bottom: the same surface seen from above, with the contour lines p = 0.1, 0.5, 0.9
and the points (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from surface_tilt import surface_traces, scene

here = Path(__file__).parent
X, y = make_classification(n_samples=300, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                           class_sep=0.8, random_state=1)
xr, yr = [X[:, 0].min() - 0.5, X[:, 0].max() + 0.5], [X[:, 1].min() - 0.5, X[:, 1].max() + 0.5]
gx, gy = np.linspace(*xr, 100), np.linspace(*yr, 100)
GX, GY = np.meshgrid(gx, gy)
CS = [[0, "#C9DAEC"], [0.5, "#FFFFFF"], [1, "#FDDDB8"]]
Cs = (100, 0.01)
fig = make_subplots(2, 2, specs=[[{"type": "scene"}] * 2, [{}, {}]], row_heights=[0.45, 0.55], vertical_spacing=0.06,
                    horizontal_spacing=0.1, subplot_titles=[f"C = {c}: surface" for c in Cs] +
                    [f"C = {c}: seen from above" for c in Cs])
for col, c in enumerate(Cs, start=1):
    m = LogisticRegression(C=c, max_iter=10000).fit(X, y)
    P = m.predict_proba(np.c_[GX.ravel(), GY.ravel()])[:, 1].reshape(GX.shape)
    print("C", c, "p at the origin", round(float(m.predict_proba([[0, 0]])[0, 1]), 3), "coef", m.coef_[0].round(2))
    tr, zf = surface_traces(gx, gy, P, (0.1, 0.9, 0.4), colorscale=CS)
    for t in tr:
        fig.add_trace(t, 1, col)
    fig.update_scenes(scene(gx, gy, P, zf, "x₁", "x₂", "p", (1.6, -1.6, 1.0), 3), row=1, col=col)
    fig.add_trace(go.Contour(x=gx, y=gy, z=P, colorscale=CS, zmin=0, zmax=1, showscale=False,
                             contours=dict(start=0.1, end=0.9, size=0.4, showlabels=True),
                             line=dict(width=1.5, color="#555")), 2, col)
    for cls, color in ((0, "#4C78A8"), (1, "#F58518")):
        fig.add_trace(go.Scatter(x=X[y == cls, 0], y=X[y == cls, 1], mode="markers",
                                 marker=dict(color=color, size=6, line=dict(color="white", width=1))), 2, col)
    fig.update_xaxes(title="x₁", range=xr, row=2, col=col)
    fig.update_yaxes(title="x₂", range=yr, row=2, col=col)
fig.update_layout(template="simple_white", width=1100, height=980, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=10, r=20, t=50, b=60))
fig.update_annotations(font_size=18)
fig.write_image(here / "surface_panel.png", scale=2)
fig.write_image(here / "surface_panel.pdf")
