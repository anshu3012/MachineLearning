"""Social Network Ads data (age, salary; app.load split): decision surface as max_depth grows 1, 2, ..., 13
(13 = fully grown here). Right: training accuracy and 5-fold cross-validation accuracy on the training set,
the measure the Note uses to choose the depth. Same trees as figs.py (random_state 42).
Run: python depth_sweep.py  -> depth_sweep.gif, depth_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import fit, grid, traces  # noqa: E402

full = fit("ads")[0].get_depth()
depths = list(range(1, full + 1))
trees = [fit("ads", max_depth=d) for d in depths]
X_train, y_train = trees[0][1], trees[0][3]
train = [t[0].score(X_train, y_train) for t in trees]
cv = [cross_val_score(DecisionTreeClassifier(random_state=42, max_depth=d), X_train, y_train, cv=5).mean()
      for d in depths]
best = depths[int(np.argmax(cv))]
assert best == 2 and train[-1] == 1.0 and cv[-1] < cv[1]       # the Note: CV picks depth 2; full tree overfits
print("cv", np.round(cv, 3))
xs, ys = grid(X_train)


def frame(k):
    tree, *_, axes, classes = trees[k]
    d = depths[k]
    name = f"max_depth = {d}" + (" (fully grown)" if d == full else "")
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.12,
                        subplot_titles=(f"{name}: {tree.get_n_leaves()} leaves", "accuracy"))
    for t in traces(tree, X_train, y_train, classes, show_legend=False):
        fig.add_trace(t, 1, 1)
    for vals, label, col in ((train, "training", "#6B6B6B"), (cv, "cross-validation", "#E45756")):
        fig.add_trace(go.Scatter(x=depths[:k + 1], y=vals[:k + 1], mode="lines+markers", name=label,
                                 line=dict(color=col, width=4), marker=dict(size=10)), 1, 2)
    if d >= best:
        fig.add_annotation(x=best, y=cv[best - 1], text="best: depth 2", ax=40, ay=0, xanchor="left", font=dict(color="#E45756"),
                           row=1, col=2)
    fig.update_xaxes(range=[xs[0], xs[-1]], title=axes[0], row=1, col=1)
    fig.update_yaxes(range=[ys[0], ys[-1]], title=axes[1], showticklabels=False, row=1, col=1)
    fig.update_xaxes(range=[0.5, full + 0.5], dtick=2, title="max_depth", row=1, col=2)
    fig.update_yaxes(range=[0.78, 1.01], row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=60, r=20, t=70, b=80), legend=dict(x=0.99, xanchor="right", y=0.42, font_size=20))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    last = len(depths) - 1
    for k in range(last + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(last + 1, last + 5):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=9,scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "depth_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 1, 5, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "depth_sweep_frames.png")
    shutil.rmtree(tmp)
