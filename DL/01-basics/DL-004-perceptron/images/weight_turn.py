"""Weights as feature importance, drawn: the trained perceptron of section 8 on standardized inputs has
z = 5.82 x1 + 1.48 x2 + 1 (x1 = CGPA, x2 = resume score). Keeping w1 and b, we sweep w2 from 0 to 8 and draw the line
z = 0 over the 100 students. With w2 = 0 only CGPA decides (a vertical line); as w2 grows, the resume score gets
more say and the line turns. Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.linear_model import Perceptron
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
GREEN, RED, BLUE = "#54A24B", "#E45756", "#4C78A8"
df = pd.read_csv(HERE.parent / "data" / "placement.csv")
X, y = df[["cgpa", "resume_score"]].values, df.placed.values
model = make_pipeline(StandardScaler(), Perceptron(random_state=0)).fit(X, y)
p = model[-1]
W1, W2, B = p.coef_[0][0], p.coef_[0][1], p.intercept_[0]
assert (round(W1, 2), round(W2, 2), B) == (5.82, 1.48, 1.0)
Z = model[0].transform(X)
SWEEP = [0, 0.5, 1.48, 3, 5.82, 8]
xs = np.linspace(-2.6, 2.6, 2)


def frame(w2):
    acc = 100 * (((W1 * Z[:, 0] + w2 * Z[:, 1] + B) >= 0) == y).mean()
    fig = go.Figure()
    for lab, c, name in ((1, GREEN, "placed"), (0, RED, "not placed")):
        m = y == lab
        fig.add_scatter(x=Z[m, 0], y=Z[m, 1], mode="markers", name=name, marker=dict(size=11, color=c))
    if w2 == 0:
        fig.add_scatter(x=[-B / W1] * 2, y=[-2.6, 2.6], mode="lines", line=dict(color=BLUE, width=5), name="z = 0")
    else:
        fig.add_scatter(x=xs, y=-(W1 * xs + B) / w2, mode="lines", line=dict(color=BLUE, width=5), name="z = 0")
    note = {0: "only CGPA counts", 1.48: "the trained value", 5.82: "both count equally"}.get(w2, "")
    fig.update_layout(template="simple_white", width=900, height=780, font=FONT,
                      title=dict(text=f"z = 5.82·x₁ + <b>{w2:g}</b>·x₂ + 1   {('(' + note + ')') if note else ''}"
                                      f"<br>training accuracy {acc:.0f}%", x=0.5, y=0.95, font=dict(size=22)),
                      xaxis=dict(title="x₁: CGPA (standardized)", range=[-2.6, 2.6]),
                      yaxis=dict(title="x₂: resume score (standardized)", range=[-2.6, 2.6], scaleanchor="x"),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.13),
                      margin=dict(l=80, r=30, t=110, b=130))
    return fig, acc


if __name__ == "__main__":
    tmp = HERE / ".wt_frames"
    tmp.mkdir(exist_ok=True)
    keys, accs = [], []
    for w2 in SWEEP:
        keys.append(tmp / f"w{w2}.png")
        fig, a = frame(w2)
        accs.append(a)
        fig.write_image(keys[-1])
    print(dict(zip(SWEEP, accs)))
    assert accs[SWEEP.index(1.48)] == 97
    seq = [i for i in range(len(SWEEP)) for _ in range(3)] + [2] * 4
    for j, i in enumerate(seq):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "weight_turn.gif")], check=True)
    ims = [Image.open(keys[i]).convert("RGB") for i in (0, 2, 4)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (3 * w + 32, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "weight_turn_frames.png")
    shutil.rmtree(tmp)
