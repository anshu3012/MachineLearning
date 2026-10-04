"""PCA step by step on 40 points in 3 columns (two classes), then projected onto PC1 and PC2 (Plotly).
Same data recipe as the original example: two 3-D normal clouds, means (0,0,0) and (1,1,1), seed 23."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
np.random.seed(23)
c1 = np.random.multivariate_normal([0, 0, 0], np.eye(3), 20)
c2 = np.random.multivariate_normal([1, 1, 1], np.eye(3), 20)
X = StandardScaler().fit_transform(np.vstack([c1, c2]))          # step 1: mean centre (and scale)
y = np.r_[np.ones(20), np.zeros(20)]
C = np.cov(X.T)                                                  # step 2
vals, vecs = np.linalg.eigh(C)                                   # step 3
order = np.argsort(vals)[::-1]
vals, vecs = vals[order], vecs[:, order]
W = vecs[:, :2].T                                                # step 4: top 2 eigenvectors as rows (2 x 3)
Z = X @ W.T                                                      # step 5: (40 x 3)(3 x 2) = 40 x 2
print("eigenvalues", vals.round(3), "share", (vals / vals.sum()).round(3))
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {"type": "xy"}]], column_widths=[0.55, 0.45],
                    subplot_titles=("40 points in 3 columns, with PC1 and PC2", "The same points on PC1 and PC2"))
for cls, colour in ((1, BLUE), (0, ORANGE)):
    m = y == cls
    fig.add_trace(go.Scatter3d(x=X[m, 0], y=X[m, 1], z=X[m, 2], mode="markers",
                               marker=dict(size=5, color=colour, line=dict(width=1, color="white"))), 1, 1)
    fig.add_trace(go.Scatter(x=Z[m, 0], y=Z[m, 1], mode="markers",
                             marker=dict(size=11, color=colour, line=dict(width=1, color="white"))), 1, 2)
for k, colour in ((0, RED), (1, GREEN)):
    tip = 2.2 * vecs[:, k]
    fig.add_trace(go.Scatter3d(x=[0, tip[0]], y=[0, tip[1]], z=[0, tip[2]], mode="lines+text",
                               line=dict(color=colour, width=9), text=["", f"PC{k + 1}"],
                               textfont=dict(color=colour, size=16)), 1, 1)
fig.update_scenes(xaxis_title="feature 1", yaxis_title="feature 2", zaxis_title="feature 3",
                  camera=dict(eye=dict(x=1.9, y=-1.8, z=1.0)), aspectmode="cube")
fig.update_xaxes(title=f"PC1 (variance {vals[0]:.2f})", row=1, col=2)
fig.update_yaxes(title=f"PC2 (variance {vals[1]:.2f})", scaleanchor="x", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=540, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=15), margin=dict(l=10, r=20, t=60, b=50))
fig.update_annotations(font_size=17)
fig.write_image(here / "pca_3d_to_2d.png", scale=2)
fig.write_image(here / "pca_3d_to_2d.pdf")
