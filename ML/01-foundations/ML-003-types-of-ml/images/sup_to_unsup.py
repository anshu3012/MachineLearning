"""Supervised vs unsupervised on one dataset. Frame 1: the 90 example students of clustering.py, coloured by a target
(placed or not). Frame 2: the target column is removed, every dot is grey: nothing to predict. Frame 3: k-means colours
the three groups it finds from IQ and CGPA alone. Example data; the placed column is made here (seeded): the chance of
placement rises with IQ and CGPA. Plotly frames -> ffmpeg GIF, plus a grid of the three frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

from clustering import COL, X, labels, names, scaled

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=24)
GREEN, RED, GREY = "#54A24B", "#E45756", "#8A8A8A"

p = 1 / (1 + np.exp(-2.0 * (scaled.sum(1) + 0.3)))        # higher IQ and CGPA: more likely placed
placed = np.random.default_rng(3).random(90) < p
assert placed.sum() == 47, placed.sum()


def frame(k):
    fig = go.Figure()
    if k == 0:
        title = "<b>Supervised:</b> every student has a target"
        for m, name, c in [(placed, "placed", GREEN), (~placed, "not placed", RED)]:
            fig.add_scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=name, marker=dict(size=14, color=c))
    elif k == 1:
        title = "<b>Target removed:</b> features only, nothing to predict"
        fig.add_scatter(x=X[:, 0], y=X[:, 1], mode="markers", name="no target", marker=dict(size=14, color=GREY))
    else:
        title = "<b>Unsupervised:</b> clustering finds 3 groups by itself"
        for j in sorted(names, key=lambda j: list(COL).index(names[j])):
            fig.add_scatter(x=X[labels == j, 0], y=X[labels == j, 1], mode="markers", name=names[j],
                            marker=dict(size=14, color=COL[names[j]]))
    fig.update_layout(template="simple_white", width=1000, height=720, font=FONT, title=dict(text=title, x=0.5, y=0.96),
                      xaxis=dict(title="IQ", range=[68, 136]), yaxis=dict(title="CGPA", range=[5.2, 9.9]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.0, yanchor="bottom"),
                      margin=dict(l=90, r=30, t=120, b=90))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".su_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(3):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    for j, k in enumerate([0] * 3 + [1] * 3 + [2] * 5):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "sup_to_unsup.gif")], check=True)
    ims = [Image.open(k).convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i % 2 * (w + 16), i // 2 * (h + 16)))
    sheet.save(HERE / "sup_to_unsup_frames.png")
    shutil.rmtree(tmp)
