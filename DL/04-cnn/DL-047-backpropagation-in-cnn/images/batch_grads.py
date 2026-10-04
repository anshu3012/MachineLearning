"""Section 7: for a batch of 32 images, each image gives its own dL/dW2 = (a2 - y) F^T (dots); the batch gradient
(1/m)(A2 - Y) F^T is their average (black bar). Same data and starting weights as the Notebook (Plotly)."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from mnist_small import HERE, SMALL, Y, W2, b2, F_of
from common import BLUE, RED, FONT

m = 32
Fs = np.hstack([F_of(SMALL[i]) for i in range(m)])                       # 4 x m
A2s = 1 / (1 + np.exp(-(W2 @ Fs + b2)))
per = (A2s - Y[:m]) * Fs                                                 # 4 x m: column i = image i's gradient
batch = ((A2s - Y[:m]) @ Fs.T / m).ravel()
assert np.allclose(per.mean(axis=1), batch)
g0 = pd.read_csv(HERE.parent / "data" / "last_layer_grads.csv").value.to_numpy()[:4]
assert np.allclose(per[:, 0], g0)                                       # image 1 = section 6.2's example
rng = np.random.default_rng(0)
fig = go.Figure()
for k in range(4):
    for lab, c, sel in (("image of a 0 (y = 0)", BLUE, Y[:m] == 0), ("image of a 1 (y = 1)", RED, Y[:m] == 1)):
        fig.add_trace(go.Scatter(x=k + 0.18 * rng.uniform(-1, 1, sel.sum()), y=per[k, sel], mode="markers",
                                 marker=dict(size=10, color=c, opacity=0.7), name=lab, showlegend=k == 0))
    fig.add_trace(go.Scatter(x=[k - 0.3, k + 0.3], y=[batch[k]] * 2, mode="lines", line=dict(color="black", width=4),
                             name="batch gradient = average", showlegend=k == 0))
fig.add_hline(y=0, line=dict(color="#BBBBBB", width=1))
fig.update_layout(template="simple_white", width=950, height=500, font=dict(FONT, size=18),
                  xaxis=dict(tickvals=list(range(4)), ticktext=[f"∂L/∂w<sub>{k + 1}</sub>" for k in range(4)]),
                  yaxis=dict(title="gradient"), legend=dict(orientation="h", x=0, y=1.12),
                  margin=dict(l=80, r=20, t=60, b=50))
fig.write_image(HERE / "batch_grads.png", scale=2)
fig.write_image(HERE / "batch_grads.pdf")
