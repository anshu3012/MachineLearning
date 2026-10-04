"""Why an overfit model fails: training error and new-data error as the model gets more complex. Data: the same 12
training points and 300 new points as fitting.py (a sine wave plus noise, seed 31). A polynomial of degree 1 to 11 is
fitted to the 12 points. Left: the fitted curve, the training points and 12 of the new points, with a segment from each
new point to the curve (its error). Right: the error (root mean squared) on the training points and on all 300 new
points, drawn degree by degree. Idea after StatQuest, "Machine Learning Fundamentals: Bias and Variance" (compare the
fits on the training set and on the testing set). Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=24)
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"

rng = np.random.default_rng(31)                       # identical draws to fitting.py
truth = lambda x: np.sin(2 * np.pi * x)
x_train = np.sort(rng.uniform(0, 1, 12))
y_train = truth(x_train) + rng.normal(0, 0.25, x_train.size)
LO, HI = x_train.min(), x_train.max()
x_new = rng.uniform(LO, HI, 300)
y_new = truth(x_new) + rng.normal(0, 0.25, x_new.size)
DEG = list(range(1, 12))
COEF = {d: np.polyfit(x_train, y_train, d) for d in DEG}
rmse = lambda c, x, y: float(np.sqrt(np.mean((np.polyval(c, x) - y) ** 2)))
TRAIN = [rmse(COEF[d], x_train, y_train) for d in DEG]
NEW = [rmse(COEF[d], x_new, y_new) for d in DEG]
assert [round(v, 2) for v in (TRAIN[0], NEW[0], TRAIN[2], NEW[2], TRAIN[10], NEW[10])] == [0.47, 0.55, 0.21, 0.32, 0.0, 0.67]
SHOWN = np.argsort(x_new)[::25]                       # 12 of the new points, spread over the range


def frame(d):
    c = COEF[d]
    xs = np.linspace(LO, HI, 400)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.12)
    for i in SHOWN:
        fig.add_scatter(x=[x_new[i]] * 2, y=[y_new[i], float(np.clip(np.polyval(c, x_new[i]), -2, 2))], mode="lines",
                        line=dict(color=ORANGE, width=2), row=1, col=1)
    fig.add_scatter(x=xs, y=np.clip(np.polyval(c, xs), -2, 2), mode="lines", line=dict(color="black", width=4), row=1, col=1)
    fig.add_scatter(x=x_new[SHOWN], y=y_new[SHOWN], mode="markers", row=1, col=1,
                    marker=dict(size=11, color=ORANGE, symbol="diamond"))
    fig.add_scatter(x=x_train, y=y_train, mode="markers", marker=dict(size=13, color=BLUE), row=1, col=1)
    k = DEG.index(d) + 1
    for vals, col, name in [(TRAIN, BLUE, "training data"), (NEW, ORANGE, "new data")]:
        fig.add_scatter(x=DEG[:k], y=vals[:k], mode="lines+markers", line=dict(color=col, width=4), marker=dict(size=11),
                        row=1, col=2)
        fig.add_annotation(x=DEG[k - 1], y=vals[k - 1], xref="x2", yref="y2", text=f"<b>{vals[k - 1]:.2f}</b>",
                           showarrow=False, yshift=22 if name == "new data" or vals[k - 1] < 0.08 else -22, font=dict(color=col, size=24))
    fig.add_annotation(x=0.02, y=1.0, xref="x2 domain", yref="y2 domain", xanchor="left", showarrow=False, align="left",
                       text=f"<span style='color:{ORANGE}'>◆ error on new data</span><br>"
                            f"<span style='color:{BLUE}'>● error on training data</span>", font=dict(size=22))
    fig.update_xaxes(title="input", range=[0, 1], showticklabels=False, row=1, col=1)
    fig.update_yaxes(title="output", range=[-2.1, 2.1], showticklabels=False, row=1, col=1)
    fig.update_xaxes(title="model complexity (polynomial degree)", range=[0.5, 11.5], dtick=1, row=1, col=2)
    fig.update_yaxes(title="error", range=[0, 1.0], row=1, col=2)
    fig.update_layout(template="simple_white", width=1300, height=700, font=FONT, showlegend=False,
                      title=dict(text=f"<b>Degree {d}</b>: training error {TRAIN[k - 1]:.2f}, new-data error {NEW[k - 1]:.2f}",
                                 x=0.5, y=0.95, font=dict(size=30)),
                      margin=dict(l=70, r=30, t=100, b=90))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".tt_frames"
    tmp.mkdir(exist_ok=True)
    keys = {}
    for d in DEG:
        keys[d] = tmp / f"k{d}.png"
        frame(d).write_image(keys[d])
    for j, d in enumerate([d for d in DEG for _ in range(2)] + [11] * 6):
        shutil.copy(keys[d], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=860:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "train_test_error.gif")], check=True)
    ims = [Image.open(keys[d]).convert("RGB") for d in (3, 11)]      # the same two fits as fitting.py
    w, h = ims[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "train_test_error_frames.png")
    shutil.rmtree(tmp)
