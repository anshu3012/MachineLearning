"""Binomial MLE as an animation: 4 of 7 people prefer orange Fanta. Top: the PMF of B(7, p) with the bar at x = 4
highlighted (its height is the likelihood of p). Bottom: that height traced against p; the peak is at p = 4/7.
Run: python binomial_sweep.py  -> binomial_sweep.gif, binomial_sweep_frames.png (Plotly frames + ffmpeg)"""
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
N, X = 7, 4
PS = np.round(np.arange(0.05, 0.951, 0.05), 2)
p_fine = np.linspace(0.01, 0.99, 400)
L_fine = stats.binom(N, p_fine).pmf(X)
assert abs(p_fine[L_fine.argmax()] - X / N) < 0.005


def frame(p):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.17, row_heights=[0.5, 0.5],
                        subplot_titles=(f"PMF of B(7, p): probability of each count, p = {p:.2f}",
                                        "likelihood of p = height of the orange bar"))
    k = np.arange(N + 1)
    fig.add_trace(go.Bar(x=k, y=stats.binom(N, p).pmf(k), marker_color=[ORANGE if i == X else "#C9D6E5" for i in k],
                         showlegend=False), 1, 1)
    seen = p_fine <= p + 1e-9
    fig.add_trace(go.Scatter(x=p_fine[seen], y=L_fine[seen], mode="lines", line=dict(color=GREEN, width=4),
                             showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=[p], y=[stats.binom(N, p).pmf(X)], mode="markers", marker=dict(size=14, color=ORANGE),
                             showlegend=False), 2, 1)
    fig.update_xaxes(title_text="number who prefer orange (x)", dtick=1, row=1, col=1)
    fig.update_yaxes(range=[0, 0.75], title_text="probability", row=1, col=1)
    fig.update_xaxes(range=[0, 1], title_text="p, the chance a person prefers orange", row=2, col=1)
    fig.update_yaxes(range=[0, 0.33], title_text="L(p | x = 4, n = 7)", row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=820, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"p = {p:.2f}    likelihood = {stats.binom(N, p).pmf(X):.3f}", x=0.5, y=0.985),
                      margin=dict(l=80, r=30, t=110, b=60))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".binom_frames"
    tmp.mkdir(exist_ok=True)
    for k, p in enumerate(PS):
        frame(p).write_image(tmp / f"{k:03d}.png")
    last = len(PS) - 1
    for k in range(last + 1, last + 7):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "binomial_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{list(PS).index(q):03d}.png").convert("RGB") for q in (0.25, 0.4, 0.55, 0.85)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "binomial_sweep_frames.png")
    shutil.rmtree(tmp)
