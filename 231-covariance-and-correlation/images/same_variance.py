"""Two tiny datasets with the same means and the same variances (2/3 each) but opposite directions: only the
covariance (+2/3 against -2/3, population version) tells them apart. Data: the Note's section 2 points."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
up = np.array([[-1, -1], [0, 0], [1, 1]]); down = np.array([[-1, 1], [0, 0], [1, -1]])
for d in (up, down):
    assert np.isclose(d[:, 0].var(), 2 / 3) and np.isclose(d[:, 1].var(), 2 / 3)
cov = lambda d: ((d[:, 0] - d[:, 0].mean()) * (d[:, 1] - d[:, 1].mean())).mean()
assert np.isclose(cov(up), 2 / 3) and np.isclose(cov(down), -2 / 3)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14, subplot_titles=[
    "rising: var x = var y = 2/3<br><b>covariance = +2/3</b>", "falling: var x = var y = 2/3<br><b>covariance = −2/3</b>"])
for j, (d, c) in enumerate(((up, "#4C78A8"), (down, "#E45756")), start=1):
    fig.add_scatter(x=d[:, 0], y=d[:, 1], mode="lines+markers", marker=dict(size=20, color=c), line=dict(color=c, width=2, dash="dot"),
                    row=1, col=j)
    fig.update_xaxes(range=[-1.6, 1.6], title_text="x", zeroline=True, row=1, col=j)
    fig.update_yaxes(range=[-1.6, 1.6], title_text="y", zeroline=True, row=1, col=j)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1100, height=560, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=19), margin=dict(l=60, r=30, t=110, b=60))
fig.write_image(here / "same_variance.png", scale=2)
fig.write_image(here / "same_variance.pdf")
