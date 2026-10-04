"""Logistic regression on polynomial features of the moons data, degree swept from 1 to 25 (same setup as degrees.py:
200 points, noise 0.25, C = 10,000). Left: decision regions for the seed-0 training set. Right: training and test
accuracy averaged over 20 training sets (seeds 0-19) on one fresh 5,000-point test set, growing one degree per frame.
Run: python degree_sweep.py  -> degree_sweep.gif, degree_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

warnings.simplefilter("ignore")
HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
X, y = make_moons(n_samples=200, noise=0.25, random_state=0)
X_test, y_test = make_moons(n_samples=5000, noise=0.25, random_state=999)
sets = [make_moons(n_samples=200, noise=0.25, random_state=s) for s in range(20)]
make = lambda d: make_pipeline(PolynomialFeatures(degree=d, include_bias=False), StandardScaler(),
                               LogisticRegression(C=1e4, max_iter=100000))
degrees = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 25]
train, test = [], []
for d in degrees:
    fits = [make(d).fit(*s) for s in sets]
    train.append(np.mean([m.score(*s) for m, s in zip(fits, sets)]))
    test.append(np.mean([m.score(X_test, y_test) for m in fits]))
    print(d, round(train[-1], 3), round(test[-1], 3))
best = degrees[int(np.argmax(test))]
assert best == 3 and train[-1] > train[2] and test[-1] < test[2]   # the Note's lesson: peak at 3, overfit after

xs, ys = np.linspace(-2, 3, 200), np.linspace(-1.6, 2.0, 150)
XX, YY = np.meshgrid(xs, ys)
grid = np.c_[XX.ravel(), YY.ravel()]
P = [make(d).fit(X, y).predict_proba(grid)[:, 1].reshape(XX.shape) for d in degrees]


def frame(k):
    d = degrees[k]
    fig = make_subplots(rows=1, cols=2, column_widths=[0.56, 0.44], horizontal_spacing=0.1,
                        subplot_titles=(f"degree {d}: {make(d)[0].fit(X).n_output_features_} features",
                                        "accuracy (20 training sets)"))
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=(P[k] > 0.5).astype(float), colorscale=[[0, "#DCE6F2"], [1, "#FDE5CC"]],
                             showscale=False), 1, 1)
    fig.add_trace(go.Contour(x=xs, y=ys, z=P[k], contours=dict(start=0.5, end=0.5, coloring="none"),
                             line=dict(color="black", width=3), showscale=False, showlegend=False), 1, 1)
    for cls, col in ((0, BLUE), (1, ORANGE)):
        fig.add_trace(go.Scatter(x=X[y == cls, 0], y=X[y == cls, 1], mode="markers", showlegend=False,
                                 marker=dict(color=col, size=7, line=dict(color="white", width=0.5))), 1, 1)
    for vals, name, col in ((train, "training", GREY), (test, "test", "#E45756")):
        fig.add_trace(go.Scatter(x=degrees[:k + 1], y=vals[:k + 1], mode="lines+markers", name=name,
                                 line=dict(color=col, width=4), marker=dict(size=10)), 1, 2)
    if degrees[k] >= best:
        fig.add_annotation(x=best, y=test[2], text="best: degree 3", showarrow=True, ay=-60, ax=40,
                           font=dict(color="#E45756"), row=1, col=2)
    fig.update_xaxes(range=[-2, 3], showticklabels=False, row=1, col=1)
    fig.update_yaxes(range=[-1.6, 2.0], showticklabels=False, row=1, col=1)
    fig.update_xaxes(title="degree", type="log", range=[-0.05, 1.45], tickvals=[1, 2, 3, 5, 10, 25], row=1, col=2)
    fig.update_yaxes(range=[0.84, 0.975], dtick=0.04, row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=20, r=20, t=70, b=70), legend=dict(x=0.99, xanchor="right", y=0.02))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    last = len(degrees) - 1
    for k in range(last + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(last + 1, last + 5):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=10,scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "degree_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 2, 7, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "degree_sweep_frames.png")
    shutil.rmtree(tmp)
