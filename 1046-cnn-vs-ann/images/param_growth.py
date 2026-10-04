"""Section 5.2 as an animation: the image grows from 28 x 28 x 3 to 1080 x 1080 x 3. A Conv2D layer of 50 filters
of 3 x 3 keeps 1,400 parameters; a Dense layer of 100 nodes on the flattened image grows with the pixel count
(Plotly frames + ffmpeg). Run: python param_growth.py -> param_growth.gif, param_growth_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, RED, GREY, FONT

HERE = Path(__file__).parent
conv = lambda n: (3 * 3 * 3 + 1) * 50                       # does not depend on n
dense = lambda n: (n * n * 3 + 1) * 100
assert conv(224) == conv(1080) == 1_400
assert dense(224) == 15_052_900 and dense(1080) == 349_920_100   # the Note's table (Keras in the Notebook)
SIDES = [28, 64, 128, 224, 320, 480, 640, 800, 960, 1080]
grid = np.arange(28, 1081, 4)


def frame(n):
    fig = go.Figure()
    g = grid[grid <= n]
    fig.add_trace(go.Scatter(x=g, y=dense(g), name="Dense, 100 nodes", line=dict(color=RED, width=4)))
    fig.add_trace(go.Scatter(x=g, y=[conv(0)] * len(g), name="Conv2D, 50 filters 3 × 3", line=dict(color=BLUE, width=4)))
    fig.add_trace(go.Scatter(x=[n, n], y=[dense(n), conv(n)], mode="markers+text", showlegend=False,
                             marker=dict(size=14, color=[RED, BLUE]),
                             text=[f"{dense(n):,}", "1,400"], textposition=["top right", "bottom right"] if n < 400 else ["top left", "bottom left"],
                             textfont=dict(size=22, color=[RED, BLUE])))
    fig.update_layout(template="simple_white", width=900, height=600, font=dict(FONT, size=20),
                      title=dict(text=f"image {n} × {n} × 3", x=0.5, font=dict(size=26)),
                      xaxis=dict(title="image height = width (pixels)", range=[0, 1120]),
                      yaxis=dict(type="log", title="parameters (log scale)", range=[2.5, 9.2],
                                 tickvals=[1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9],
                                 ticktext=["1k", "10k", "100k", "1M", "10M", "100M", "1B"]),
                      legend=dict(x=0.45, y=0.5), margin=dict(l=90, r=30, t=70, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".growth_frames"
    tmp.mkdir(exist_ok=True)
    seq = [s for s in SIDES for _ in range(2)] + [SIDES[-1]] * 8
    files = {}
    for s in SIDES:
        files[s] = tmp / f"n{s}.png"
        frame(s).write_image(files[s])
    for j, s in enumerate(seq):
        shutil.copy(files[s], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "param_growth.gif")], check=True)
    keys = [Image.open(files[s]).convert("RGB") for s in (28, 224, 640, 1080)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "param_growth_frames.png")
    shutil.rmtree(tmp)
