"""A 9 from MNIST passes through a small trained CNN, one layer per stage: the input, the 8 maps of the first
convolution layer (with their 3 x 3 filters), the 16 maps of the second, and the 10 output probabilities.
Data: data/cnn_layers.npz from the Notebook. Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from common import BLUE, GREY, RED

HERE = Path(__file__).parent
d = np.load(HERE.parent / "data" / "cnn_layers.npz")
digit, K, C1, C2, P = d["digit"], d["kernels1"], d["conv1"], d["conv2"], d["probs"]
assert P.argmax() == 9 and C1.shape == (26, 26, 8) and C2.shape == (11, 11, 16)
FONT = dict(family="Latin Modern Roman", size=24)
W, H = 1000, 640
MAP = dict(colorscale="Inferno", showscale=False)


def square(fig):
    """Equal-aspect, axis-free heatmap panels."""
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False, autorange="reversed")
    for ax in fig.layout:
        if ax.startswith("yaxis"):
            fig.layout[ax].scaleanchor = ax.replace("yaxis", "x")


def layout(fig, title):
    fig.update_layout(template="simple_white", width=W, height=H, font=FONT, margin=dict(l=10, r=10, t=80, b=10),
                      title=dict(text=title, x=0.5, y=0.97), showlegend=False)
    return fig


def stage_input():
    fig = make_subplots(1, 1)
    fig.add_trace(go.Heatmap(z=digit, colorscale="gray", showscale=False))
    square(fig)
    return layout(fig, "1. Input: a 28 × 28 grid of pixels")


def stage_conv1(n):
    """First n of the 8 layer-1 maps shown, each under its 3 x 3 filter (red +, blue -)."""
    specs = [[{"rowspan": 4}] + [{}] * 4] + [[None] + [{}] * 4 for _ in range(3)]
    fig = make_subplots(4, 5, specs=specs, row_heights=[0.17, 0.33, 0.17, 0.33], column_widths=[0.28] + [0.18] * 4,
                        horizontal_spacing=0.02, vertical_spacing=0.02)
    fig.add_trace(go.Heatmap(z=digit, colorscale="gray", showscale=False), 1, 1)
    vmax = np.abs(K).max()
    for i in range(8):
        r, c = 1 + 2 * (i // 4), 2 + i % 4
        kz = K[:, :, i] if i < n else np.zeros((3, 3))
        mz = C1[:, :, i] if i < n else np.zeros((26, 26))
        fig.add_trace(go.Heatmap(z=kz, colorscale="RdBu", reversescale=True, zmin=-vmax, zmax=vmax, showscale=False),
                      r, c)
        fig.add_trace(go.Heatmap(z=mz, zmin=0, zmax=C1.max(), **MAP), r + 1, c)
    square(fig)
    return layout(fig, "2. Layer 1: 8 filters (3 × 3) give 8 maps")


def stage_conv2(n):
    """First n of the 16 layer-2 maps, 4 x 4 grid, beside the input."""
    specs = [[{"rowspan": 4}] + [{}] * 4] + [[None] + [{}] * 4 for _ in range(3)]
    fig = make_subplots(4, 5, specs=specs, column_widths=[0.28] + [0.18] * 4,
                        horizontal_spacing=0.02, vertical_spacing=0.02)
    fig.add_trace(go.Heatmap(z=digit, colorscale="gray", showscale=False), 1, 1)
    for i in range(16):
        z = C2[:, :, i] if i < n else np.zeros((11, 11))
        fig.add_trace(go.Heatmap(z=z, zmin=0, zmax=C2.max(), **MAP), 1 + i // 4, 2 + i % 4)
    square(fig)
    return layout(fig, "3. Layer 2: 16 maps, each sees an 8 × 8 patch")


def stage_output(t):
    """Probability bars grown to share t of their height."""
    fig = make_subplots(1, 2, column_widths=[0.28, 0.72], horizontal_spacing=0.12)
    fig.add_trace(go.Heatmap(z=digit, colorscale="gray", showscale=False), 1, 1)
    fig.add_trace(go.Bar(x=list(range(10)), y=t * P, marker_color=[RED if k == 9 else BLUE for k in range(10)],
                         text=[f"{P[9]:.2f}" if (k == 9 and t == 1) else "" for k in range(10)],
                         textposition="outside"), 1, 2)
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor="x", row=1, col=1)
    fig.update_xaxes(title="digit", tickmode="linear", dtick=1, row=1, col=2)
    fig.update_yaxes(title="probability", range=[0, 1.12], row=1, col=2)
    return layout(fig, "4. Output: the network says 9")


FRAMES = ([stage_input()] * 4 + [stage_conv1(n) for n in range(1, 9)] + [stage_conv1(8)] * 4
          + [stage_conv2(n) for n in (4, 8, 12, 16)] + [stage_conv2(16)] * 4
          + [stage_output(t) for t in (0.2, 0.4, 0.6, 0.8, 1.0)] + [stage_output(1.0)] * 8)
KEYS = (0, 11, 19, len(FRAMES) - 1)                           # one frame per stage, each fully built

if __name__ == "__main__":
    tmp = HERE / ".cnn_frames"
    tmp.mkdir(exist_ok=True)
    done = {}
    for k, fig in enumerate(FRAMES):
        if id(fig) in done:                                    # repeated (held) frame
            shutil.copy(done[id(fig)], tmp / f"{k:03d}.png")
        else:
            fig.write_image(tmp / f"{k:03d}.png")
            done[id(fig)] = tmp / f"{k:03d}.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "cnn_layers.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in KEYS]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "cnn_layers_frames.png")
    shutil.rmtree(tmp)
