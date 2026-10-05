"""A prediction path as a shrinking region. The fully grown iris tree of Figure 4 (DecisionTreeClassifier,
random_state=0, all 150 flowers) routes the flower (5.9, 3.2, 4.8, 1.8) through nodes #0, #2, #12, #13 to leaf #15.
Each question cuts the petal-length / petal-width plane; the last one is on sepal width, so it shows as a count of
the training flowers still on the path, not as a cut. Plotly frames -> ffmpeg GIF, plus a grid for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
COL = ["#4C78A8", "#F58518", "#54A24B"]
NAMES = ["setosa", "versicolor", "virginica"]
iris = load_iris()
X, y = iris.data, iris.target
full = DecisionTreeClassifier(random_state=0).fit(X, y)
flower = np.array([5.9, 3.2, 4.8, 1.8])
path = full.decision_path(flower[None]).indices.tolist()
assert path == [0, 2, 12, 13, 15], path
t = full.tree_
STEPS = []                                              # (node, feature, threshold, went_left)
for a, b in zip(path[:-1], path[1:]):
    STEPS.append((a, t.feature[a], t.threshold[a], b == t.children_left[a]))
assert [(s[1], round(s[2], 2), s[3]) for s in STEPS] == [(3, 0.8, False), (3, 1.75, False), (2, 4.85, True),
                                                         (1, 3.1, False)]
FN = ["sepal length", "sepal width", "petal length", "petal width"]


def region(k):
    """Bounds on petal length (x) and petal width (y) after k questions, and the training flowers still on the path."""
    xl, xh, yl, yh = 0.5, 7.2, 0.0, 2.7
    keep = np.ones(len(y), bool)
    for node, f, thr, left in STEPS[:k]:
        keep &= (X[:, f] <= thr) if left else (X[:, f] > thr)
        if f == 2:
            xl, xh = (xl, thr) if left else (thr, xh)
        if f == 3:
            yl, yh = (yl, thr) if left else (thr, yh)
    return xl, xh, yl, yh, keep


assert [int(region(k)[4].sum()) for k in range(5)] == [150, 100, 46, 3, 1]


def frame(k):
    xl, xh, yl, yh, keep = region(k)
    fig = go.Figure()
    fig.add_shape(type="rect", x0=xl, x1=xh, y0=yl, y1=yh, fillcolor="#E45756", opacity=0.10, line_width=0)
    fig.add_shape(type="rect", x0=xl, x1=xh, y0=yl, y1=yh, fillcolor="rgba(0,0,0,0)", line=dict(color="#E45756", width=3))
    for c in range(3):
        m = y == c
        fig.add_scatter(x=X[m & ~keep, 2], y=X[m & ~keep, 3], mode="markers", showlegend=False,
                        marker=dict(size=9, color=COL[c], opacity=0.15))
        fig.add_scatter(x=X[m & keep, 2], y=X[m & keep, 3], mode="markers", name=NAMES[c],
                        marker=dict(size=11, color=COL[c], line=dict(width=1, color="white")))
    fig.add_scatter(x=[flower[2]], y=[flower[3]], mode="markers", name="flower followed (training row 70)",
                    marker=dict(size=30, symbol="star-open", color="black", line=dict(width=2.5)))
    if k == 0:
        head = "Start at the root: all 150 training flowers"
    else:
        node, f, thr, left = STEPS[k - 1]
        q = f"#{node}: {FN[f]} {'≤' if left else '>'} {thr:.2f}"
        n = int(keep.sum())
        head = f"{q}  →  {n} training flower{'s' if n > 1 else ''} left"
        if f == 1:
            head += " (a cut on sepal width,<br>not drawn on this plane)"
    if k == len(STEPS):
        head += "<br>Leaf #15: <b>versicolor</b>"
    fig.update_layout(template="simple_white", width=1000, height=760, font=FONT,
                      title=dict(text=head, x=0.5, y=0.95, font=dict(size=22)),
                      xaxis=dict(title="petal length (cm)", range=[0.5, 7.2]),
                      yaxis=dict(title="petal width (cm)", range=[0, 2.7]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.14),
                      margin=dict(l=80, r=30, t=120, b=130))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".pr_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(len(STEPS) + 1):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [k for k in range(len(keys)) for _ in range(3)] + [len(keys) - 1] * 4
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "path_region.gif")], check=True)
    ims = [Image.open(keys[k]).convert("RGB") for k in (1, 3)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "path_region_frames.png")
    shutil.rmtree(tmp)
