"""Building the positional encoding one position per frame (d_model = 128). Top: four of the 64 sine waves, with
angle rates 1, 1/10, 1/100 and 1/1000; the dots are their values at the current position. Bottom: the rows of the
encoding filled so far. Run: python pe_waves.py -> pe_waves.gif, pe_waves_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, ORANGE, GREEN, RED, FONT

HERE = Path(__file__).parent
N, D = 50, 128
pos, i = np.arange(N)[:, None], np.arange(D // 2)[None, :]
angle = pos / 10000 ** (2 * i / D)
pe = np.zeros((N, D))
pe[:, 0::2], pe[:, 1::2] = np.sin(angle), np.cos(angle)
WAVES = [(0, "1", BLUE), (32, "1/10", ORANGE), (64, "1/100", GREEN), (96, "1/1000", RED)]   # dimension, rate
xs = np.linspace(0, N - 1, 400)


def frame(p):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.5, 0.5], vertical_spacing=0.13,
                        subplot_titles=(f"dimension 2i: sin(pos × rate), position {p}",
                                        "positional encodings of positions 0 to " + str(p)))
    for dim, rate, c in WAVES:
        r = 1 / 10000 ** (dim / D)
        fig.add_trace(go.Scatter(x=xs, y=np.sin(xs * r), mode="lines", line=dict(color=c, width=2.5),
                                 name=f"dim {dim}, rate {rate}"), 1, 1)
        fig.add_trace(go.Scatter(x=[p], y=[np.sin(p * r)], mode="markers", marker=dict(color=c, size=13,
                                 line=dict(color="black", width=1)), showlegend=False), 1, 1)
    fig.add_vline(x=p, line=dict(color="black", dash="dot", width=1.5), row=1, col=1)
    z = pe.copy()
    z[p + 1:] = np.nan
    fig.add_trace(go.Heatmap(z=z, colorscale="RdBu", zmin=-1, zmax=1, showscale=False), 2, 1)
    for dim, _, c in WAVES:
        fig.add_vline(x=dim, line=dict(color=c, width=2), row=2, col=1)
    fig.update_xaxes(title="position", range=[-1, N], row=1, col=1)
    fig.update_yaxes(title="value", range=[-1.15, 1.15], row=1, col=1)
    fig.update_xaxes(title="dimension (0 to 127)", row=2, col=1)
    fig.update_yaxes(title="position", range=[N - 0.5, -0.5], row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=820, font=FONT,
                      legend=dict(orientation="h", x=0, y=1.1), margin=dict(l=70, r=20, t=110, b=55))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".pe_frames"
    tmp.mkdir(exist_ok=True)
    for p in range(N):
        frame(p).write_image(tmp / f"{p:03d}.png")
    for k in range(N, N + 8):                                 # hold the last frame
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "pe_waves.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 5, 20, N - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for j, im in enumerate(keys):
        sheet.paste(im, ((j % 2) * (w + 16), (j // 2) * (h + 16)))
    sheet.save(HERE / "pe_waves_frames.png")
    shutil.rmtree(tmp)
