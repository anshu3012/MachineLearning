"""The height example as an animation. One person is measured at 130 cm (the data, fixed). The candidate
distribution N(mu, 10^2) slides from mu = 100 to 200 cm; the likelihood of each mu is the height of its curve above
130 (top). Bottom: those heights traced against mu. The likelihood is highest when the curve is centred on 130.
Run: python likelihood_slide.py -> likelihood_slide.gif, likelihood_slide_frames.png (Plotly frames + ffmpeg)"""
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
FONT = dict(family="Latin Modern Roman", size=20)
X0, SD = 130.0, 10.0
MUS = np.arange(100, 200.1, 5.0)
grid = np.linspace(60, 240, 600)
mu_fine = np.linspace(100, 200, 400)
L = stats.norm(mu_fine, SD).pdf(X0)
assert abs(mu_fine[L.argmax()] - X0) < 0.3


def frame(mu):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.16, row_heights=[0.55, 0.45],
                        subplot_titles=("candidate distribution N(μ, 10²); data fixed at 130 cm",
                                        "likelihood of μ given the observation 130 cm"))
    fig.add_trace(go.Scatter(x=grid, y=stats.norm(mu, SD).pdf(grid), mode="lines", line=dict(color=BLUE, width=4),
                             showlegend=False), 1, 1)
    h = stats.norm(mu, SD).pdf(X0)
    fig.add_trace(go.Scatter(x=[X0, X0], y=[0, h], mode="lines", line=dict(color=ORANGE, width=5), showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=[X0], y=[0], mode="markers", marker=dict(size=14, color="black"), showlegend=False), 1, 1)
    seen = mu_fine <= mu + 1e-9
    fig.add_trace(go.Scatter(x=mu_fine[seen], y=L[seen], mode="lines", line=dict(color=GREEN, width=4),
                             showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=[mu], y=[h], mode="markers", marker=dict(size=14, color=ORANGE), showlegend=False), 2, 1)
    fig.update_xaxes(range=[60, 240], title_text="height (cm)", row=1, col=1)
    fig.update_yaxes(range=[0, 0.045], title_text="density", row=1, col=1)
    fig.update_xaxes(range=[100, 200], title_text="mean μ of the candidate distribution (cm)", row=2, col=1)
    fig.update_yaxes(range=[0, 0.045], title_text="likelihood", row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=820, font=FONT,
                      title=dict(text=f"μ = {mu:.0f} cm    likelihood = {h:.2g}", x=0.5, y=0.985),
                      margin=dict(l=80, r=30, t=110, b=60))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".slide_frames"
    tmp.mkdir(exist_ok=True)
    for k, mu in enumerate(MUS):
        frame(mu).write_image(tmp / f"{k:03d}.png")
    last = len(MUS) - 1
    for k in range(last + 1, last + 6):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "likelihood_slide.gif")], check=True)
    keys = [Image.open(tmp / f"{list(MUS).index(m):03d}.png").convert("RGB") for m in (100.0, 120.0, 130.0, 160.0)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "likelihood_slide_frames.png")
    shutil.rmtree(tmp)
