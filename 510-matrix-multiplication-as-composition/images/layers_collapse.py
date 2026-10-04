"""Section 7.2: two linear layers W1 = M1, then W2 = M2, move a square of points exactly where the single matrix
M2 M1 moves it. The input [1, 1] goes to [-1, 1], then to [2, -1]; the one-step matrix sends it straight to [2, -1].
Run: python layers_collapse.py  -> layers_collapse.gif, layers_collapse_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
M1, M2 = np.array([[1, -2], [1, 0]]), np.array([[0, 2], [1, 0]])
P = M2 @ M1
x = np.array([1, 1])
assert (M1 @ x == [-1, 1]).all() and (M2 @ (M1 @ x) == [2, -1]).all() and (P @ x == [2, -1]).all()
assert (P == [[2, 0], [1, -2]]).all()                                         # the Note's numbers
g = np.linspace(0, 1, 6)
square = np.array([[a, b] for a in g for b in g])                             # a square of input points
outline = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])


def lerp(M, t):
    return (1 - t) * np.eye(2) + t * M


def frame(t1, t2, t3, caption):
    """t1, t2: progress of layer 1 then layer 2 (left panel); t3: progress of the single matrix (right panel)."""
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                        subplot_titles=["two layers: W1 = M1, then W2 = M2", "one layer: W2 W1"])
    left = lerp(M2, t2) @ lerp(M1, t1)
    right = lerp(P, t3)
    for c, M in [(1, left), (2, right)]:
        pts, out, xi = square @ M.T, outline @ M.T, M @ x
        fig.add_trace(go.Scatter(x=out[:, 0], y=out[:, 1], mode="lines", fill="toself", fillcolor="rgba(76,120,168,0.15)",
                                 line=dict(color=BLUE, width=3), showlegend=False), row=1, col=c)
        fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="markers", marker=dict(size=6, color=BLUE),
                                 showlegend=False), row=1, col=c)
        fig.add_trace(go.Scatter(x=[xi[0]], y=[xi[1]], mode="markers+text", marker=dict(size=14, color=ORANGE),
                                 text=[f"[{xi[0]:.1f}, {xi[1]:.1f}]"], textposition="top center",
                                 textfont=dict(size=20, color=ORANGE), showlegend=False), row=1, col=c)
        fig.update_xaxes(range=[-2.6, 2.8], dtick=1, showgrid=True, zeroline=True, row=1, col=c)
        fig.update_yaxes(range=[-2.6, 2.6], dtick=1, showgrid=True, zeroline=True, row=1, col=c,
                         scaleanchor="x" if c == 1 else "x2")
    fig.update_layout(template="simple_white", width=1100, height=600, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"<b>{caption}</b>", x=0.5, y=0.97), margin=dict(l=40, r=20, t=110, b=40))
    fig.update_annotations(font_size=21)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".collapse_frames"
    tmp.mkdir(exist_ok=True)
    ts = np.linspace(0, 1, 10)
    seq = [(0, 0, 0, "the same square of inputs; orange is [1, 1]")] * 4
    seq += [(t, 0, t / 2, "layer 1 (M1) acts on the left") for t in ts]
    seq += [(1, t, 0.5 + t / 2, "then layer 2 (M2)") for t in ts]
    seq += [(1, 1, 1, "same square, same point [2, -1]: two linear layers = one matrix")] * 12
    for k, s in enumerate(seq):
        frame(*s).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "layers_collapse.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (3, 13, 22, len(seq) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "layers_collapse_frames.png")
    shutil.rmtree(tmp)
