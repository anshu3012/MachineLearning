"""Bagging against boosting, one base model per frame, on the noisy concentric circles of the Notebook (500 points).
Top: bagging with fully grown trees; each tree's random sample (marker size = copies) ignores every earlier tree;
equal votes. Bottom: AdaBoost (SAMME, as scikit-learn) with stumps; each stump's weights (marker size) come from the
mistakes of the stumps before it; votes weighted by alpha.
Run: python parallel_vs_sequential.py  -> parallel_vs_sequential.gif, parallel_vs_sequential_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.datasets import make_circles
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
COLOURS = {0: "#F58518", 1: "#4C78A8"}
REGION = [[0, "#FDE5CC"], [1, "#DCE6F2"]]
SHARE = [[0, "#F58518"], [0.5, "#FFFFFF"], [1, "#4C78A8"]]
N = 100
X, y = make_circles(n_samples=500, factor=0.1, noise=0.35, random_state=42)
bag = BaggingClassifier(DecisionTreeClassifier(random_state=42), n_estimators=N, random_state=42).fit(X, y)
abc = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=N, random_state=42).fit(X, y)

# AdaBoost written out (SAMME), reusing scikit-learn's seeds so that tied splits break the same way
w, stumps, alphas, weights = np.full(len(y), 1 / len(y)), [], [], []
for est in abc.estimators_:
    weights.append(w.copy())                              # the weights this stump is trained with
    stump = DecisionTreeClassifier(max_depth=1, random_state=est.random_state).fit(X, y, sample_weight=w)
    wrong = stump.predict(X) != y
    err = w[wrong].sum()
    alpha = np.log((1 - err) / err)
    w = w * np.exp(alpha * wrong)
    w = w / w.sum()
    stumps.append(stump)
    alphas.append(alpha)
assert np.allclose(alphas, abc.estimator_weights_[:len(alphas)])
xs = ys = np.linspace(-1.8, 1.8, 200)
XX, YY = np.meshgrid(xs, ys)
grid = np.c_[XX.ravel(), YY.ravel()]
bag_votes = {"grid": np.array([t.predict(grid) for t in bag.estimators_]), "X": np.array([t.predict(X) for t in bag.estimators_])}
ada_votes = {"grid": np.array([a * (2 * s.predict(grid) - 1) for s, a in zip(stumps, alphas)]),
             "X": np.array([a * (2 * s.predict(X) - 1) for s, a in zip(stumps, alphas)])}
assert np.array_equal(ada_votes["X"].sum(0) > 0, abc.predict(X) == 1)          # our weighted vote = AdaBoostClassifier


def bag_share(k, where):
    return bag_votes[where][:k].mean(0)                     # share of trees voting blue


def ada_share(k, where):
    """Alpha-weighted vote, mapped to 0 (sure orange) .. 0.5 (tie) .. 1 (sure blue) by its largest size on the grid."""
    return 0.5 + 0.5 * ada_votes[where][:k].sum(0) / np.abs(ada_votes["grid"][:k].sum(0)).max()


acc = {k: (np.mean((bag_share(k, "X") > 0.5) == y), np.mean((ada_share(k, "X") > 0.5) == y)) for k in range(1, N + 1)}
print({k: tuple(round(a, 3) for a in acc[k]) for k in (1, 5, 10, 50, 100)})
KS = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 75, 100]


def frame(k):
    copies = np.bincount(bag.estimators_samples_[k - 1], minlength=len(y))
    wk = weights[k - 1] * len(y)                             # 1 = the starting weight
    titles = [f"bagging, tree {k}: its own random sample", f"bagging, equal vote of {k}: train accuracy {acc[k][0]:.2f}",
              f"boosting, stump {k}: weights from past mistakes", f"boosting, vote weighted by alpha: train accuracy {acc[k][1]:.2f}"]
    fig = make_subplots(2, 2, subplot_titles=titles, horizontal_spacing=0.03, vertical_spacing=0.08)
    panels = [(1, 1, bag.estimators_[k - 1].predict(grid), copies, 4 + 4 * copies),
              (2, 1, stumps[k - 1].predict(grid), wk, np.clip(3 + 8 * wk, 3, 40))]
    for r, c, Z, keep, size in panels:
        fig.add_trace(go.Heatmap(x=xs, y=ys, z=Z.reshape(XX.shape), zmin=0, zmax=1, colorscale=REGION, showscale=False), r, c)
        for cls in (0, 1):
            m = (y == cls) & (keep > 0)
            fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", marker=dict(
                color=COLOURS[cls], size=size[m], opacity=0.8, line=dict(color="white", width=0.5))), r, c)
    for r, share in ((1, bag_share), (2, ada_share)):
        fig.add_trace(go.Heatmap(x=xs, y=ys, z=share(k, "grid").reshape(XX.shape), zmin=0, zmax=1, colorscale=SHARE,
                                 opacity=0.6, showscale=False), r, 2)
        for cls in (0, 1):
            m = y == cls
            fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers",
                                     marker=dict(color=COLOURS[cls], size=4, line=dict(color="white", width=0.3))), r, 2)
    fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False, ticks="")
    fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False, ticks="")
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1200, height=1180, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=10, r=10, t=90, b=10),
                      title=dict(text=f"{k} base model{'s' * (k > 1)}", x=0.5, y=0.985, font_size=30))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".pvs_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(KS):
        frame(k).write_image(tmp / f"{i:03d}.png")
    for i in range(len(KS), len(KS) + 6):                   # hold the last frame
        shutil.copy(tmp / f"{len(KS) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "parallel_vs_sequential.gif")], check=True)
    keys = [Image.open(tmp / f"{KS.index(k):03d}.png").convert("RGB") for k in (1, 2, 10, 100)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "parallel_vs_sequential_frames.png")
    shutil.rmtree(tmp)
