"""The first six eigenvectors of MNIST (PCA components_, fitted on all 70,000 images), each reshaped to 28 x 28.
Red pixels count positively in that component, blue negatively. Ratios 9.7, 7.2, 6.1, ... percent."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "mnist_components.csv")
r, C = d.ratio.values, d.drop(columns="ratio").values
assert C.shape == (6, 784) and [round(100 * v, 1) for v in r[:3]] == [9.7, 7.2, 6.1]
assert np.allclose(np.linalg.norm(C, axis=1), 1, atol=1e-3)
fig = make_subplots(rows=2, cols=3, horizontal_spacing=0.03, vertical_spacing=0.09,
                    subplot_titles=[f"PC{i + 1}: {100 * v:.1f}% of the variance" for i, v in enumerate(r)])
m = np.abs(C).max()
for i in range(6):
    fig.add_heatmap(z=C[i].reshape(28, 28)[::-1], colorscale="RdBu_r", zmid=0, zmin=-m, zmax=m, showscale=False,
                    row=i // 3 + 1, col=i % 3 + 1)
fig.update_xaxes(visible=False); fig.update_yaxes(visible=False)
for k in range(1, 7):
    fig.update_xaxes(scaleanchor=f"y{k if k > 1 else ''}", row=(k - 1) // 3 + 1, col=(k - 1) % 3 + 1)
for a in fig.layout.annotations:
    a.font.size = 19
fig.update_layout(template="simple_white", width=1100, height=780, font=dict(family="Latin Modern Roman", size=17),
                  margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(here / "eigen_pictures.png", scale=2)
fig.write_image(here / "eigen_pictures.pdf")
