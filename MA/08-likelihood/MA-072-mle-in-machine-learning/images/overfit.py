"""Maximum likelihood polynomials of degree 0 to 9 fitted to 10 noisy points of y = -sin(x/5) + cos(x)
(noise standard deviation 0.2), as in Mathematics for Machine Learning, Section 9.2.2. Left: the fit. Right: training
and test RMSE up to the current degree. Training error only falls; test error falls, then explodes.
Run: python overfit.py -> overfit.gif, overfit_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
rng = np.random.default_rng(4)
truth = lambda x: -np.sin(x / 5) + np.cos(x)
x = np.linspace(-4.5, 4.5, 10) + rng.uniform(-0.3, 0.3, 10)
y = truth(x) + rng.normal(0, 0.2, 10)
xt = np.linspace(-4.5, 4.5, 200)
yt = truth(xt) + rng.normal(0, 0.2, 200)
phi = lambda v, M: np.vander(v, M + 1, increasing=True)        # columns 1, x, x^2, ..., x^M
fits = [np.linalg.lstsq(phi(x, M), y, rcond=None)[0] for M in range(10)]   # MLE = least squares
rmse = lambda th, v, t: np.sqrt(np.mean((phi(v, len(th) - 1) @ th - t) ** 2))
train = [rmse(th, x, y) for th in fits]
test = [rmse(th, xt, yt) for th in fits]
assert all(a >= b - 1e-9 for a, b in zip(train, train[1:])) and train[9] < 1e-6
assert np.argmin(test) in range(4, 9) and test[9] > 3 * min(test)


def frame(M):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, column_widths=[0.55, 0.45],
                        subplot_titles=(f"degree {M}: maximum likelihood fit", "error (RMSE)"))
    g = np.linspace(-4.7, 4.7, 400)
    fig.add_trace(go.Scatter(x=g, y=truth(g), mode="lines", line=dict(color=GREY, width=2, dash="dash"),
                             name="true function"), 1, 1)
    fig.add_trace(go.Scatter(x=g, y=phi(g, M) @ fits[M], mode="lines", line=dict(color=BLUE, width=4),
                             name="MLE polynomial"), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=12, color="black"), name="training data"), 1, 1)
    d = list(range(M + 1))
    fig.add_trace(go.Scatter(x=d, y=train[:M + 1], mode="lines+markers", line=dict(color=GREEN, width=4),
                             name="training error"), 1, 2)
    fig.add_trace(go.Scatter(x=d, y=np.minimum(test[:M + 1], 2.5), mode="lines+markers",
                             line=dict(color=RED, width=4), name="test error (capped at 2.5)"), 1, 2)
    fig.update_xaxes(range=[-4.8, 4.8], title_text="x", row=1, col=1)
    fig.update_yaxes(range=[-3, 3], title_text="y", row=1, col=1)
    fig.update_xaxes(range=[-0.3, 9.3], dtick=1, title_text="degree of the polynomial", row=1, col=2)
    fig.update_yaxes(range=[0, 2.6], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=dict(family="Latin Modern Roman", size=20),
                      legend=dict(orientation="h", x=0, y=-0.2), margin=dict(l=70, r=20, t=50, b=150))
    fig.update_annotations(font_size=21)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".overfit_frames"
    tmp.mkdir(exist_ok=True)
    for M in range(10):
        frame(M).write_image(tmp / f"{M:03d}.png")
    for k in range(10, 14):
        shutil.copy(tmp / "009.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "overfit.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (1, 4, 7, 9)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "overfit_frames.png")
    shutil.rmtree(tmp)
    print("train", np.round(train, 3), "\ntest", np.round(test, 3))
