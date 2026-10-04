"""Section 3.2: nine points centred on (0, 0) (a 3 x 3 grid of our own) have their mean at (0, 0); one outlier at
(20, 20) moves the mean to (2, 2), outside the group. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=18)
g = np.array([[x, y] for x in (-1, 0, 1) for y in (-1, 0, 1)], float)
allp = np.vstack([g, [[20, 20]]])
assert np.allclose(g.mean(0), 0) and np.allclose(allp.mean(0), [2, 2])
fig = go.Figure()
fig.add_scatter(x=g[:, 0], y=g[:, 1], mode="markers", marker=dict(size=12, color="#4C78A8"), name="nine points")
fig.add_scatter(x=[20], y=[20], mode="markers", marker=dict(size=14, color="#E45756", symbol="diamond"), name="outlier (20, 20)")
fig.add_scatter(x=[0], y=[0], mode="markers+text", marker=dict(size=16, color="black", symbol="x"), name="mean, 9 points")
fig.add_annotation(x=0, y=0, ax=8, ay=-1.8, axref="x", ayref="y", text="mean without the outlier (0, 0)", showarrow=True,
                   arrowhead=2, xanchor="left", font=dict(size=17))
fig.add_scatter(x=[2], y=[2], mode="markers+text", marker=dict(size=16, color="#E45756", symbol="x"), text=["mean with it (2, 2)"],
                textposition="top right", textfont=dict(color="#E45756"), name="mean, 10 points")
fig.update_layout(template="simple_white", width=900, height=560, font=FONT, showlegend=False,
                  xaxis=dict(range=[-3, 22], title="feature 1"), yaxis=dict(range=[-3, 22], title="feature 2", scaleanchor="x"),
                  margin=dict(l=60, r=20, t=20, b=60))
fig.write_image(here / "outlier_mean.png", scale=2)
fig.write_image(here / "outlier_mean.pdf")
