"""Section 7.2: dividing each feature by its standard deviation (2 and 10) is the diagonal matrix diag(0.5, 0.1).
A cloud with those spreads becomes a round cloud; i-hat and j-hat only shrink along their own axes.
Toy data (seeded): 200 points, standard deviations 2 and 10. Run: python scaling_stretch.py -> scaling_stretch.png/.pdf"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, GREEN, RED = "#4C78A8", "#54A24B", "#E45756"
rng = np.random.default_rng(0)
X = rng.normal(0, [2, 10], size=(200, 2))
D = np.diag([1 / 2, 1 / 10])
assert np.allclose(D, [[0.5, 0], [0, 0.1]])                                   # the Note's matrix
Z = X @ D.T
print("spreads before", X.std(0).round(2), "after", Z.std(0).round(2))
assert np.allclose(Z.std(0), X.std(0) / [2, 10])

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=["before: spreads 2 and 10", "after diag(0.5, 0.1): both spreads about 1"])
for c, (P, ih, jh) in enumerate([(X, [1, 0], [0, 1]), (Z, [0.5, 0], [0, 0.1])], start=1):
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers", marker=dict(size=6, color=BLUE, opacity=0.55),
                             showlegend=False), row=1, col=c)
    for h, col, name in [(ih, GREEN, "i"), (jh, RED, "j")]:
        fig.add_trace(go.Scatter(x=[0, h[0]], y=[0, h[1]], mode="lines+markers", line=dict(color=col, width=6),
                                 marker=dict(size=[0, 10], color=col), name=f"{name} lands on {h}",
                                 showlegend=(c == 2)), row=1, col=c)
fig.update_xaxes(range=[-32, 32], row=1, col=1, title="feature 1")
fig.update_yaxes(range=[-32, 32], row=1, col=1, title="feature 2", scaleanchor="x", scaleratio=1)
fig.update_xaxes(range=[-3.5, 3.5], row=1, col=2, title="feature 1 / 2")
fig.update_yaxes(range=[-3.5, 3.5], row=1, col=2, title="feature 2 / 10", scaleanchor="x2", scaleratio=1)
fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=20),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "scaling_stretch.png", scale=2)
fig.write_image(HERE / "scaling_stretch.pdf")
