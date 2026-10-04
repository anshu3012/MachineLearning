"""Every line gets a number. A line through the centre of 10 of the Note's 100 points (5 per class) turns through 360 degrees; for every
angle we compute two candidate losses: the count of misclassified points (0-1 loss) and the perceptron loss.
The count moves in jumps (flat in between); the perceptron loss changes smoothly.
Run: python rotating_line.py -> rotating_line.gif, rotating_line_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.datasets import make_classification

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X, Y01 = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                             n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=15)
Y = np.where(Y01 == 1, 1, -1)
keep = np.r_[np.where(Y == 1)[0][:5], np.where(Y == -1)[0][:5]]      # 5 points per class, so every jump of the count shows
X, Y = X[keep], Y[keep]
C = X.mean(0)
ANG = np.arange(0, 361, 3)


def line(deg):
    n = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg))])     # (w1, w2); b puts the line through the centre
    return n, -n @ C


def losses(deg):
    n, b = line(deg)
    s = Y * (X @ n + b)
    return int((s < 0).sum()), float(np.maximum(0, -s).mean())


CNT, PL = map(np.array, zip(*[losses(a) for a in ANG]))
fine = np.array([losses(a) for a in np.arange(0, 360, 0.25)])
assert (np.diff(fine[:, 0]) == 0).mean() > 0.95        # the count is flat for most small turns of the line
assert (np.diff(fine[:, 1]) != 0)[fine[:-1, 1] > 0].all()    # the perceptron loss changes with every small turn, unless it is 0
BEST = ANG[PL.argmin()]
xr, yr = (X[:, 0].min() - 0.5, X[:, 0].max() + 0.5), (X[:, 1].min() - 0.5, X[:, 1].max() + 0.5)


def frame(k):
    n, b = line(ANG[k])
    d = np.array([-n[1], n[0]])
    fig = make_subplots(2, 2, specs=[[{"rowspan": 2}, {}], [None, {}]], column_widths=[0.5, 0.5], horizontal_spacing=0.13,
                        vertical_spacing=0.2, subplot_titles=["the line", "misclassified points (0-1 loss)", "perceptron loss"])
    for cls, col in ((1, BLUE), (-1, ORANGE)):
        fig.add_trace(go.Scatter(x=X[Y == cls, 0], y=X[Y == cls, 1], mode="markers", marker=dict(color=col, size=14)), 1, 1)
    e = np.array([C - 20 * d, C + 20 * d])
    fig.add_trace(go.Scatter(x=e[:, 0], y=e[:, 1], mode="lines", line=dict(color="black", width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=ANG[:k + 1], y=CNT[:k + 1], mode="lines", line=dict(color=RED, width=4, shape="hv")), 1, 2)
    fig.add_trace(go.Scatter(x=ANG[:k + 1], y=PL[:k + 1], mode="lines", line=dict(color=GREEN, width=4)), 2, 2)
    fig.add_trace(go.Scatter(x=[ANG[k]], y=[CNT[k]], mode="markers", marker=dict(color=RED, size=14)), 1, 2)
    fig.add_trace(go.Scatter(x=[ANG[k]], y=[PL[k]], mode="markers", marker=dict(color=GREEN, size=14)), 2, 2)
    fig.update_xaxes(range=xr, title="x₁", row=1, col=1)
    fig.update_yaxes(range=yr, title="x₂", row=1, col=1)
    for r, top in ((1, 10.5), (2, PL.max() * 1.1)):
        fig.update_xaxes(range=[0, 360], dtick=90, row=r, col=2)
        fig.update_yaxes(range=[-0.04 * top, top], row=r, col=2)
    fig.update_xaxes(title="angle of the line (degrees)", row=2, col=2)
    fig.update_annotations(font=dict(size=24))
    fig.update_layout(template="simple_white", width=1100, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=20, t=110, b=70),
                      title=dict(text=f"angle {ANG[k]}°:  {CNT[k]} misclassified,  perceptron loss {PL[k]:.2f}", x=0.5, font=dict(size=28)))
    return fig


if __name__ == "__main__":
    print("best angle", BEST, "count there", CNT[PL.argmin()], "max loss", PL.max().round(2))
    tmp = HERE / ".rot_frames"
    tmp.mkdir(exist_ok=True)
    n = len(ANG)
    for k in range(n):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(n, n + 12):
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "10", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "rotating_line.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (n // 4, n - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "rotating_line_frames.png")
    shutil.rmtree(tmp)
