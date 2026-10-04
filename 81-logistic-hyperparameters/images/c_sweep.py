"""Breast cancer data, standardised: the 30 logistic-regression coefficients as C falls from 100 to 0.001
(the penalty grows), for L2 (top) and L1 (bottom), with 5-fold CV accuracy in each title. Same models as c_path.py.
Run: python c_sweep.py  -> c_sweep.gif, c_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

warnings.simplefilter("ignore")
HERE = Path(__file__).parent
X, y = load_breast_cancer(return_X_y=True)
Cs = np.logspace(2, -3, 26)
model = lambda C, l1: make_pipeline(StandardScaler(), LogisticRegression(C=C, l1_ratio=l1, solver="saga", max_iter=50000, random_state=0))
coef, acc = {}, {}
for l1 in (0, 1):
    coef[l1] = np.array([model(C, l1).fit(X, y)[-1].coef_[0] for C in Cs])
    acc[l1] = [cross_val_score(model(C, l1), X, y, cv=5).mean() for C in Cs]
nz = {l1: (np.abs(coef[l1]) > 1e-8).sum(1) for l1 in (0, 1)}
print("L1 non-zero:", nz[1].tolist())
assert nz[0].min() == 30 and nz[1][-1] == 0                  # L2 keeps all 30; L1 ends with none
order = np.argsort(-(coef[1] != 0).sum(0), kind="stable")   # features that survive L1 longest first
LIM = 1.05 * max(np.abs(coef[0]).max(), np.abs(coef[1]).max())


def frame(k):
    C = Cs[k]
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.2, subplot_titles=(
        f"L2: {nz[0][k]} of 30 not zero, accuracy {acc[0][k]:.2f}",
        f"L1: {nz[1][k]} of 30 not zero, accuracy {acc[1][k]:.2f}"))
    for r, l1, col in ((1, 0, "#4C78A8"), (2, 1, "#E45756")):
        c = coef[l1][k][order]
        fig.add_trace(go.Bar(x=np.arange(30), y=c, marker_color=col, showlegend=False), r, 1)
        zero = np.abs(c) <= 1e-8
        fig.add_trace(go.Scatter(x=np.arange(30)[zero], y=np.zeros(zero.sum()), mode="markers", showlegend=False,
                                 marker=dict(symbol="circle-open", size=10, color="black", line_width=2)), r, 1)
    fig.update_xaxes(showticklabels=False, ticks="")
    fig.update_xaxes(title="the 30 measurements (open circle = exactly 0)", row=2, col=1)
    fig.update_yaxes(range=[-LIM, LIM], title="coefficient")
    fig.update_layout(template="simple_white", width=1000, height=760, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"C = {C:.3g}  (smaller C = stronger penalty)", x=0.5, y=0.98),
                      margin=dict(l=90, r=20, t=110, b=70), bargap=0.15)
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    last = len(Cs) - 1
    for k in range(last + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(last + 1, last + 8):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=8,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "c_sweep.gif")], check=True)
    picks = [0, int(np.argmin(np.abs(Cs - 1))), int(np.argmin(np.abs(Cs - 0.03))), last]
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in picks]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "c_sweep_frames.png")
    shutil.rmtree(tmp)
