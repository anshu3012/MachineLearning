"""A random forest grows tree by tree on the student placement data (CGPA, IQ; Note 13's 100 students).
Left: the newest tree's bootstrap sample (dot size = times drawn, grey = left out) and that tree's regions.
Right: the forest's vote map, the share of trees voting "placed", after t trees.
Each tree is what RandomForestClassifier builds: a bootstrap sample, a fully grown tree, max_features="sqrt".
Run: python forest_grows.py  -> forest_grows.gif, forest_grows_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#BBBBBB"
df = pd.read_csv(HERE.parent / "data" / "placement.csv")
X, y = df[["cgpa", "iq"]].to_numpy(), df["placement"].to_numpy()
n = len(y)
rng = np.random.default_rng(0)
xs = np.linspace(X[:, 0].min() - 0.3, X[:, 0].max() + 0.3, 220)
ys = np.linspace(X[:, 1].min() - 10, X[:, 1].max() + 10, 220)
XX, YY = np.meshgrid(xs, ys)
G = np.c_[XX.ravel(), YY.ravel()]

T = 100
counts, maps = [], []
for t in range(T):
    idx = rng.integers(0, n, n)                          # bootstrap: n rows with replacement
    tree = DecisionTreeClassifier(max_features="sqrt", random_state=t).fit(X[idx], y[idx])
    counts.append(np.bincount(idx, minlength=n))
    maps.append(tree.predict(G).reshape(XX.shape))
cum = np.cumsum(maps, axis=0) / np.arange(1, T + 1)[:, None, None]   # share of trees voting "placed"
SHOW = [1, 2, 3, 4, 5, 6, 8, 12, 20, 40, 100]
# the vote map settles: the change per added tree shrinks as the forest grows
change = [np.abs(cum[t] - cum[t - 1]).mean() for t in range(1, T)]
assert np.mean(change[:5]) > 5 * np.mean(change[-20:])
print("in-bag share of tree 1:", (counts[0] > 0).mean(), " mean |change| first 5 vs last 20:",
      round(np.mean(change[:5]), 3), round(np.mean(change[-20:]), 4))


def frame(t):
    c = counts[t - 1]
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                        subplot_titles=(f"tree {t}: its own sample", f"forest of {t} tree{'s' if t > 1 else ''}"))
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=maps[t - 1], zmin=0, zmax=1, showscale=False, hoverinfo="skip",
                             colorscale=[[0, "#DCE6F2"], [1, "#FDE5CC"]]), 1, 1)
    out = c == 0
    fig.add_trace(go.Scatter(x=X[out, 0], y=X[out, 1], mode="markers", name="left out of this tree",
                             marker=dict(color=GREY, size=8, symbol="x")), 1, 1)
    for cls, col, name in ((0, BLUE, "not placed"), (1, ORANGE, "placed")):
        m = (y == cls) & ~out
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=name,
                                 marker=dict(color=col, size=6 + 5 * c[m], line=dict(color="white", width=1))), 1, 1)
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=cum[t - 1], zmin=0, zmax=1, hoverinfo="skip",
                             colorscale=[[0, BLUE], [0.5, "white"], [1, ORANGE]],
                             colorbar=dict(title="share voting<br>placed", len=0.8, thickness=18)), 1, 2)
    for cls, col in ((0, BLUE), (1, ORANGE)):
        m = y == cls
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", showlegend=False,
                                 marker=dict(color=col, size=7, line=dict(color="black", width=1))), 1, 2)
    fig.update_xaxes(range=[xs[0], xs[-1]], title="CGPA")
    fig.update_yaxes(range=[ys[0], ys[-1]])
    fig.update_yaxes(title="IQ", col=1)
    fig.update_annotations(font_size=26)
    fig.update_layout(template="simple_white", width=1200, height=640, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=80, r=20, t=120, b=70), legend=dict(orientation="h", x=0, y=1.13, yanchor="bottom"))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".forest_frames"
    tmp.mkdir(exist_ok=True)
    k = 0
    for i, t in enumerate(SHOW):
        frame(t).write_image(tmp / f"{k:03d}.png")
        for _ in range(9 if i == len(SHOW) - 1 else 2):    # each tree held 3 frames, the last one longer
            shutil.copy(tmp / f"{k:03d}.png", tmp / f"{k + 1:03d}.png")
            k += 1
        k += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=780:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "forest_grows.gif")], check=True)
    keys = [Image.open(tmp / f"{3 * SHOW.index(t):03d}.png").convert("RGB") for t in (1, 3, 12, 100)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "forest_grows_frames.png")
    shutil.rmtree(tmp)
