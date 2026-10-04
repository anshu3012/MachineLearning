"""One collection of vectors, two pictures: iris flowers as feature vectors [petal length, petal width]. Left: 10
flowers drawn as arrows from the origin. Right: all 150 flowers drawn as points, one at the tip of each arrow."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_iris

here = Path(__file__).parent
X = load_iris().data[:, 2:4]
assert X.shape == (150, 2)
pick = X[::15]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=["10 flowers as arrows", "150 flowers as points"])
for x, y in pick:
    fig.add_annotation(x=x, y=y, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", arrowhead=2, arrowwidth=2,
                       arrowcolor="#4C78A8")
fig.add_scatter(x=X[:, 0], y=X[:, 1], mode="markers", marker=dict(size=7, color="#4C78A8", opacity=0.6), row=1, col=2)
for c in (1, 2):
    fig.update_xaxes(title_text="petal length (cm)", range=[0, 7.2], row=1, col=c)
    fig.update_yaxes(title_text="petal width (cm)", range=[0, 2.7], row=1, col=c)
for a in fig.layout.annotations[:2]:
    a.font.size = 20
fig.update_layout(template="simple_white", width=1300, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=60, b=60))
fig.write_image(here / "arrows_points.png", scale=2)
fig.write_image(here / "arrows_points.pdf")
