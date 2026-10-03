"""MNIST: one digit image next to the random forest's feature importance of every pixel, as 28 x 28 heatmaps (Plotly).
The forest is trained once on 42,000 images (about a minute); its 784 importances are cached in ../data/."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
CACHE = HERE.parent / "data" / "mnist_importances.csv"
EXAMPLE = HERE.parent / "data" / "mnist_example.csv"
if not CACHE.exists():
    from sklearn.datasets import fetch_openml
    from sklearn.ensemble import RandomForestClassifier
    X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
    idx = np.random.default_rng(0).choice(len(X), 42000, replace=False)   # same size as the Kaggle train.csv
    X, y = X[idx], y[idx]
    rf = RandomForestClassifier(random_state=42, n_jobs=-1).fit(X, y)
    pd.DataFrame({"importance": rf.feature_importances_}).to_csv(CACHE, index=False)
    zero = X[np.where(y == "0")[0][0]]
    pd.DataFrame({"pixel": zero.astype(int)}).to_csv(EXAMPLE, index=False)
imp = pd.read_csv(CACHE)["importance"].values.reshape(28, 28)
digit = pd.read_csv(EXAMPLE)["pixel"].values.reshape(28, 28)
print("max importance", imp.max().round(4), "pixels with zero importance", int((imp == 0).sum()))

fig = make_subplots(1, 2, subplot_titles=["(a) one image: a handwritten 0", "(b) feature importance of each pixel"],
                    horizontal_spacing=0.12)
fig.add_trace(go.Heatmap(z=digit, colorscale="Greys", showscale=False), 1, 1)
fig.add_trace(go.Heatmap(z=imp, colorscale="Blues", colorbar=dict(title="importance", x=1.02, len=0.9)), 1, 2)
for c in (1, 2):
    fig.update_xaxes(range=[-0.5, 27.5], showticklabels=False, ticks="", showline=True, mirror=True, linecolor="#6B6B6B", constrain="domain", row=1, col=c)
    fig.update_yaxes(range=[27.5, -0.5], showticklabels=False, ticks="", showline=True, mirror=True, linecolor="#6B6B6B",
                     scaleanchor=f"x{'' if c == 1 else 2}", row=1, col=c)
fig.update_annotations(font_size=22)
fig.update_layout(template="simple_white", width=1200, height=600, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=20, r=40, t=60, b=20))
fig.write_image(HERE / "mnist_importance.png", scale=2)
fig.write_image(HERE / "mnist_importance.pdf")
