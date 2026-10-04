"""Three made-up datasets where PCA does not help (Plotly). Orange line: PC1. Below each: the points projected on PC1."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.decomposition import PCA

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
rng = np.random.default_rng(1)
n = 150
ang = rng.uniform(0, 2 * np.pi, n)
r = np.sqrt(rng.uniform(0, 1, n)) * 3
circle = np.c_[r * np.cos(ang), r * np.sin(ang)]
a = np.c_[rng.uniform(-3, 3, n), rng.normal(-0.6, 0.2, n)]
b = np.c_[rng.uniform(-3, 3, n), rng.normal(0.6, 0.2, n)]
clusters, lab = np.r_[a, b], np.r_[np.zeros(n), np.ones(n)]
x = rng.uniform(-2, 2, n)
curve = np.c_[x, x ** 2 - 1.3 + rng.normal(0, 0.08, n)]
cases = [("1. Same spread in every direction", circle, np.zeros(n)),
         ("2. Classes differ along the small spread", clusters, lab),
         ("3. A curved pattern", curve, np.zeros(n))]
fig = make_subplots(2, 3, row_heights=[0.8, 0.2], vertical_spacing=0.08, horizontal_spacing=0.06,
                    subplot_titles=[c[0] for c in cases] + ["", "", ""])
for col, (title, P, lbl) in enumerate(cases, start=1):
    p = PCA(1).fit(P)
    d, c = p.components_[0], p.mean_
    share = p.explained_variance_ratio_[0]
    colours = np.where(lbl == 1, RED, BLUE)
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers", marker=dict(size=6, color=colours, opacity=0.7)), 1, col)
    line = np.array([c - 4 * d, c + 4 * d])
    fig.add_trace(go.Scatter(x=line[:, 0], y=line[:, 1], mode="lines", line=dict(color=ORANGE, width=4)), 1, col)
    z = (P - c) @ d
    fig.add_trace(go.Scatter(x=z, y=rng.normal(0, 0.05, len(z)), mode="markers",
                             marker=dict(size=6, color=colours, opacity=0.5)), 2, col)
    fig.update_xaxes(range=[-4, 4], showticklabels=False, ticks="", row=1, col=col)
    fig.update_yaxes(range=[-4, 4], showticklabels=False, ticks="", scaleanchor=f"x{'' if col == 1 else col}", row=1, col=col)
    fig.update_xaxes(range=[-4, 4], showticklabels=False, ticks="", title=f"on PC1: {share:.0%} of the variance",
                     row=2, col=col)
    fig.update_yaxes(visible=False, range=[-0.5, 0.5], row=2, col=col)
    print(title, round(share, 3))
fig.update_layout(template="simple_white", width=1150, height=560, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=16), margin=dict(l=20, r=20, t=50, b=40))
fig.update_annotations(font_size=17)
fig.write_image(here / "pca_fails.png", scale=2)
fig.write_image(here / "pca_fails.pdf")
