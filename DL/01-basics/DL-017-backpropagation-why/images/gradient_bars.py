"""The gradient as nine bars (Plotly frames). The 2-2-1 regression network of the Note is trained as in the
backpropagation Notes (all weights 0.1, biases 0, learning rate 0.001, one student at a time). Each frame shows the
nine partial derivatives of the mean loss over the four students at the start of an epoch: their signs, their very different sizes, and
how all of them shrink towards 0 as training converges.
Run: python gradient_bars.py -> gradient_bars.gif, gradient_bars_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, save_gif

HERE = Path(__file__).parent
X = np.array([[8, 8], [7, 9], [6, 10], [5, 12]], float)
Y = np.array([4, 5, 6, 7], float)
NAMES = ["W¹₁₁", "W¹₂₁", "W¹₁₂", "W¹₂₂", "b₁₁", "b₁₂", "W²₁₁", "W²₂₁", "b₂₁"]
COLS = [BLUE] * 4 + [GREEN] * 2 + [ORANGE] * 2 + [GREEN]


def grads(W1, b1, W2, b2, x, y):
    O = W1.T @ x + b1
    g = -2 * (y - (W2 @ O + b2))
    return np.outer(x, g * W2), g * W2, g * O, g


def mean_gradient(W1, b1, W2, b2):
    """The nine partial derivatives of the mean loss over the four students."""
    out = []
    for x, y in zip(X, Y):
        dW1, db1, dW2, db2 = grads(W1, b1, W2, b2, x, y)
        out.append(np.r_[dW1[0, 0], dW1[1, 0], dW1[0, 1], dW1[1, 1], db1, dW2, db2])
    return np.mean(out, axis=0)


W1, b1, W2, b2 = np.full((2, 2), 0.1), np.zeros(2), np.full(2, 0.1), 0.0
SHOW = [0, 1, 2, 3, 4, 5, 7, 10, 20, 50, 100, 300, 1000]
snaps = {}
for epoch in range(1001):
    if epoch in SHOW:
        snaps[epoch] = mean_gradient(W1, b1, W2, b2)
    for x, y in zip(X, Y):
        dW1, db1, dW2, db2 = grads(W1, b1, W2, b2, x, y)
        W1, b1, W2, b2 = W1 - 0.001 * dW1, b1 - 0.001 * db1, W2 - 0.001 * dW2, b2 - 0.001 * db2
g0 = snaps[0]
assert np.abs(snaps[1000]).max() < 0.1 * np.abs(g0).max()                                   # all shrink as training converges
LIM = np.abs(np.array(list(snaps.values()))).max() * 1.15


def frame(epoch):
    g = snaps[epoch]
    fig = go.Figure(go.Bar(x=NAMES, y=g, marker_color=COLS, text=[f"{v:.2f}".replace("-", "−") for v in g], textposition="outside",
                           textfont=dict(size=20)))
    fig.add_hline(y=0, line_color="black", line_width=1)
    fig.update_layout(template="simple_white", width=1000, height=600, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"the gradient of the mean loss after <b>{epoch}</b> epochs", x=0.5),
                      yaxis=dict(title="partial derivative of the loss", range=[-LIM, LIM]), margin=dict(l=90, r=20, t=80, b=60))
    return fig


if __name__ == "__main__":
    save_gif([frame(e) for e in SHOW], "gradient_bars", [0, SHOW.index(3), SHOW.index(10), len(SHOW) - 1], HERE, fps=1.5, hold=4)
    for e in (0, 3, 10, 1000):
        print(e, snaps[e].round(2))
