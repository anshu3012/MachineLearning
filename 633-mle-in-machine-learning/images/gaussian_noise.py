"""Gaussian noise + maximum likelihood = least squares. Four points, the line y = w x with the slope w sweeping
from 1.4 to 2.6. Top: a normal bell (sigma = 1) around the line at each x; the likelihood of a point is the bell's
height at its y. Bottom: the negative log-likelihood and the mean squared error against w; both bottom out at
w = 2.01. Run: python gaussian_noise.py -> gaussian_noise.gif, gaussian_noise_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X = np.array([1, 2, 3, 4.0])
Y = np.array([1.8, 4.3, 5.7, 8.2])
WS = np.round(np.arange(1.4, 2.601, 0.05), 2)
w_fine = np.linspace(1.4, 2.6, 300)
nll = lambda w: -stats.norm(w * X, 1).logpdf(Y).sum()
mse = lambda w: np.mean((Y - w * X) ** 2)
W_HAT = X @ Y / (X @ X)
assert abs(w_fine[np.argmin([nll(w) for w in w_fine])] - W_HAT) < 0.01
assert abs(w_fine[np.argmin([mse(w) for w in w_fine])] - W_HAT) < 0.01


def frame(w):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.15, row_heights=[0.58, 0.42],
                        specs=[[{}], [{"secondary_y": True}]],
                        subplot_titles=("the line y = w x with a normal bell (σ = 1) around it at each x",
                                        "negative log-likelihood (green) and MSE (orange)"))
    xs = np.linspace(0, 5, 50)
    fig.add_trace(go.Scatter(x=xs, y=w * xs, mode="lines", line=dict(color=BLUE, width=4), showlegend=False), 1, 1)
    t = np.linspace(-3, 3, 80)
    for xi, yi in zip(X, Y):
        dens = stats.norm.pdf(t)                              # bell drawn sideways, peak 0.4 -> width 0.7
        fig.add_trace(go.Scatter(x=xi + dens * 1.75, y=w * xi + t, mode="lines", line=dict(color=GREY, width=2),
                                 showlegend=False), 1, 1)
        fig.add_trace(go.Scatter(x=[xi, xi + stats.norm.pdf(yi - w * xi) * 1.75], y=[yi, yi], mode="lines",
                                 line=dict(color=GREEN, width=5), showlegend=False), 1, 1)
        fig.add_trace(go.Scatter(x=[xi, xi], y=[yi, w * xi], mode="lines", line=dict(color=RED, width=3, dash="dot"),
                                 showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=X, y=Y, mode="markers", marker=dict(size=13, color="black"), showlegend=False), 1, 1)
    seen = w_fine <= w + 1e-9
    fig.add_trace(go.Scatter(x=w_fine[seen], y=[nll(v) for v in w_fine[seen]], mode="lines",
                             line=dict(color=GREEN, width=4), showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=w_fine[seen], y=[mse(v) for v in w_fine[seen]], mode="lines",
                             line=dict(color=ORANGE, width=4, dash="dash"), showlegend=False), 2, 1, secondary_y=True)
    fig.add_vline(x=W_HAT, line=dict(color=GREY, dash="dot", width=2), row=2, col=1)
    fig.update_xaxes(range=[0, 5], title_text="x", row=1, col=1)
    fig.update_yaxes(range=[-1, 12], title_text="y", row=1, col=1)
    fig.update_xaxes(range=[1.4, 2.6], title_text="slope w", row=2, col=1)
    fig.update_yaxes(range=[3, 12], title_text="NLL", row=2, col=1, secondary_y=False)
    fig.update_yaxes(range=[0, 4.5], title_text="MSE", row=2, col=1, secondary_y=True)
    fig.update_layout(template="simple_white", width=900, height=900, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"w = {w:.2f}    NLL = {nll(w):.2f}    MSE = {mse(w):.3f}", x=0.5, y=0.985),
                      margin=dict(l=80, r=80, t=110, b=60))
    fig.update_annotations(font_size=19)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".noise_frames"
    tmp.mkdir(exist_ok=True)
    for k, w in enumerate(WS):
        frame(w).write_image(tmp / f"{k:03d}.png")
    last = len(WS) - 1
    for k in range(last + 1, last + 7):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "gaussian_noise.gif")], check=True)
    keys = [Image.open(tmp / f"{list(WS).index(v):03d}.png").convert("RGB") for v in (1.5, 1.8, 2.0, 2.5)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "gaussian_noise_frames.png")
    shutil.rmtree(tmp)
