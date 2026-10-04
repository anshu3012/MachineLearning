"""Logistic regression by maximum likelihood on 8 Iris flowers (petal width; 4 versicolor = 0, 4 virginica = 1).
The straight line in log-odds space turns about the point where it crosses 0 (x0 = 1.627 cm, the MLE's crossing).
Top left: on the log-odds axis the flowers sit at -inf / +inf, so least-squares residuals are infinite; each flower
is projected onto the line. Top right: the same line as a probability squiggle; the bar at each flower is its
likelihood (p for virginica, 1 - p for versicolor). Bottom: the log-likelihood (sum of log bars) against the slope,
highest at the MLE slope 7.27 with log-likelihood -3.01.
Run: python logistic_rotate.py -> logistic_rotate.gif, logistic_rotate_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from scipy import optimize
from sklearn.datasets import load_iris

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Xall, yall = load_iris(return_X_y=True)
IDX = [57, 53, 51, 77, 119, 103, 110, 115]                     # versicolor 1.0, 1.3, 1.5, 1.7; virginica 1.5, 1.8, 2.0, 2.3
x = Xall[IDX, 3]
t = (yall[IDX] == 2).astype(float)
loglik = lambda b0, b1: np.sum(t * (b0 + b1 * x) - np.logaddexp(0, b0 + b1 * x))
res = optimize.minimize(lambda b: -loglik(*b), [0, 0])
B0, B1 = res.x
X0 = -B0 / B1
assert abs(B1 - 7.27) < 0.01 and abs(-res.fun + 3.01) < 0.01 and abs(X0 - 1.627) < 0.001
ll_s = lambda s: loglik(-s * X0, s)
S = np.round(np.arange(0, 16.01, 0.5), 2)
s_fine = np.linspace(0, 16, 400)
ll_fine = np.array([ll_s(s) for s in s_fine])
assert abs(s_fine[ll_fine.argmax()] - B1) < 0.05
jit = np.array([0, 0, -0.015, 0, 0.015, 0, 0, 0])               # the two 1.5 cm flowers side by side
xs = np.linspace(0.8, 2.5, 300)
col = [GREEN if v else BLUE for v in t]


def frame(s):
    fig = make_subplots(rows=2, cols=2, vertical_spacing=0.2, horizontal_spacing=0.12, row_heights=[0.55, 0.45],
                        specs=[[{}, {}], [{"colspan": 2}, None]],
                        subplot_titles=("log-odds: flowers at ±∞", "probability: bar = likelihood",
                                        "log-likelihood against the slope of the line"))
    z = s * (x - X0)
    fig.add_trace(go.Scatter(x=xs, y=s * (xs - X0), mode="lines", line=dict(color=GREY, width=4)), 1, 1)
    for xi, zi, ti, c in zip(x + jit, z, t, col):
        edge = 5.4 if ti else -5.4
        fig.add_trace(go.Scatter(x=[xi, xi], y=[np.clip(zi, -5.4, 5.4), edge], mode="lines",
                                 line=dict(color=c, width=2, dash="dot")), 1, 1)
        fig.add_trace(go.Scatter(x=[xi], y=[edge], mode="markers",
                                 marker=dict(size=15, color=c, symbol="triangle-up" if ti else "triangle-down")), 1, 1)
        if abs(zi) < 5.4:
            fig.add_trace(go.Scatter(x=[xi], y=[zi], mode="markers", marker=dict(size=11, color=c, line=dict(width=1))), 1, 1)
    p = 1 / (1 + np.exp(-z))
    fig.add_trace(go.Scatter(x=xs, y=1 / (1 + np.exp(-s * (xs - X0))), mode="lines", line=dict(color=GREY, width=4)), 1, 2)
    for xi, pi, ti, c in zip(x + jit, p, t, col):
        lo, hi = (0, pi) if ti else (pi, 1)
        fig.add_trace(go.Scatter(x=[xi, xi], y=[lo, hi], mode="lines", line=dict(color=c, width=7)), 1, 2)
        fig.add_trace(go.Scatter(x=[xi], y=[ti], mode="markers", marker=dict(size=12, color=c)), 1, 2)
    seen = s_fine <= s + 1e-9
    fig.add_trace(go.Scatter(x=s_fine[seen], y=ll_fine[seen], mode="lines", line=dict(color=ORANGE, width=4)), 2, 1)
    fig.add_trace(go.Scatter(x=[s], y=[ll_s(s)], mode="markers", marker=dict(size=14, color=ORANGE)), 2, 1)
    fig.update_xaxes(range=[0.8, 2.5], title_text="petal width (cm)", row=1, col=1)
    fig.update_xaxes(range=[0.8, 2.5], title_text="petal width (cm)", row=1, col=2)
    fig.update_yaxes(range=[-6, 6], title_text="log-odds of virginica", row=1, col=1)
    fig.update_yaxes(range=[-0.05, 1.05], title_text="P(virginica)", row=1, col=2)
    fig.update_xaxes(range=[0, 16], title_text="slope of the log-odds line", row=2, col=1)
    fig.update_yaxes(range=[-8, -2], title_text="log-likelihood", row=2, col=1)
    fig.update_layout(template="simple_white", width=1100, height=860, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"slope {s:.1f}    log-likelihood {ll_s(s):.2f}", x=0.5, y=0.985),
                      margin=dict(l=80, r=30, t=110, b=60))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".logit_frames"
    tmp.mkdir(exist_ok=True)
    seq = list(S) + [round(B1, 2)] * 8                          # end by settling on the MLE line
    for k, s in enumerate(seq):
        frame(s).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "logistic_rotate.gif")], check=True)
    keys = [Image.open(tmp / f"{seq.index(v):03d}.png").convert("RGB") for v in (0.0, 3.0, round(B1, 2), 16.0)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "logistic_rotate_frames.png")
    shutil.rmtree(tmp)
