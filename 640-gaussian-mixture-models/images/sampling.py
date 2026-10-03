"""Sampling from a Gaussian mixture in two steps, animated. Top: the mixture weights 0.5, 0.2, 0.3; the component
picked for the latest draw is highlighted. Bottom: the latest draw (diamond) and the density histogram of all draws,
coloured by the component that generated each, growing towards the mixture density (black).
Run: python sampling.py -> sampling.gif, sampling_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

from common import COLS, FONT, GREY, MU, PI, components, mixture, sample

HERE = Path(__file__).parent
rng = np.random.default_rng(1)
z, x = sample(3000, rng)
COUNTS = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 80, 120, 200, 300, 500, 800, 1200, 2000, 3000]
edges = np.arange(-5.5, 8.01, 0.5)
g = np.linspace(-5.5, 8, 400)


def frame(n):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.15, row_heights=[0.25, 0.75],
                        subplot_titles=("step 1: pick a component with probability π<sub>k</sub>",
                                        f"step 2: draw x from it   ({n} draws so far)"))
    last = z[n - 1]
    fig.add_trace(go.Bar(x=[0.5, 0.2, 0.3], y=["k = 1", "k = 2", "k = 3"], orientation="h",
                         marker_color=[c if k == last else "#DDDDDD" for k, c in enumerate(COLS)],
                         text=["π₁ = 0.5", "π₂ = 0.2", "π₃ = 0.3"], textposition="outside", showlegend=False), 1, 1)
    width = edges[1] - edges[0]
    for k in range(3):
        h, _ = np.histogram(x[:n][z[:n] == k], bins=edges)
        fig.add_trace(go.Bar(x=edges[:-1] + width / 2, y=h / (n * width), width=width, marker_color=COLS[k],
                             opacity=0.75, name=f"from component {k + 1}"), 2, 1)
    comp = components(g)
    for k in range(3):
        fig.add_trace(go.Scatter(x=g, y=comp[:, k], mode="lines", line=dict(color=COLS[k], width=2, dash="dash"),
                                 showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=g, y=mixture(g), mode="lines", line=dict(color="black", width=3), name="mixture p(x)"), 2, 1)
    fig.add_trace(go.Scatter(x=[x[n - 1]], y=[0.02], mode="markers", marker=dict(symbol="diamond", size=18,
                             color=COLS[last], line=dict(color="black", width=1.5)), name="latest draw"), 2, 1)
    fig.update_xaxes(range=[0, 0.75], showticklabels=False, row=1, col=1)
    fig.update_xaxes(range=[-5.5, 8], title_text="x", row=2, col=1)
    fig.update_yaxes(range=[0, 0.42], title_text="density", row=2, col=1)
    fig.update_layout(template="simple_white", barmode="stack", width=900, height=820, font=FONT, bargap=0,
                      title=dict(text=f"latest draw: component {last + 1}, x = {x[n - 1]:.2f}", x=0.5, y=0.985),
                      legend=dict(x=0.62, y=0.6), margin=dict(l=80, r=30, t=110, b=60))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    assert abs(np.mean(z == 0) - 0.5) < 0.03 and abs(x.mean() - PI @ MU) < 0.15
    tmp = HERE / ".sampling_frames"
    tmp.mkdir(exist_ok=True)
    for k, n in enumerate(COUNTS):
        frame(n).write_image(tmp / f"{k:03d}.png")
    last = len(COUNTS) - 1
    for k in range(last + 1, last + 6):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "sampling.gif")], check=True)
    keys = [Image.open(tmp / f"{COUNTS.index(n):03d}.png").convert("RGB") for n in (1, 10, 200, 3000)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "sampling_frames.png")
    shutil.rmtree(tmp)
