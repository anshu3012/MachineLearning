"""Model-based learning as a process: logistic regression learns its decision boundary on the Note's placement data
by gradient descent (the same loss and L2 penalty as scikit-learn's LogisticRegression(C=1), on scaled features),
then drops the training data and classifies the new student (IQ 94.5, CGPA 8.3) with its 3 parameters alone.
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from placement_data import placement_data

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
BLUE, GREEN, RED, PURPLE = "#4C78A8", "#54A24B", "#E45756", "#B279A2"
X, y = placement_data()
query = np.array([94.5, 8.3])
sc = StandardScaler().fit(X)
Xs, qs = sc.transform(X), sc.transform(query[None])[0]

w, b, lr = np.array([1.0, -1.0]), 0.0, 0.05            # a bad starting boundary
hist = []
for it in range(4001):
    p = 1 / (1 + np.exp(-(Xs @ w + b)))
    hist.append((it, w.copy(), b, -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))))
    w, b = w - lr * (Xs.T @ (p - y) + w), b - lr * (p - y).sum()     # sklearn's loss with C = 1
ref = LogisticRegression().fit(Xs, y)
assert np.allclose(hist[-1][1], ref.coef_[0], atol=1e-3) and abs(hist[-1][2] - ref.intercept_[0]) < 1e-3
SHOW = [0, 1, 2, 4, 8, 16, 40, 4000]
IQ = np.linspace(73, 137, 60)


def boundary(w, b):
    iq_s = (IQ - sc.mean_[0]) / sc.scale_[0]
    return (-(w[0] * iq_s + b) / w[1]) * sc.scale_[1] + sc.mean_[1]


def frame(k, final=False):
    it, w, b, loss = hist[k]
    acc = ((Xs @ w + b > 0) == y).mean()
    fig = go.Figure()
    if not final:
        for lab, col, name, sym in [(1, GREEN, "placed", "circle"), (0, RED, "not placed", "x")]:
            m = y == lab
            fig.add_scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=name, marker=dict(color=col, size=11, symbol=sym))
    fig.add_scatter(x=IQ, y=boundary(w, b), mode="lines", name="decision boundary", line=dict(color=PURPLE, width=5))
    if final:
        side = "placed" if qs @ w + b > 0 else "not placed"
        prob = 1 / (1 + np.exp(-(qs @ w + b)))
        fig.add_scatter(x=[query[0]], y=[query[1]], mode="markers", name="new student",
                        marker=dict(color=BLUE, size=24, symbol="star", line=dict(color="black", width=1)))
        title = (f"Training data dropped. Kept: w₁ = {w[0]:.2f}, w₂ = {w[1]:.2f}, b = {b:.2f} (scaled features)"
                 f"<br>New student (IQ 94.5, CGPA 8.3): above the line, <b>{side}</b> (probability {prob:.2f})")
    else:
        title = f"Gradient descent step {it}: loss {loss:.3f}, {100 * acc:.0f}% of training students on the right side"
    fig.update_layout(template="simple_white", width=1000, height=720, font=FONT, title=dict(text=title, x=0.5, y=0.95,
                      font=dict(size=21)),
                      xaxis=dict(title="IQ", range=[73, 137]), yaxis=dict(title="CGPA", range=[4.8, 10.0]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15),
                      margin=dict(l=80, r=30, t=110, b=130))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".mt_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in SHOW:
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    keys.append(tmp / "final.png")
    frame(4000, final=True).write_image(keys[-1])
    seq = [0] * 3 + [i for i in range(1, len(keys) - 1) for _ in range(2)] + [len(SHOW) - 1] * 2 + [len(keys) - 1] * 6
    for j, i in enumerate(seq):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "model_training.gif")], check=True)
    ims = [Image.open(keys[i]).convert("RGB") for i in (0, len(keys) - 1)]
    W, H = ims[0].size
    sheet = Image.new("RGB", (2 * W + 16, H), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (W + 16), 0))
    sheet.save(HERE / "model_training_frames.png")
    shutil.rmtree(tmp)
    print("final", hist[-1][1].round(2), round(hist[-1][2], 2), "step0 acc", ((Xs @ hist[0][1] > 0) == y).mean())
