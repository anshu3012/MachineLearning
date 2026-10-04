"""Symmetry through training, from data/twins.npz (experiments/twins.py): the weights from x1 into the 3 ReLU hidden
nodes, epoch by epoch. Left: every weight started at 0.5, so the three nodes get identical gradients and their three
lines are one. Right: Keras' random start, the three lines go their own ways.
Plotly frames -> ffmpeg GIF, plus the final frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
D = np.load(HERE.parent / "data" / "twins.npz")
Wc, Wr = D["Wc"], D["Wr"]
assert np.allclose(Wc[:, 0, 0], Wc[:, 0, 1]) and np.allclose(Wc[:, 0, 0], Wc[:, 0, 2])
assert round(float(Wc[-1, 0, 0]), 3) == 0.312 and round(float(Wc[-1, 1, 0]), 3) == -0.842
COL = ["#4C78A8", "#F58518", "#54A24B"]
DASH = ["solid", "dash", "dot"]
E = np.arange(101)
CUTS = [0, 1, 2, 5, 10, 20, 40, 70, 100]


def frame(c):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=(
        "Every weight started at 0.5: the 3 nodes stay twins", "Random start: the 3 nodes differ"))
    for col, W in ((1, Wc), (2, Wr)):
        for j in range(3):
            fig.add_scatter(x=E[:c + 1], y=W[:c + 1, 0, j], mode="lines", name=f"node {j + 1}", showlegend=col == 2,
                            line=dict(color=COL[j], width=5 - j, dash=DASH[j]), row=1, col=col)
    fig.update_xaxes(title_text="epoch", range=[0, 100])
    fig.update_yaxes(title_text="weight from input x₁", range=[-2.5, 1.4], row=1, col=1)
    fig.update_yaxes(range=[-2.5, 1.4], row=1, col=2)
    fig.update_layout(template="simple_white", width=1250, height=560, font=dict(family="Latin Modern Roman", size=19),
                      title=dict(text=f"Weights from input x₁ into the 3 hidden nodes, epoch {c}", x=0.5, y=0.96,
                                 font=dict(size=21)),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2),
                      margin=dict(l=90, r=30, t=100, b=120))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".tw_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for i, c in enumerate(CUTS):
        keys.append(tmp / f"k{i}.png")
        frame(c).write_image(keys[-1])
    seq = [i for i in range(len(CUTS)) for _ in range(2)] + [len(CUTS) - 1] * 5
    for j, i in enumerate(seq):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=880:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "twins.gif")], check=True)
    shutil.copy(keys[-1], HERE / "twins_frames.png")
    shutil.rmtree(tmp)
