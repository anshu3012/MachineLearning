"""Gradient descent on the Ridge loss for three lambdas, from the same start, drawn on the contours of the plain
squared-error loss (Plotly frames + ffmpeg -> ridge_race.gif, ridge_race_frames.png). The bigger lambda, the
closer to m = 0 the path stops; the dashed curve is every Ridge answer as lambda runs from 0 upwards.
Right: the line each path gives, on the data. Same data, start and learning rate as paths.py."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, noise=20, random_state=13)
x = X.ravel()
LAMS = {0: BLUE, 100: ORANGE, 250: GREEN}
STEPS, LR = 40, 0.005


def descend(lam):
    m, b, path = -5.0, 20.0, [(-5.0, 20.0)]
    for _ in range(STEPS):
        err = y - m * x - b
        m, b = m - LR * (-(err * x).sum() + lam * m), b - LR * (-err.sum())
        path.append((m, b))
    return np.array(path)


paths = {lam: descend(lam) for lam in LAMS}
for lam, P in paths.items():                                # each path ends at sklearn's Ridge answer
    r = Ridge(alpha=lam).fit(X, y)
    assert np.allclose(P[-1], [r.coef_[0], r.intercept_], atol=0.05), (lam, P[-1])
    print(lam, P[-1].round(1))
curve = np.array([[r.coef_[0], r.intercept_] for r in (Ridge(alpha=a).fit(X, y) for a in np.r_[0, np.geomspace(1, 1e5, 80)])])
ms, bs = np.linspace(-10, 35, 160), np.linspace(-15, 25, 160)
M, B = np.meshgrid(ms, bs)
Z = np.log(((y[:, None, None] - M * x[:, None, None] - B) ** 2).sum(0))
SHOW = 20                                                   # all three have settled by step 20
FRAMES = list(range(SHOW + 1)) + [SHOW] * 8


def frame(k):
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                        subplot_titles=(f"step {k}: squared-error contours", "the lines, on the data"))
    fig.add_trace(go.Contour(x=ms, y=bs, z=Z, showscale=False, colorscale="Greys", reversescale=True, opacity=0.8,
                             contours=dict(coloring="lines", size=0.25), line=dict(width=1)), 1, 1)
    fig.add_trace(go.Scatter(x=curve[:, 0], y=curve[:, 1], mode="lines", line=dict(color=GREY, width=3, dash="dash")),
                  1, 1)
    fig.add_trace(go.Scatter(x=X.ravel(), y=y, mode="markers", marker=dict(size=6, color=GREY, opacity=0.5)), 1, 2)
    xs = np.array([-3, 3])
    for lam, c in LAMS.items():
        P = paths[lam][:k + 1]
        fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines+markers", line=dict(color=c, width=3),
                                 marker=dict(size=6), name=f"λ = {lam}: m = {P[-1, 0]:.1f}"), 1, 1)
        fig.add_trace(go.Scatter(x=xs, y=P[-1, 0] * xs + P[-1, 1], mode="lines", line=dict(color=c, width=4),
                                 showlegend=False), 1, 2)
    fig.add_trace(go.Scatter(x=[-5], y=[20], mode="markers+text", text=["start"], textposition="top right",
                             marker=dict(size=11, color="black"), showlegend=False), 1, 1)
    fig.add_annotation(x=12, y=-6, text="every Ridge answer,<br>λ from 0 up", showarrow=False, font=dict(size=17, color=GREY),
                       row=1, col=1)
    fig.update_xaxes(title="slope m", range=[-10, 35], row=1, col=1)
    fig.update_yaxes(title="intercept b", range=[-15, 25], row=1, col=1)
    fig.update_xaxes(title="x", range=[-3, 3], row=1, col=2)
    fig.update_yaxes(title="y", range=[-90, 90], row=1, col=2)
    fig.update_layout(template="simple_white", width=1150, height=560, font=dict(family="Latin Modern Roman", size=20),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=30, t=60, b=130))
    fig.update_traces(showlegend=False, selector=dict(type="contour"))
    for t in fig.data[:3]:
        t.showlegend = False
    fig.update_annotations(font_size=21, yshift=-6)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ridge_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(FRAMES):
        frame(k).write_image(tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "ridge_race.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 1, 3, SHOW + 8)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "ridge_race_frames.png")
    shutil.rmtree(tmp)
