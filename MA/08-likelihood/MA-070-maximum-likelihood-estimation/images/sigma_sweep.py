"""Searching for the standard deviation with the mean fixed at 32. The width of N(32, sigma^2) grows from 0.8 to 5
over the five mouse weights 29, 31, 32, 33, 35. Top: the curve and the five heights. Bottom: their product, the
likelihood, traced against sigma; highest at sigma = 2 (2.59e-5). Replaces the still sigma_search figure.
Run: python sigma_sweep.py  -> sigma_sweep.gif, sigma_sweep_frames.png (Plotly frames + ffmpeg)"""
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
SIGMAS = np.round(np.arange(0.8, 5.01, 0.2), 2)
grid = np.linspace(22, 42, 400)
s_fine = np.linspace(0.8, 5, 400)
lik = lambda s: stats.norm(32, s).pdf(X).prod()
L_fine = np.array([lik(s) for s in s_fine]) * 1e5
assert abs(s_fine[L_fine.argmax()] - 2) < 0.02
assert np.allclose([lik(1) * 1e5, lik(2) * 1e5, lik(4) * 1e5], [0.05, 2.59, 0.53], atol=0.006)


def frame(s):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.16, row_heights=[0.55, 0.45],
                        subplot_titles=("the curve N(32, σ²) and the height above each mouse",
                                        "likelihood = product of the five heights"))
    fig.add_trace(go.Scatter(x=grid, y=stats.norm(32, s).pdf(grid), mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    for xi, hi in zip(X, stats.norm(32, s).pdf(X)):
        fig.add_trace(go.Scatter(x=[xi, xi], y=[0, hi], mode="lines", line=dict(color=ORANGE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=X, y=np.zeros_like(X), mode="markers", marker=dict(size=14, color="black")), 1, 1)
    seen = s_fine <= s + 1e-9
    fig.add_trace(go.Scatter(x=s_fine[seen], y=L_fine[seen], mode="lines", line=dict(color=GREEN, width=4)), 2, 1)
    fig.add_trace(go.Scatter(x=[s], y=[lik(s) * 1e5], mode="markers", marker=dict(size=14, color=GREEN)), 2, 1)
    fig.update_xaxes(range=[22, 42], title_text="mouse weight (grams)", row=1, col=1)
    fig.update_yaxes(range=[0, 0.42], title_text="density", row=1, col=1)
    fig.update_xaxes(range=[0.8, 5], title_text="standard deviation σ of the curve", row=2, col=1)
    fig.update_yaxes(range=[0, 2.9], title_text="likelihood (× 10⁻⁵)", row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=820, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"σ = {s:.1f}    likelihood = {lik(s) * 1e5:.2f} × 10⁻⁵", x=0.5, y=0.985),
                      margin=dict(l=80, r=30, t=110, b=60))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sigma_frames"
    tmp.mkdir(exist_ok=True)
    for k, s in enumerate(SIGMAS):
        frame(s).write_image(tmp / f"{k:03d}.png")
    last = len(SIGMAS) - 1
    for k in range(last + 1, last + 7):                        # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "sigma_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{list(SIGMAS).index(v):03d}.png").convert("RGB") for v in (1.0, 2.0, 3.0, 5.0)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "sigma_sweep_frames.png")
    shutil.rmtree(tmp)
