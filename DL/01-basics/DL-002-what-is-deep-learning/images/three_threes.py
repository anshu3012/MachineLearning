"""Three handwritten 3s from MNIST (the first three 3s of the test set, data/three_threes.npz) and the pixels they share.
A pixel counts as ink when its value is above 127. Plotly, because the picture is data (pixel grids)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
X = np.load(HERE.parent / "data" / "three_threes.npz")["images"]
ink = X > 127
n = ink.reshape(3, -1).sum(1)
common = ink.all(0)
print("ink pixels:", n, "in all three:", common.sum())
assert list(n) == [137, 100, 100] and common.sum() == 34, (n, common.sum())

titles = [f"<b>3 number {i + 1}</b><br>{n[i]} ink pixels" for i in range(3)] + \
         [f"<b>ink in all three</b><br>only {common.sum()} pixels"]
fig = make_subplots(rows=1, cols=4, subplot_titles=titles, horizontal_spacing=0.03)
for i in range(3):
    fig.add_heatmap(z=X[i][::-1], colorscale="Greys", showscale=False, row=1, col=i + 1)
fig.add_heatmap(z=common[::-1].astype(int), colorscale=[[0, "white"], [1, "#E45756"]], showscale=False, zmin=0, zmax=1,
                row=1, col=4)
fig.update_xaxes(visible=False, constrain="domain")
fig.update_yaxes(visible=False)
fig.update_annotations(font=dict(size=21))
fig.update_layout(template="simple_white", width=1200, height=400, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=10, r=10, t=80, b=10), plot_bgcolor="white")
fig.write_image(HERE / "three_threes.png", scale=2)
