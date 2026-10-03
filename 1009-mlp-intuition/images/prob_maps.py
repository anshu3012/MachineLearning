"""Two perceptrons (sigmoid) and the perceptron that combines them: probability maps with the 0.5 boundary.
Our own weights (not from data): h1 = s(3(x1 + x2)), h2 = s(3(x1 - x2)), out = s(8 h1 + 8 h2 - 12)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
s = lambda z: 1 / (1 + np.exp(-z))
xs = np.linspace(-3, 3, 301)
X1, X2 = np.meshgrid(xs, xs)
H1, H2 = s(3 * (X1 + X2)), s(3 * (X1 - X2))
OUT = s(8 * H1 + 8 * H2 - 12)

rng = np.random.default_rng(0)                       # sample points, labelled by the combined model
P = rng.uniform(-2.8, 2.8, size=(160, 2))
lab = s(8 * s(3 * (P[:, 0] + P[:, 1])) + 8 * s(3 * (P[:, 0] - P[:, 1])) - 12) > 0.5

titles = ["Perceptron 1: σ(3x<sub>1</sub> + 3x<sub>2</sub>)", "Perceptron 2: σ(3x<sub>1</sub> − 3x<sub>2</sub>)", "Combined: σ(8·p<sub>1</sub> + 8·p<sub>2</sub> − 12)"]
fig = make_subplots(1, 3, subplot_titles=titles, horizontal_spacing=0.06)
for k, Z in enumerate([H1, H2, OUT], start=1):
    fig.add_trace(go.Contour(x=xs, y=xs, z=Z, colorscale=[[0, "#F6C9C9"], [0.5, "#FFFFFF"], [1, "#CBE5C5"]],
                             zmin=0, zmax=1, showscale=False, hoverinfo="skip",
                             contours=dict(start=0.1, end=0.9, size=0.1), line=dict(width=0.5, color="#BBBBBB")), 1, k)
    fig.add_trace(go.Contour(x=xs, y=xs, z=Z, showscale=False, hoverinfo="skip", contours_coloring="none", showlegend=False,
                             contours=dict(start=0.5, end=0.5, size=1), line=dict(width=4, color="black")), 1, k)
    for m, c in [(lab, "#54A24B"), (~lab, "#E45756")]:
        fig.add_trace(go.Scatter(x=P[m, 0], y=P[m, 1], mode="markers", showlegend=False,
                                 marker=dict(color=c, size=7, line=dict(color="white", width=0.8))), 1, k)
    fig.update_xaxes(title_text="x<sub>1</sub>", range=[-3, 3], row=1, col=k)
    fig.update_yaxes(range=[-3, 3], scaleanchor=f"x{'' if k == 1 else k}", row=1, col=k)
fig.update_yaxes(title_text="x<sub>2</sub>", row=1, col=1)
fig.update_annotations(font=dict(size=26))
fig.update_layout(template="simple_white", width=1350, height=500, font=dict(family="Latin Modern Roman", size=22),
                  margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(here / "prob_maps.png", scale=2)
fig.write_image(here / "prob_maps.pdf")
print("misclassified by p1 alone, p2 alone:", ((s(3 * (P[:, 0] + P[:, 1])) > 0.5) != lab).sum(), ((s(3 * (P[:, 0] - P[:, 1])) > 0.5) != lab).sum())
