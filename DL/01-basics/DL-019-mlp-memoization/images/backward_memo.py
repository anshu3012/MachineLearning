"""Backpropagation with memoization on the Note's 3-3-2-1 network (weights from rng(0), x = (0.5, -1, 2), y = 1, as in
the Notebook). The backward pass visits each node once, stores dL/dO there, and every node and weight behind it
reuses the stored numbers. Last frame: the first-layer weight W^1_11 read off the stored dL/dO11.
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, GREY, RED = "#4C78A8", "#F58518", "#BBBBBB", "#E45756"
sizes = [3, 3, 2, 1]
rng = np.random.default_rng(0)
W = {l: rng.normal(0, 0.5, (sizes[l - 1], sizes[l])) for l in (1, 2, 3)}
x, y = np.array([0.5, -1.0, 2.0]), 1.0
sig = lambda z: 1 / (1 + np.exp(-z))
O = {0: x, 1: sig(W[1].T @ x)}
O[2] = sig(W[2].T @ O[1])
O[3] = W[3].T @ O[2]
slope = {1: O[1] * (1 - O[1]), 2: O[2] * (1 - O[2]), 3: np.ones(1)}
G = {3: np.array([-2 * (y - O[3][0])])}                 # stored dL/dO, one number per node
for l in (2, 1):
    G[l] = W[l + 1] @ (G[l + 1] * slope[l + 1])
gW111 = G[1][0] * slope[1][0] * x[0]
assert round(O[3][0], 3) == -0.194 and round(G[3][0], 3) == -2.387 and round(gW111, 4) == -0.0138

pos = {(l, j): (l, (sizes[l] - 1) / 2 - j) for l in range(4) for j in range(sizes[l])}
NAME = {0: "x", 1: "O₁", 2: "O₂", 3: "ŷ"}
STEPS = [(None, "Forward pass done: every output O is stored. Now go backwards from the loss."),
         (3, "Output: ∂L/∂ŷ = −2(y − ŷ), computed once and stored"),
         (2, "Layer 2: each node uses the stored ∂L/∂ŷ (no recomputing)"),
         (1, "Layer 1: each node sums the stored values of the two nodes it feeds"),
         ("w", "A first-layer weight: its node's stored value × slope × input")]


def frame(k):
    upto, title = STEPS[k]
    done = set() if upto is None else ({3, 2, 1} if upto == "w" else set(range(upto, 4)))
    fig = go.Figure()
    for l in (1, 2, 3):
        for i in range(sizes[l - 1]):
            for j in range(sizes[l]):
                active = (l in done and l - 1 in done) or (upto == l + 0 and False)
                hot = upto in (2, 1) and l == upto + 1                 # links used in this step
                col = ORANGE if hot else (BLUE if l - 1 in done and l in done else GREY)
                if upto == "w" and (l, i, j) == (1, 0, 0):
                    col = RED
                (x0, y0), (x1, y1) = pos[(l - 1, i)], pos[(l, j)]
                fig.add_scatter(x=[x0, x1], y=[y0, y1], mode="lines", showlegend=False, hoverinfo="skip",
                                line=dict(color=col, width=5 if col in (ORANGE, RED) else 2))
    for (l, j), (px, py) in pos.items():
        filled = l in done
        fig.add_scatter(x=[px], y=[py], mode="markers", showlegend=False, hoverinfo="skip",
                        marker=dict(size=58, color=ORANGE if filled else "white", line=dict(width=3, color=BLUE)))
        lab = f"{NAME[l]}{j + 1}" if l in (0,) else (NAME[l] if l == 3 else f"O{l}{j + 1}")
        fig.add_annotation(x=px, y=py, text=f"<b>{lab}</b>", showarrow=False, font=dict(size=17))
        if filled:
            fig.add_annotation(x=px, y=py - 0.33, text=f"∂L/∂O = {G[l][j]:.3f}", showarrow=False,
                               font=dict(size=16, color="#B35900"))
        else:
            val = x[j] if l == 0 else O[l][j]
            fig.add_annotation(x=px, y=py + 0.33, text=f"{val:.3f}", showarrow=False, font=dict(size=15, color=GREY))
    stored = sum(sizes[l] for l in done)
    extra = f"<br>Node values computed: {stored} (plain recursion needs 59 for all weights)" if upto else ""
    if upto == "w":
        extra = (f"<br>∂L/∂W¹₁₁ = {G[1][0]:.4f} × {slope[1][0]:.3f} × {x[0]:.1f} = <b>{gW111:.4f}</b>,"
                 " the same as the two-path sum of section 4.4")
    fig.update_layout(template="simple_white", width=1100, height=720, font=FONT,
                      title=dict(text=title + extra, x=0.5, y=0.95, font=dict(size=19)),
                      xaxis=dict(visible=False, range=[-0.4, 3.4]), yaxis=dict(visible=False, range=[-1.6, 1.5]),
                      margin=dict(l=10, r=10, t=110, b=10))
    for l, t in enumerate(["input", "hidden layer 1", "hidden layer 2", "output"]):
        fig.add_annotation(x=l, y=-1.5, text=t, showarrow=False, font=dict(size=17, color="#555"))
    return fig


if __name__ == "__main__":
    print("dL/dO:", {l: G[l].round(4).tolist() for l in G}, "gW111", round(gW111, 5))
    tmp = HERE / ".bm_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(len(STEPS)):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [0] * 3 + [1] * 3 + [2] * 3 + [3] * 3 + [4] * 6
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "backward_memo.gif")], check=True)
    shutil.copy(keys[4], HERE / "backward_memo_frames.png")     # the final frame: readable in the PDF
    shutil.rmtree(tmp)
