"""RBF SVM (C = 1) on the playground's moons data (200 points, noise 0.2) as gamma grows from 0.01 to 1000.
Left: decision regions and support vectors (app.traces). Right: training accuracy and accuracy on a fresh
5,000-point test set from the same generator (seed 99), growing one gamma per frame.
Run: python gamma_sweep.py  -> gamma_sweep.gif, gamma_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.datasets import make_moons
from sklearn.svm import SVC

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import make_data, traces  # noqa: E402

X, y = make_data("moons")
Xt, yt = make_moons(n_samples=5000, noise=0.2, random_state=99)
gammas = np.logspace(-2, 3, 21)
models = [SVC(kernel="rbf", C=1, gamma=g).fit(X, y) for g in gammas]
train = [m.score(X, y) for m in models]
test = [m.score(Xt, yt) for m in models]
best = int(np.argmax(test))
assert 0 < best < len(gammas) - 1 and train[-1] == 1.0 and test[-1] < test[best] - 0.2   # under, best, over
print("best gamma", gammas[best], test[best])


fmt = lambda v: f"{v:,.0f}" if v >= 10 else f"{v:.2g}"


def frame(k):
    m = models[k]
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                        subplot_titles=(f"gamma = {fmt(gammas[k])}: {len(m.support_)} support vectors", "accuracy"))
    for t in traces(m, X, y, showlegend=False):
        fig.add_trace(t, 1, 1)
    for vals, name, col in ((train, "training", "#6B6B6B"), (test, "fresh test set", "#E45756")):
        fig.add_trace(go.Scatter(x=gammas[:k + 1], y=vals[:k + 1], mode="lines+markers", name=name,
                                 line=dict(color=col, width=4), marker=dict(size=9)), 1, 2)
    fig.update_xaxes(showticklabels=False, row=1, col=1)
    fig.update_yaxes(showticklabels=False, scaleanchor="x", row=1, col=1)
    fig.update_xaxes(type="log", range=[-2.2, 3.2], dtick=1, exponentformat="power", title="gamma", row=1, col=2)
    fig.update_yaxes(range=[0.6, 1.02], row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=20, r=20, t=70, b=70), legend=dict(x=0.6, y=0.02, font_size=20))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    last = len(gammas) - 1
    for k in range(last + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(last + 1, last + 7):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=9,scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "gamma_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 8, best, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "gamma_sweep_frames.png")
    shutil.rmtree(tmp)
