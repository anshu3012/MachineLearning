"""Soft-margin SVM on the Note's 18 points as C falls from 1000 to 0.03: the margin widens, more points need slack
(orange sticks, drawn from each point to its own hyperplane), mistakes are ringed. Same data and SVC as figs.py.
Run: python c_sweep.py  -> c_sweep.gif, c_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.svm import SVC

HERE = Path(__file__).parent
GREEN, RED, ORANGE = "#54A24B", "#E45756", "#F58518"
G = np.array([(2, 6), (3.5, 7.5), (4.5, 6), (6, 7.5), (2.5, 8.5), (5, 9), (7, 9), (7.5, 6.8), (6, 4.3)])
R = np.array([(1, 1.5), (2.5, 3), (3.5, 1), (5, 2.5), (6.5, 1.5), (7, 3.5), (1.5, 3.8), (4, 3.5), (2.8, 5.2)])
X, y = np.r_[G, R], np.r_[np.ones(len(G)), -np.ones(len(R))]
xs = np.array([0, 8.5])
Cs = np.logspace(3, np.log10(0.03), 25)
for key in (1.0, 0.05):                                       # land exactly on the C values of the text
    Cs[np.argmin(np.abs(np.log(Cs / key)))] = key
Cs = [float(c) for c in Cs]
fits = [SVC(kernel="linear", C=C).fit(X, y) for C in Cs]
W = [(m.coef_[0], m.intercept_[0]) for m in fits]
margin = [2 / np.linalg.norm(w) for w, _ in W]
assert margin[-1] > margin[0] * 10                           # small C: much wider margin


def frame(k):
    (w, b), C = W[k], Cs[k]
    s = np.maximum(0, 1 - y * (X @ w + b))
    s[s < 1e-3] = 0
    wrong = np.sign(X @ w + b) != y
    n = np.linalg.norm(w)
    fig = go.Figure()
    for rhs, colour, dash in ((0, "black", "solid"), (1, GREEN, "dash"), (-1, RED, "dash")):
        fig.add_trace(go.Scatter(x=xs, y=(rhs - b - w[0] * xs) / w[1], mode="lines",
                                 line=dict(color=colour, width=4 if rhs == 0 else 3, dash=dash)))
    for i in np.flatnonzero(s):
        end = X[i] + y[i] * s[i] / n * w / n                    # walk to the point's own hyperplane
        fig.add_trace(go.Scatter(x=[X[i, 0], end[0]], y=[X[i, 1], end[1]], mode="lines",
                                 line=dict(color=ORANGE, width=5)))
    for P, c in ((G, GREEN), (R, RED)):
        fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers",
                                 marker=dict(color=c, size=14, line=dict(color="black", width=1))))
    fig.add_trace(go.Scatter(x=X[wrong, 0], y=X[wrong, 1], mode="markers",
                             marker=dict(size=30, color="rgba(0,0,0,0)", line=dict(color="black", width=3))))
    fig.update_layout(template="simple_white", width=720, height=820, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"C = {C:g}<br>margin {margin[k]:.2f}, {int(wrong.sum())} mistake{'' if wrong.sum() == 1 else 's'}, "
                                      f"Σξ = {s.sum():.2f}", x=0.5, y=0.96),
                      margin=dict(l=70, r=20, t=130, b=70),
                      xaxis=dict(title="x₁", range=[0, 8.5]), yaxis=dict(title="x₂", range=[0, 10], scaleanchor="x"))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    last = len(Cs) - 1
    seq = [k for k in range(last + 1) for _ in range(4 if Cs[k] in (1000.0, 1.0, 0.05) else 1)] + [last] * 8
    for k in range(last + 1):
        frame(k).write_image(tmp / f"f{k:03d}.png")
    for j, k in enumerate(seq):                                # pause on the three C values of the text
        shutil.copy(tmp / f"f{k:03d}.png", tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=8,scale=560:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "c_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"f{Cs.index(c):03d}.png").convert("RGB") for c in (1000.0, 1.0, 0.05)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (3 * w + 32, h), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "c_sweep_frames.png")
    shutil.rmtree(tmp)
