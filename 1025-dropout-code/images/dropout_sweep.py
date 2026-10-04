"""Dropout rate sweep on the regression problem: the fitted curve for p = 0 to 0.8 (left, seed 0) and the training
and test MSE, mean of 5 seeds, traced as p grows (right). Data: data/sweep_curves.csv, data/sweep_scores.csv and
data/regression_points.csv from the Notebook. Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
from PIL import Image
from plotly.subplots import make_subplots
from common import BLUE, RED, GREY

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
pts = pd.read_csv(DATA / "regression_points.csv")
cur = pd.read_csv(DATA / "sweep_curves.csv")
sc = pd.read_csv(DATA / "sweep_scores.csv")
FONT = dict(family="Latin Modern Roman", size=22)
PS = list(sc.p)
best = sc.p[sc.test_mse.idxmin()]


def frame(p):
    d = sc[sc.p <= p + 1e-9]
    fig = make_subplots(1, 2, column_widths=[0.5, 0.5], horizontal_spacing=0.12)
    fig.add_scatter(x=pts.x, y=pts.y_train, mode="markers", name="training points", marker=dict(color="black", size=9),
                    row=1, col=1)
    fig.add_scatter(x=pts.x, y=pts.y_test, mode="markers", name="test points", marker=dict(color=RED, size=9),
                    row=1, col=1)
    fig.add_scatter(x=cur.x, y=cur[f"p={p:g}"], mode="lines", name="prediction", line=dict(color=BLUE, width=4),
                    row=1, col=1)
    fig.add_scatter(x=d.p, y=d.train_mse, mode="lines+markers", name="training MSE", line=dict(color=GREY, width=3),
                    marker=dict(size=10), row=1, col=2)
    fig.add_scatter(x=d.p, y=d.test_mse, mode="lines+markers", name="test MSE", line=dict(color=RED, width=3),
                    marker=dict(size=10), row=1, col=2)
    fig.update_xaxes(title="x", row=1, col=1)
    fig.update_yaxes(title="y", range=[-1.8, 1.8], row=1, col=1)
    fig.update_xaxes(title="dropout rate p", range=[-0.04, 0.84], dtick=0.2, row=1, col=2)
    fig.update_yaxes(title="MSE (mean of 5 seeds)", range=[0, 1.1 * sc[["train_mse", "test_mse"]].max().max()],
                     row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=560, font=FONT,
                      title=dict(text=f"dropout rate p = {p:g}", x=0.5),
                      legend=dict(orientation="h", x=0, y=-0.2), margin=dict(l=70, r=20, t=70, b=40))
    return fig


SEQ = [PS[0]] * 3 + [p for p in PS for _ in range(3)] + [PS[-1]] * 6
KEYS = [0.0, 0.2, best, PS[-1]]

if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    made = {}
    for k, p in enumerate(SEQ):
        out = tmp / f"{k:03d}.png"
        if p in made:
            shutil.copy(made[p], out)
        else:
            frame(p).write_image(out)
            made[p] = out
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "dropout_sweep.gif")], check=True)
    keys = [Image.open(made[k]).convert("RGB") for k in KEYS]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "dropout_sweep_frames.png")
    shutil.rmtree(tmp)
