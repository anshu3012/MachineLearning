"""Exponential likelihood as an animation: three waits between web-page views, 2, 2.5 and 1.5 seconds. The rate
lambda grows from 0.1 to 2. Top: the curve lambda e^(-lambda x) and its height above each wait. Bottom: the product
of the three heights, the likelihood lambda^3 e^(-6 lambda), traced against lambda; highest at lambda = 3/6 = 0.5.
Run: python exponential_sweep.py  -> exponential_sweep.gif, exponential_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X = np.array([2, 2.5, 1.5])
LAMS = np.round(np.arange(0.1, 2.001, 0.1), 2)
grid = np.linspace(0, 6, 300)
l_fine = np.linspace(0.05, 2, 400)
lik = lambda lam: (lam * np.exp(-lam * X)).prod()
L_fine = np.array([lik(l) for l in l_fine]) * 1e3
assert abs(l_fine[L_fine.argmax()] - 0.5) < 0.01
assert abs(lik(1) - 0.0025) < 1e-4 and abs(lik(0.5) - 0.0062) < 1e-4


def frame(lam):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.17, row_heights=[0.5, 0.5],
                        subplot_titles=("the curve λe<sup>−λx</sup> and its height above each wait",
                                        "likelihood = product of the three heights"))
    fig.add_trace(go.Scatter(x=grid, y=lam * np.exp(-lam * grid), mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    for xi in X:
        fig.add_trace(go.Scatter(x=[xi, xi], y=[0, lam * np.exp(-lam * xi)], mode="lines",
                                 line=dict(color=ORANGE, width=5)), 1, 1)
    fig.add_trace(go.Scatter(x=X, y=np.zeros(3), mode="markers", marker=dict(size=14, color="black")), 1, 1)
    seen = l_fine <= lam + 1e-9
    fig.add_trace(go.Scatter(x=l_fine[seen], y=L_fine[seen], mode="lines", line=dict(color=GREEN, width=4)), 2, 1)
    fig.add_trace(go.Scatter(x=[lam], y=[lik(lam) * 1e3], mode="markers", marker=dict(size=14, color=GREEN)), 2, 1)
    fig.update_xaxes(range=[0, 6], title_text="waiting time x (seconds)", row=1, col=1)
    fig.update_yaxes(range=[0, 1.05], title_text="density", row=1, col=1)
    fig.update_xaxes(range=[0, 2], title_text="rate λ (events per second)", row=2, col=1)
    fig.update_yaxes(range=[0, 7], title_text="likelihood (× 10⁻³)", row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=820, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"λ = {lam:.1f}    likelihood = {lik(lam) * 1e3:.2f} × 10⁻³", x=0.5, y=0.985),
                      margin=dict(l=80, r=30, t=110, b=60))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".exp_frames"
    tmp.mkdir(exist_ok=True)
    for k, lam in enumerate(LAMS):
        frame(lam).write_image(tmp / f"{k:03d}.png")
    last = len(LAMS) - 1
    for k in range(last + 1, last + 7):                        # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "exponential_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{list(LAMS).index(v):03d}.png").convert("RGB") for v in (0.2, 0.5, 1.0, 2.0)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "exponential_sweep_frames.png")
    shutil.rmtree(tmp)
