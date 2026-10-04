"""Bagging grows one tree at a time on the moons data (decision trees, 50 rows each drawn with replacement, as in
section 2.1). Left: the newest tree alone, with the rows it drew. Right: the vote of all trees so far.
Run: python bagging_grows.py  -> bagging_grows.gif, bagging_grows_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, REGION, X_test, X_train, fit, xs, y_test, y_train, ys  # noqa: E402  same data as the app

(single, single_acc), (bag, bag_acc) = fit("decision tree", n_estimators=100, max_samples=50)
XX, YY = np.meshgrid(xs, ys)
grid = np.c_[XX.ravel(), YY.ravel()]


def blue_share(k, P):
    """Share of the first k trees that vote class 1 (blue) at the points P."""
    return np.mean([t.predict(P[:, f]) for t, f in zip(bag.estimators_[:k], bag.estimators_features_[:k])], axis=0)


acc = {k: np.mean((blue_share(k, X_test) > 0.5) == y_test) for k in range(1, 101)}
assert abs(acc[100] - bag_acc) < 1e-9, (acc[100], bag_acc)   # our vote is the BaggingClassifier's prediction
print("single tree", round(single_acc, 3), "| accuracy after k trees:", {k: round(acc[k], 3) for k in (1, 5, 10, 25, 100)})
KS = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 75, 100]
SHARE = [[0, "#F58518"], [0.5, "#FFFFFF"], [1, "#4C78A8"]]


def frame(k):
    t, f = bag.estimators_[k - 1], bag.estimators_features_[k - 1]
    copies = np.bincount(bag.estimators_samples_[k - 1], minlength=len(y_train))
    fig = make_subplots(1, 2, horizontal_spacing=0.04, subplot_titles=[
        f"tree {k} alone: its 50 drawn points", f"vote of {k} tree{'s' * (k > 1)}: test accuracy {acc[k]:.3f}"])
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=t.predict(grid[:, f]).reshape(XX.shape), zmin=0, zmax=1,
                             colorscale=REGION, showscale=False), 1, 1)
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=blue_share(k, grid).reshape(XX.shape), zmin=0, zmax=1, colorscale=SHARE,
                             opacity=0.55, colorbar=dict(title="share of trees<br>voting blue", len=0.8, thickness=18)),
                  1, 2)
    for cls in (0, 1):
        m = y_train == cls
        drawn = m & (copies > 0)
        fig.add_trace(go.Scatter(x=X_train[m & ~drawn, 0], y=X_train[m & ~drawn, 1], mode="markers", showlegend=False,
                                 marker=dict(color=COLOURS[cls], size=4, opacity=0.25)), 1, 1)
        fig.add_trace(go.Scatter(x=X_train[drawn, 0], y=X_train[drawn, 1], mode="markers", showlegend=False,
                                 marker=dict(color=COLOURS[cls], size=8 + 4 * copies[drawn],
                                             line=dict(color="black", width=1.2))), 1, 1)
        fig.add_trace(go.Scatter(x=X_train[m, 0], y=X_train[m, 1], mode="markers", showlegend=False,
                                 marker=dict(color=COLOURS[cls], size=5, line=dict(color="white", width=0.5))), 1, 2)
    fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False, ticks="")
    fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False, ticks="")
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1300, height=640, font=dict(family="Latin Modern Roman", size=20),
                      margin=dict(l=10, r=10, t=60, b=10))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".bagging_grows_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(KS):
        frame(k).write_image(tmp / f"{i:03d}.png")
    for i in range(len(KS), len(KS) + 6):                   # hold the last frame
        shutil.copy(tmp / f"{len(KS) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bagging_grows.gif")], check=True)
    keys = [Image.open(tmp / f"{KS.index(k):03d}.png").convert("RGB") for k in (1, 5, 20, 100)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "bagging_grows_frames.png")
    shutil.rmtree(tmp)
