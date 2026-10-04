"""100 random picks (with replacement) from 100 training points, against one shuffled epoch (each point once).
Each cell is one point; its number is how often it has been picked. Random picks leave about a third unseen.
Run: python random_picks.py -> random_picks.gif, random_picks_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
RED, GREEN, ORANGE, GREY = "#E45756", "#54A24B", "#F58518", "#6B6B6B"
N = 100
rng = np.random.default_rng(0)
random_picks = rng.integers(0, N, N)             # one "epoch" of random single picks
shuffled = rng.permutation(N)                    # one shuffled epoch
# the theory value (1 - 1/100)^100 = 0.366, and the average over many runs agrees
unseen = [(np.bincount(np.random.default_rng(s).integers(0, N, N), minlength=N) == 0).sum() for s in range(2000)]
assert abs(np.mean(unseen) / N - (1 - 1 / N) ** N) < 0.01
# colours by count: 0 unseen (red), 1 once (green), 2 or more (orange, darker for more)
SCALE = [[0, RED], [0.249, RED], [0.25, GREEN], [0.499, GREEN], [0.5, "#F9B46B"], [0.749, "#F9B46B"],
         [0.75, ORANGE], [1, ORANGE]]


def counts(order, k):
    return np.bincount(order[:k], minlength=N).reshape(10, 10)


def frame(k):
    fig = make_subplots(1, 2, horizontal_spacing=0.06,
                        subplot_titles=["random picks", "shuffled epoch"])
    for col, order in ((1, random_picks), (2, shuffled)):
        c = counts(order, k)
        fig.add_trace(go.Heatmap(z=np.minimum(c, 3), zmin=0, zmax=3, colorscale=SCALE, showscale=False,
                                 text=c, texttemplate="%{text}", textfont=dict(size=22, color="white"),
                                 xgap=3, ygap=3), 1, col)
        miss = int((c == 0).sum())
        fig.add_annotation(text=f"never picked: <b>{miss}</b>", x=4.5, y=-1.3, xref=f"x{col}", yref=f"y{col}",
                           showarrow=False, font=dict(size=28, color=RED if miss else GREEN))
    fig.update_xaxes(visible=False, range=[-0.6, 9.6])
    fig.update_yaxes(visible=False, range=[-2.0, 9.6], scaleanchor="x")
    fig.update_yaxes(scaleanchor="x2", row=1, col=2)
    fig.update_annotations(selector=dict(text="random picks"), font=dict(size=28))
    fig.update_annotations(selector=dict(text="shuffled epoch"), font=dict(size=28))
    fig.update_layout(template="simple_white", width=1000, height=640,
                      font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"100 points, {k} picks so far   (red 0, green 1, orange 2+)", x=0.5, y=0.97,
                                 font=dict(size=26)),
                      margin=dict(l=10, r=10, t=110, b=10))
    return fig


if __name__ == "__main__":
    print("unseen after 100 random picks, this run:", (counts(random_picks, N) == 0).sum(),
          " average over 2000 runs:", np.mean(unseen))
    tmp = HERE / ".pick_frames"
    tmp.mkdir(exist_ok=True)
    ks = list(range(0, N + 1, 5))
    for i, k in enumerate(ks):
        frame(k).write_image(tmp / f"{i:03d}.png")
    for i in range(len(ks), len(ks) + 8):                     # hold the last frame
        shutil.copy(tmp / f"{len(ks) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "random_picks.gif")], check=True)
    keys = [Image.open(tmp / f"{ks.index(k):03d}.png").convert("RGB") for k in (25, 50, 75, 100)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "random_picks_frames.png")
    shutil.rmtree(tmp)
