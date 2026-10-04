"""Variance made visible: draw the noisy concentric circles of section 3 eight times (new random_state each time,
same recipe), train one fully grown tree and a random forest of 500 trees on each draw, and compare how much each
model's decision surface moves. Last frame: the share of the eight surfaces that say blue at every point.
Run: python resample_variance.py  -> resample_variance.gif, resample_variance_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.datasets import make_circles
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
COLOURS = {0: "#F58518", 1: "#4C78A8"}
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]
SHARE = [[0, "#F58518"], [0.5, "#FFFFFF"], [1, "#4C78A8"]]
DRAWS = 8
xs = ys = np.linspace(-1.8, 1.8, 240)
XX, YY = np.meshgrid(xs, ys)
grid = np.c_[XX.ravel(), YY.ravel()]

runs = []
SEEDS = [42, 0, 1, 2, 3, 4, 5, 6]                           # draw 1 is the data of Figure 1
for seed in SEEDS[:DRAWS]:
    X, y = make_circles(n_samples=500, factor=0.1, noise=0.35, random_state=seed)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    tree = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
    rf = RandomForestClassifier(n_estimators=500, random_state=42, n_jobs=-1).fit(X_train, y_train)
    runs.append(dict(X=X_train, y=y_train, tree=tree.predict(grid), rf=rf.predict(grid),
                     acc=(tree.score(X_test, y_test), rf.score(X_test, y_test))))
share = {m: np.mean([r[m] for r in runs], axis=0) for m in ("tree", "rf")}
# variance of the surface: how often two draws disagree at a grid point, averaged over all pairs of draws
flip = {m: np.mean([np.mean(runs[a][m] != runs[b][m]) for a in range(DRAWS) for b in range(a)]) for m in ("tree", "rf")}
acc = np.array([r["acc"] for r in runs])
assert flip["rf"] < flip["tree"] and acc[:, 1].mean() > acc[:, 0].mean()
print("pairwise disagreement: tree", round(flip["tree"], 3), "forest", round(flip["rf"], 3),
      "| mean test accuracy: tree", round(acc[:, 0].mean(), 3), "forest", round(acc[:, 1].mean(), 3))


def frame(d):
    last = d == DRAWS
    if last:
        titles = [f"one tree, all {DRAWS} draws: two draws<br>disagree on {flip['tree']:.0%} of the plane",
                  f"forest, all {DRAWS} draws: two draws<br>disagree on {flip['rf']:.0%} of the plane"]
    else:
        r = runs[d]
        titles = [f"draw {d + 1}: one fully grown tree<br>test accuracy {r['acc'][0]:.2f}",
                  f"draw {d + 1}: random forest, 500 trees<br>test accuracy {r['acc'][1]:.2f}"]
    fig = make_subplots(1, 2, horizontal_spacing=0.04, subplot_titles=titles)
    for i, m in enumerate(("tree", "rf"), start=1):
        if last:
            fig.add_trace(go.Heatmap(x=xs, y=ys, z=share[m].reshape(XX.shape), zmin=0, zmax=1, colorscale=SHARE,
                                     opacity=0.7, showscale=(i == 2), colorbar=dict(
                                         title=dict(text="share of draws saying blue", side="top"),
                                         orientation="h", y=-0.04, yanchor="top", thickness=16, len=0.6)), 1, i)
            continue
        fig.add_trace(go.Heatmap(x=xs, y=ys, z=runs[d][m].reshape(XX.shape), zmin=0, zmax=1, colorscale=REGION,
                                 showscale=False), 1, i)
        for cls in (0, 1):
            k = runs[d]["y"] == cls
            fig.add_trace(go.Scatter(x=runs[d]["X"][k, 0], y=runs[d]["X"][k, 1], mode="markers", showlegend=False,
                                     marker=dict(color=COLOURS[cls], size=6, line=dict(color="white", width=0.5))), 1, i)
    fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False, ticks="")
    fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False, ticks="", scaleanchor=None)
    fig.update_annotations(font_size=25)
    fig.update_layout(template="simple_white", width=1300, height=720, font=dict(family="Latin Modern Roman", size=20),
                      margin=dict(l=10, r=10, t=95, b=110))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".resample_frames"
    tmp.mkdir(exist_ok=True)
    for d in range(DRAWS + 1):
        frame(d).write_image(tmp / f"{d:03d}.png")
    for i in range(DRAWS + 1, DRAWS + 6):                    # hold the last frame
        shutil.copy(tmp / f"{DRAWS:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "resample_variance.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 1, 2, DRAWS)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "resample_variance_frames.png")
    shutil.rmtree(tmp)
