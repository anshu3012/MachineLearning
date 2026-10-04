"""How hidden neurons shape the decision boundary: one hidden ReLU layer with 1, 10, 50 and 1,000 neurons on the
Note's 100 moon points. Each neuron's hyperplane (where its input w.x + b is 0) is a dashed line; the decision
boundary (black) is straight between them and bends only where it crosses one. Data: data/neuron_lines.csv
(weights of the four trained networks, i = -1 is the output bias) and data/points.csv, from the Notebook.
Plotly frames -> ffmpeg GIF, plus a grid of the four key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, ORANGE, GREY

HERE = Path(__file__).parent
D = HERE.parent / "data"
L, P = pd.read_csv(D / "neuron_lines.csv"), pd.read_csv(D / "points.csv")
POCKETS = pd.read_csv(D / "pocket_points.csv")
FONT = dict(family="Latin Modern Roman", size=22)
X0, X1, Y0, Y1 = -2, 3, -1.75, 2.25
xx, yy = np.meshgrid(np.linspace(X0, X1, 501), np.linspace(Y0, Y1, 401))
GRID = np.c_[xx.ravel(), yy.ravel()]


def network(n):
    m = L[(L.n == n) & (L.i >= 0)]
    W, b, v = m[["w1", "w2"]].values.T, m.b.values, m.v.values
    c = L[(L.n == n) & (L.i == -1)].b.values[0]
    return W, b, v, c


def segments(n):
    """Count the straight segments of the decision boundary: one per pattern of active neurons along it."""
    W, b, v, c = network(n)
    H = GRID @ W + b
    s = ((np.maximum(H, 0) @ v + c) > 0).reshape(xx.shape)
    A = (H > 0).reshape(xx.shape + (n,))
    edge = np.zeros_like(s)
    edge[:, 1:] |= s[:, 1:] != s[:, :-1]
    edge[1:, :] |= s[1:, :] != s[:-1, :]
    return len({A[r, q].tobytes() for r, q in zip(*np.nonzero(edge))})


def frame(n, show_lines=True):
    W, b, v, c = network(n)
    logit = (np.maximum(GRID @ W + b, 0) @ v + c).reshape(xx.shape)
    fig = go.Figure()
    fig.add_trace(go.Heatmap(x=xx[0], y=yy[:, 0], z=(logit > 0).astype(int), showscale=False, opacity=0.18,
                             colorscale=[[0, ORANGE], [1, BLUE]], hoverinfo="skip"))
    if show_lines and n <= 50:                                   # each neuron's hyperplane w1 x1 + w2 x2 + b = 0
        xs, ys = [], []
        for (w1, w2), bi in zip(W.T, b):
            if abs(w2) > abs(w1):
                xa = np.array([X0, X1]); ya = -(w1 * xa + bi) / w2
            else:
                ya = np.array([Y0, Y1]); xa = -(w2 * ya + bi) / w1
            xs += [*xa, None]; ys += [*ya, None]
        fig.add_scatter(x=xs, y=ys, mode="lines", line=dict(color=GREY, width=1.6, dash="dash"), opacity=0.9, name="a neuron's hyperplane", hoverinfo="skip")
    fig.add_trace(go.Contour(x=xx[0], y=yy[:, 0], z=logit, showscale=False, hoverinfo="skip",
                             contours=dict(start=0, end=0, size=1, coloring="lines"),
                             colorscale=[[0, "black"], [1, "black"]], line=dict(width=3.5), name="decision boundary",
                             showlegend=True))
    for cls, col in ((0, ORANGE), (1, BLUE)):
        q = P[P.y == cls]
        fig.add_scatter(x=q.x1, y=q.x2, mode="markers", name=f"class {cls}",
                        marker=dict(color=col, size=11, line=dict(width=1.5, color="white")))
    if n == 1000:
        fig.add_scatter(x=POCKETS.x1, y=POCKETS.x2, mode="markers", name="caught by a small pocket",
                        marker=dict(symbol="circle-open", size=34, color="black", line=dict(width=3)))
    k = segments(n)
    word = "neuron" if n == 1 else "neurons"
    fig.update_layout(template="simple_white", width=1000, height=820, font=FONT,
                      title=dict(text=f"<b>{n:,} hidden {word}</b><br>{n:,} hyperplane{'s' if n > 1 else ''}"
                                      f"{' (not drawn)' if n > 50 else ''} · {k} straight segment{'s' if k > 1 else ''}", x=0.5, y=0.96),
                      xaxis=dict(range=[X0, X1], title="x1", showgrid=False),
                      yaxis=dict(range=[Y0, Y1], title="x2", showgrid=False, scaleanchor="x"),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12),
                      margin=dict(l=70, r=20, t=110, b=130))
    return fig, k


SEQ = [1] * 6 + [10] * 6 + [50] * 6 + [1000] * 10
if __name__ == "__main__":
    counts = pd.read_csv(D / "neuron_lines_summary.csv").set_index("n").straight_pieces.to_dict()
    tmp = HERE / ".nl_frames"
    tmp.mkdir(exist_ok=True)
    made = {}
    for n in (1, 10, 50, 1000):
        fig, k = frame(n)
        assert k == counts[n], (n, k, counts[n])          # same count as the Notebook measured
        made[n] = tmp / f"n{n}.png"
        fig.write_image(made[n])
    for j, n in enumerate(SEQ):
        shutil.copy(made[n], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "neuron_lines.gif")], check=True)
    keys = [Image.open(made[n]).convert("RGB") for n in (1, 10, 50, 1000)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "neuron_lines_frames.png")
    shutil.rmtree(tmp)
