"""The words of the Note on the Note's own data (Plotly table): the first five observations of the make_regression
data. Blue columns are the features x1 and x2, the orange column is the target y, and the green row is one
observation."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_regression

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=2, n_informative=2, noise=50, random_state=7)
assert X.shape == (100, 2)
rows = 5
fill = lambda base: [["#DDF0D8" if i == 2 else base for i in range(rows)]]
fig = go.Figure(go.Table(
    columnwidth=[90, 150, 150, 150],
    header=dict(values=["<b>row</b>", "<b>feature 1 (x₁)</b>", "<b>feature 2 (x₂)</b>", "<b>target (y)</b>"],
                fill_color=["white", "#4C78A8", "#4C78A8", "#F58518"], font=dict(color=["black", "white", "white", "white"], size=24),
                height=50, align="center", line_color="white"),
    cells=dict(values=[list(range(1, rows + 1)), np.round(X[:rows, 0], 2), np.round(X[:rows, 1], 2), np.round(y[:rows], 1)],
               fill_color=[fill("white")[0], fill("#E4EDF6")[0], fill("#E4EDF6")[0], fill("#FDE9D4")[0]],
               font=dict(size=24), height=46, align="center", line_color="white")))
fig.add_annotation(x=0.5, y=-0.02, xref="paper", yref="paper", showarrow=False, font=dict(size=22, color="#54A24B"),
                   text="green row: one observation (one student, one house, one record)")
fig.update_layout(width=1000, height=350, font=dict(family="Latin Modern Roman"), margin=dict(l=10, r=10, t=10, b=40))
fig.write_image(here / "data_table.png", scale=2)
