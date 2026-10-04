"""One mouse at 32 grams under a normal curve with sigma = 2 whose mean slides from 24 to 40.
Top: the curve and its height above the mouse (the likelihood). Bottom: that height traced against the mean, with
the tangent line at the current mean; the tangent is flat (slope 0) at mu = 32, the peak.
Run: python one_point_sweep.py  -> one_point_sweep.gif, one_point_sweep_frames.png (Plotly frames + ffmpeg)"""
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
X0, SIGMA = 32.0, 2.0
MUS = np.round(np.arange(24, 40.01, 0.5), 2)
grid = np.linspace(20, 44, 400)
mu_fine = np.linspace(24, 40, 400)
lik = lambda mu: stats.norm(mu, SIGMA).pdf(X0)
slope = lambda mu: lik(mu) * (X0 - mu) / SIGMA**2             # d/dmu of the normal density at X0
assert np.allclose([lik(28), lik(30), lik(32)], [0.027, 0.121, 0.199], atol=5e-4)


def frame(mu):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.17, row_heights=[0.5, 0.5],
                        subplot_titles=("the curve N(μ, 2²) and its height above the mouse",
                                        "likelihood of μ = that height"))
    fig.add_trace(go.Scatter(x=grid, y=stats.norm(mu, SIGMA).pdf(grid), mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=[X0, X0], y=[0, lik(mu)], mode="lines", line=dict(color=ORANGE, width=6)), 1, 1)
    fig.add_trace(go.Scatter(x=[X0], y=[0], mode="markers", marker=dict(size=16, color="black")), 1, 1)
    fig.add_vline(x=mu, line=dict(color=GREY, dash="dot", width=2), row=1, col=1)
    fig.add_annotation(x=X0 + 0.5, y=lik(mu), text=f"{lik(mu):.3f}", showarrow=False, xanchor="left",
                       font=dict(size=22, color=ORANGE), xref="x1", yref="y1")
    seen = mu_fine <= mu + 1e-9
    fig.add_trace(go.Scatter(x=mu_fine[seen], y=lik(mu_fine[seen]), mode="lines", line=dict(color=GREEN, width=4)), 2, 1)
    t = np.array([mu - 1.6, mu + 1.6])                         # tangent line at the current mean
    fig.add_trace(go.Scatter(x=t, y=lik(mu) + slope(mu) * (t - mu), mode="lines", line=dict(color=RED, width=3)), 2, 1)
    fig.add_trace(go.Scatter(x=[mu], y=[lik(mu)], mode="markers", marker=dict(size=15, color=GREEN)), 2, 1)
    fig.update_xaxes(range=[20, 44], title_text="mouse weight (grams)", row=1, col=1)
    fig.update_yaxes(range=[0, 0.24], title_text="density", row=1, col=1)
    fig.update_xaxes(range=[24, 40], title_text="mean μ of the curve", row=2, col=1)
    fig.update_yaxes(range=[-0.02, 0.24], title_text="likelihood", row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=820, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"μ = {mu:.1f}    likelihood {lik(mu):.3f}    slope {slope(mu):+.3f}",
                                 x=0.5, y=0.985),
                      margin=dict(l=80, r=30, t=110, b=60))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".one_point_frames"
    tmp.mkdir(exist_ok=True)
    for k, mu in enumerate(MUS):
        frame(mu).write_image(tmp / f"{k:03d}.png")
    last = len(MUS) - 1
    for k in range(last + 1, last + 7):                        # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "one_point_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{list(MUS).index(m):03d}.png").convert("RGB") for m in (28.0, 30.0, 32.0, 36.0)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "one_point_sweep_frames.png")
    shutil.rmtree(tmp)
