"""Dead nodes through training, from data/dead_over_time.npz (experiments/dead_over_time.py: the Notebook's exact runs
of Figure 3). Share of nodes in each hidden layer whose z is negative on every training observation, against the
training time on a log scale (for the learning-rate-10 run, also after each batch of the first epoch).
Plotly frames -> ffmpeg GIF, plus the final frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import BLUE, GREEN, GREY, RED

HERE = Path(__file__).parent
D = np.load(HERE.parent / "data" / "dead_over_time.npz")
ep = np.arange(201, dtype=float)
ep[0] = 1 / 32                                          # "before training", drawn at the left edge
B = D["relu_lr10_batches"]
lr10_x = np.r_[1 / 32, np.arange(1, 17) / 16, np.arange(2, 201)]
lr10_y = np.r_[B, D["relu_lr10"][2:]]
RUNS = [("ReLU, learning rate 10", lr10_x, lr10_y, RED, "solid"),
        ("ReLU, bias −1", ep, D["relu_bias"], GREY, "solid"),
        ("Leaky ReLU, bias −1", ep, D["leaky_bias"], BLUE, "solid"),
        ("ELU, bias −1", ep, D["elu_bias"], GREEN, "solid"),
        ("ReLU, learning rate 0.1", ep, D["relu_lr01"], "black", "dot")]
assert np.allclose(D["relu_lr10"][-1], [0.40625, 0.6875]) and np.allclose(D["leaky_bias"][-1], [0.4375, 0.46875])
assert np.allclose(D["relu_bias"][0], D["relu_bias"][-1]) and np.allclose(B[8], [0.40625, 0.65625])
CUTS = [1 / 32, 1 / 16, 0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 200]


def frame(c):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=("Hidden layer 1", "Hidden layer 2"))
    for name, x, Y, col, dash in RUNS:
        m = x <= c + 1e-9
        for k in (0, 1):
            fig.add_scatter(x=x[m], y=100 * Y[m, k], mode="lines", name=name, showlegend=k == 0,
                            line=dict(color=col, width=4 if dash == "solid" else 3, dash=dash), row=1, col=k + 1)
    fig.update_xaxes(type="log", range=[np.log10(1 / 32), np.log10(220)], title_text="epochs of training (log scale)",
                     tickvals=[1 / 16, 0.25, 1, 10, 100, 200], ticktext=["1 batch", "¼", "1", "10", "100", "200"])
    fig.update_yaxes(range=[-3, 105])
    fig.update_yaxes(title_text="nodes negative on every observation (%)", row=1, col=1)
    when = "before training" if c < 1 / 16 else (f"after {int(round(c * 16))} of the 16 batches of epoch 1" if c < 1
                                                  else f"after {int(c)} epoch{'s' if c > 1 else ''}")
    fig.update_layout(template="simple_white", width=1300, height=640, font=dict(family="Latin Modern Roman", size=19),
                      title=dict(text=f"Dead nodes, {when}", x=0.5, y=0.96, font=dict(size=22)),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2, font=dict(size=17)),
                      margin=dict(l=90, r=30, t=90, b=150))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".dt_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for i, c in enumerate(CUTS):
        keys.append(tmp / f"k{i}.png")
        frame(c).write_image(keys[-1])
    seq = [i for i in range(len(CUTS)) for _ in range(2)] + [len(CUTS) - 1] * 5
    for j, i in enumerate(seq):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "dead_over_time.gif")], check=True)
    shutil.copy(keys[-1], HERE / "dead_over_time_frames.png")
    shutil.rmtree(tmp)
