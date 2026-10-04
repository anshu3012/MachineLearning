"""Sliding a normal curve (sigma = 2) across five mouse weights 29, 31, 32, 33, 35.
Top: the curve and the five heights (one likelihood factor per mouse). Bottom: the product of the heights,
the likelihood, traced as the mean moves. The peak is at mu = 32, the average weight.
Run: python likelihood_sweep.py  -> likelihood_sweep.gif, likelihood_sweep_frames.png (Plotly frames + ffmpeg)"""
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
X = np.array([29, 31, 32, 33, 35.0])
SIGMA = 2
MUS = np.round(np.arange(26, 38.01, 0.5), 2)
grid = np.linspace(22, 42, 400)
mu_fine = np.linspace(26, 38, 400)
lik = lambda mu: stats.norm(mu, SIGMA).pdf(X).prod()
L_fine = np.array([lik(m) for m in mu_fine]) * 1e5
assert abs(mu_fine[L_fine.argmax()] - X.mean()) < 0.05


SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def sci(v):                                                  # 1.18e-09 -> "1.18 × 10⁻⁹"
    m, e = f"{v:.2e}".split("e")
    return f"{m} × 10{str(int(e)).translate(SUP)}"


def frame(mu):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.16, row_heights=[0.55, 0.45],
                        subplot_titles=("the curve N(μ, 2²) and the height above each mouse",
                                        "likelihood = product of the five heights"))
    fig.add_trace(go.Scatter(x=grid, y=stats.norm(mu, SIGMA).pdf(grid), mode="lines", line=dict(color=BLUE, width=4),
                             showlegend=False), 1, 1)
    h = stats.norm(mu, SIGMA).pdf(X)
    for xi, hi in zip(X, h):
        fig.add_trace(go.Scatter(x=[xi, xi], y=[0, hi], mode="lines", line=dict(color=ORANGE, width=4),
                                 showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=X, y=np.zeros_like(X), mode="markers", marker=dict(size=14, color="black"),
                             showlegend=False), 1, 1)
    fig.add_vline(x=mu, line=dict(color=GREY, dash="dot", width=2), row=1, col=1)
    seen = mu_fine <= mu + 1e-9
    fig.add_trace(go.Scatter(x=mu_fine[seen], y=L_fine[seen], mode="lines", line=dict(color=GREEN, width=4),
                             showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=[mu], y=[lik(mu) * 1e5], mode="markers", marker=dict(size=14, color=GREEN),
                             showlegend=False), 2, 1)
    fig.update_xaxes(range=[22, 42], title_text="mouse weight (grams)", row=1, col=1)
    fig.update_yaxes(range=[0, 0.23], title_text="density", row=1, col=1)
    fig.update_xaxes(range=[26, 38], title_text="mean μ of the curve", row=2, col=1)
    fig.update_yaxes(range=[0, 2.9], title_text="likelihood (× 10⁻⁵)", row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=820, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"μ = {mu:.1f}    likelihood = {sci(lik(mu))}", x=0.5, y=0.985),
                      margin=dict(l=80, r=30, t=110, b=60))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    for k, mu in enumerate(MUS):
        frame(mu).write_image(tmp / f"{k:03d}.png")
    last = len(MUS) - 1
    for k in range(last + 1, last + 7):                      # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "likelihood_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{list(MUS).index(m):03d}.png").convert("RGB") for m in (28.0, 30.0, 32.0, 36.0)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "likelihood_sweep_frames.png")
    shutil.rmtree(tmp)
