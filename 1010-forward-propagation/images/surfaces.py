"""The forward pass for every input at once (Plotly 3-D frames). The Note's 4-3-2-1 network with its hand-set weights;
CGPA and IQ (both scaled to 0..1) sweep a grid, 10th and 12th marks stay at the student's 0.69 and 0.81.
One frame per node: the three layer-1 outputs, the two layer-2 outputs, then the prediction. The student's point is marked.
Run: python surfaces.py -> surfaces.gif, surfaces_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED = "#4C78A8", "#F58518", "#54A24B", "#E45756"
A0 = np.array([0.72, 0.72, 0.69, 0.81])
W = [np.array([[0.2, -0.3, 0.5], [0.4, 0.1, -0.2], [-0.5, 0.2, 0.1], [0.3, -0.4, 0.2]]),
     np.array([[0.6, -0.4], [-0.2, 0.5], [0.3, 0.7]]), np.array([[0.8], [-0.6]])]
B = [np.array([0.1, -0.1, 0.2]), np.array([0.1, -0.2]), np.array([0.2])]
sig = lambda z: 1 / (1 + np.exp(-z))


def forward(X):
    """Activations of every layer for the rows of X."""
    acts = []
    for w, b in zip(W, B):
        X = sig(X @ w + b)
        acts.append(X)
    return acts


g = np.linspace(0, 1, 41)
G1, G2 = np.meshgrid(g, g)
grid = np.c_[G1.ravel(), G2.ravel(), np.full(G1.size, A0[2]), np.full(G1.size, A0[3])]
acts, one = forward(grid), forward(A0[None])
assert np.allclose(np.round(one[0][0], 3), [0.606, 0.394, 0.656]) and round(float(one[2][0, 0]), 3) == 0.594   # the Note's numbers
PANELS = [(0, 0, "layer 1, node 1", BLUE), (0, 1, "layer 1, node 2", BLUE), (0, 2, "layer 1, node 3", BLUE),
          (1, 0, "layer 2, node 1", ORANGE), (1, 1, "layer 2, node 2", ORANGE), (2, 0, "output: probability of placement", GREEN)]
LO, HI = min(a.min() for a in acts), max(a.max() for a in acts)


def frame(k):
    layer, node, name, col = PANELS[k]
    Z = acts[layer][:, node].reshape(G1.shape)
    v = float(one[layer][0, node])
    pad = 0.25 * (Z.max() - Z.min())                     # each node keeps its own height scale, so its shape shows
    fig = go.Figure(go.Surface(x=G1, y=G2, z=Z, colorscale=[[0, "white"], [1, col]], showscale=False, opacity=0.9))
    fig.add_trace(go.Scatter3d(x=[A0[0]], y=[A0[1]], z=[v], mode="markers+text", marker=dict(size=7, color=RED),
                               text=[f"student: {v:.3f}"], textposition="top center", textfont=dict(size=28, color=RED)))
    fig.update_layout(width=900, height=700, font=dict(family="Latin Modern Roman", size=18), showlegend=False,
                      title=dict(text=f"{name}<br><sup>its output for every CGPA and IQ</sup>", x=0.5, font=dict(size=30)),
                      margin=dict(l=0, r=0, t=90, b=0),
                      scene=dict(xaxis=dict(title="CGPA / 10"), yaxis=dict(title="IQ / 100"),
                                 zaxis=dict(title="output", range=[Z.min() - pad, Z.max() + pad], nticks=5),
                                 camera=dict(eye=dict(x=-1.5, y=-1.7, z=0.9)), aspectmode="cube"))
    return fig


if __name__ == "__main__":
    print("output range over the grid:", acts[2].min().round(3), acts[2].max().round(3), " all layers:", LO.round(3), HI.round(3))
    tmp = HERE / ".surf_frames"
    tmp.mkdir(exist_ok=True)
    i = 0
    for k in range(len(PANELS)):
        frame(k).write_image(tmp / f"k{k}.png")
        for _ in range(3 if k < 5 else 7):                           # hold each surface, longest on the output
            shutil.copy(tmp / f"k{k}.png", tmp / f"{i:03d}.png")
            i += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", str(HERE / "surfaces.gif")], check=True)
    ims = [Image.open(tmp / f"k{k}.png").convert("RGB") for k in range(6)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (3 * w + 32, 2 * h + 16), "white")
    for j, im in enumerate(ims):
        sheet.paste(im, ((j % 3) * (w + 16), (j // 3) * (h + 16)))
    sheet.save(HERE / "surfaces_frames.png")
    shutil.rmtree(tmp)
