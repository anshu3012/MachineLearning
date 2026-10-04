"""The 12 validation photos the plain CNN gets wrong with the highest confidence (data/mistakes.npz from
experiments/mistakes.py). Above each photo: the true label, then what the plain CNN and the CNN with batch
normalisation + dropout say, with their probability for that answer. Plotly image grid (a still set of photos).
Our own design.  Run: python mistakes.py -> mistakes.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
D = np.load(HERE.parent / "data" / "mistakes.npz")
X, y, pp, pb = D["images"], D["labels"], D["p_plain"], D["p_bn"]
assert X.shape == (12, 80, 80, 3) and all((pp > 0.5) != (y == 1))        # every one is a mistake of the plain CNN
name = lambda dog: "dog" if dog else "cat"


def says(p):
    return f"{name(p > 0.5)} {100 * max(p, 1 - p):.0f}%"


titles = [f"true: <b>{name(v)}</b><br>plain: {says(a)}<br>BN + dropout: {says(b)}" for v, a, b in zip(y, pp, pb)]
fig = make_subplots(rows=2, cols=6, horizontal_spacing=0.015, vertical_spacing=0.22, subplot_titles=titles)
for k in range(12):
    fig.add_trace(go.Image(z=X[k]), row=k // 6 + 1, col=k % 6 + 1)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_annotations(font_size=17)
fig.update_layout(template="simple_white", width=1300, height=640, font=dict(family="Latin Modern Roman", size=17),
                  margin=dict(l=10, r=10, t=90, b=10))
fig.write_image(HERE / "mistakes.png", scale=2)
