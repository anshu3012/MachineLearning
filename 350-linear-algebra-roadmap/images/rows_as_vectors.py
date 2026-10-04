"""Why ML needs linear algebra, on real data: three iris flowers, one per species, as a table (a matrix, one row per observation) and as
vectors from the origin in feature space (petal length, petal width)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_iris

here = Path(__file__).parent
X = load_iris().data[[0, 50, 100]][:, 2:4]                  # petal length, petal width: one flower per species
assert X.shape == (3, 2) and tuple(X[0]) == (1.4, 0.2)
COL = ["#4C78A8", "#F58518", "#54A24B"]
fig = make_subplots(rows=1, cols=2, column_widths=[0.4, 0.6], specs=[[{"type": "table"}, {"type": "xy"}]],
                    subplot_titles=["the data as a 3 × 2 matrix", "each row is a vector"], horizontal_spacing=0.06)
fig.add_trace(go.Table(header=dict(values=["flower", "petal length", "petal width"], fill_color="#4C78A8",
                                   font=dict(color="white", size=18), height=36),
                       cells=dict(values=[[f"x{i + 1}" for i in range(3)], X[:, 0], X[:, 1]], height=34, font=dict(size=18),
                                  fill_color=[[c for c in COL], ["white"] * 3, ["white"] * 3],
                                  font_color=[["white"] * 3, ["black"] * 3, ["black"] * 3])), row=1, col=1)
for i, (x, y) in enumerate(X):
    fig.add_annotation(x=x, y=y, ax=0, ay=0, axref="x", ayref="y", xref="x", yref="y", showarrow=True, arrowhead=3,
                       arrowsize=1.5, arrowwidth=3, arrowcolor=COL[i])
    fig.add_scatter(x=[x], y=[y], mode="text", text=[f"x{i + 1} = ({x:g}, {y:g})"], textposition="middle right",
                    textfont=dict(size=16, color=COL[i]), row=1, col=2)
fig.update_xaxes(title_text="petal length (cm)", range=[0, 7], row=1, col=2)
fig.update_yaxes(title_text="petal width (cm)", range=[0, 2.6], row=1, col=2)
for a in fig.layout.annotations[:2]:
    a.font.size = 20
fig.update_layout(template="simple_white", width=1400, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=20, r=20, t=60, b=60))
fig.write_image(here / "rows_as_vectors.png", scale=2)
fig.write_image(here / "rows_as_vectors.pdf")
