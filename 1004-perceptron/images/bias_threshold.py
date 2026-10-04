"""The bias as a threshold: the trained perceptron of section 8 on standardized inputs has z = 5.82 x1 + 1.48 x2 + b
with b = 1. Keeping the weights, we sweep b. Left: the step output against the weighted sum s = 5.82 x1 + 1.48 x2;
the jump sits at s = -b. Right: the same change on the input plane; the line z = 0 moves parallel to itself.
Plotly frames (data and a line changing) -> ffmpeg GIF, plus one key frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
S = W1 * Z[:, 0] + W2 * Z[:, 1]                      # the weighted sum, before the bias
SWEEP = [4, 2, 1, 0, -2, -4]
xs = np.linspace(-2.6, 2.6, 2)


def frame(b):
    fires = (S + b) >= 0
    acc = 100 * (fires == y).mean()
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.12,
                        subplot_titles=["<b>Step output against the weighted sum</b>", "<b>The line z = 0</b>"])
    fig.add_scatter(x=[-16, -b, -b, 16], y=[0, 0, 1, 1], mode="lines", line=dict(color=BLUE, width=5),
                    showlegend=False, row=1, col=1)
    for lab, c, name in ((1, GREEN, "placed"), (0, RED, "not placed")):
        m = y == lab
        fig.add_scatter(x=S[m], y=fires[m].astype(int), mode="markers", marker=dict(size=11, color=c, opacity=0.7),
                        showlegend=False, row=1, col=1)
        fig.add_scatter(x=Z[m, 0], y=Z[m, 1], mode="markers", name=name, marker=dict(size=10, color=c), row=1, col=2)
    fig.add_vline(x=-b, line=dict(color="black", dash="dot", width=2), row=1, col=1)
    fig.add_annotation(x=-b, y=0.5, text="threshold " + str(-b).replace("-", "−"), showarrow=False, xshift=-75 if b < 0 else 75,
                       font=dict(size=22), row=1, col=1)
    fig.add_scatter(x=xs, y=-(W1 * xs + b) / W2, mode="lines", line=dict(color=BLUE, width=5), name="z = 0",
                    row=1, col=2)
    note = " (the trained value)" if b == 1 else ""
    fig.update_layout(template="simple_white", width=1300, height=720, font=FONT,
                      title=dict(text=f"bias b = <b>{str(b).replace("-", "−")}</b>{note}: the perceptron outputs 1 when the weighted sum is "
                                      f"at least {str(-b).replace("-", "−")}<br>it outputs 1 for {fires.sum()} of 100 students; "
                                      f"training accuracy {acc:.0f}%", x=0.5, y=0.96, font=dict(size=23)),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.17),
                      margin=dict(l=80, r=30, t=150, b=120))
    fig.update_xaxes(title="weighted sum 5.82·x₁ + 1.48·x₂", range=[-16, 16], row=1, col=1)
    fig.update_yaxes(title="output", tickvals=[0, 1], range=[-0.2, 1.2], row=1, col=1)
    fig.update_xaxes(title="x₁: CGPA (standardized)", range=[-2.6, 2.6], row=1, col=2)
    fig.update_yaxes(title="x₂: resume score (standardized)", range=[-2.6, 2.6], row=1, col=2)
    fig.update_annotations(font=dict(size=22))
    return fig, int(fires.sum()), acc


if __name__ == "__main__":
    tmp = HERE / ".bt_frames"
    tmp.mkdir(exist_ok=True)
    keys, out = [], {}
    for b in SWEEP:
        keys.append(tmp / f"b{b}.png")
        fig, n, a = frame(b)
        out[b] = (n, round(a))
        fig.write_image(keys[-1])
    print(out)
    assert out[1][1] == 97
    seq = [i for i in range(len(SWEEP)) for _ in range(4)] + [2] * 6
    for j, i in enumerate(seq):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "bias_threshold.gif")], check=True)
    shutil.copy(keys[5], HERE / "bias_threshold_frames.png")          # one key frame for the PDF
    shutil.rmtree(tmp)
