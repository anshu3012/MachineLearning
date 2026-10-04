"""Section 8.3 with every number: three words with invented 2-number embeddings and the matrices W_Q, W_K, W_V of
section 8.1. One operation per frame: X -> Q, K, V -> scores QK^T -> row softmax -> Y = weights x V.
The numbers are computed here with NumPy and asserted against the values quoted in the Note.
Idea of a full numeric walk-through after StatQuest, "The matrix math behind transformer neural networks, one
step at a time!!!"; our own numbers. Tool: Plotly frames (tables filling in). -> GIF + key-frame grid."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import save_gif

HERE = Path(__file__).parent
BLUE, GREEN, PURPLE, ORANGE, GREY = "#4C78A8", "#54A24B", "#B279A2", "#F58518", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
WORDS = ["money", "bank", "grows"]
X = np.array([[1, 2], [2, 0], [0, 1]], float)
WQ, WK, WV = np.array([[1, 0], [1, 1]], float), np.array([[0, 1], [1, 0]], float), np.array([[2, 0], [0, 0.5]])
Q, K, V = X @ WQ, X @ WK, X @ WV
S = Q @ K.T
W = np.exp(S) / np.exp(S).sum(1, keepdims=True)
Y = W @ V
assert Q.tolist() == [[3, 2], [2, 0], [1, 1]] and K.tolist() == [[2, 1], [0, 2], [1, 0]]
assert V.tolist() == [[2, 1], [4, 0], [0, 0.5]] and S.tolist() == [[8, 4, 3], [4, 0, 2], [3, 2, 1]]
assert np.allclose(W.round(3), [[0.976, 0.018, 0.007], [0.867, 0.016, 0.117], [0.665, 0.245, 0.090]])
assert np.allclose(Y.round(2), [[2.02, 0.98], [1.80, 0.93], [2.31, 0.71]])


def mat(fig, x0, y0, M, title, colour, fmt="{:g}", rows=None, cols=None, shade=False):
    """Draw matrix M with its top-left corner at (x0, y0); one unit per cell."""
    n, m = M.shape
    for i in range(n):
        for j in range(m):
            fill = f"rgba(76,120,168,{0.08 + 0.8 * M[i, j]:.2f})" if shade else "white"
            fig.add_shape(type="rect", x0=x0 + j, x1=x0 + j + 1, y0=y0 - i - 1, y1=y0 - i, opacity=1,
                          line=dict(color=colour, width=2), fillcolor=fill)
            fig.add_annotation(x=x0 + j + 0.5, y=y0 - i - 0.5, text=fmt.format(M[i, j]), showarrow=False,
                               font=dict(size=19, color="white" if shade and M[i, j] > 0.6 else "black"))
        if rows:
            fig.add_annotation(x=x0 - 0.15, y=y0 - i - 0.5, text=rows[i], showarrow=False, xanchor="right",
                               font=dict(size=18, color=GREY))
    if cols:
        for j in range(m):
            fig.add_annotation(x=x0 + j + 0.5, y=y0 - n - 0.35, text=cols[j], showarrow=False, font=dict(size=16, color=GREY))
    fig.add_annotation(x=x0 + m / 2, y=y0 + 0.5, text=title, showarrow=False, font=dict(size=21, color=colour))


TITLES = ["<b>X</b>: one row per word, 2 numbers each",
          "<b>Q = XW<sub>Q</sub>, K = XW<sub>K</sub>, V = XW<sub>V</sub></b>: three vectors per word",
          "<b>scores QK<sup>T</sup></b>: every query (row) with every key (column)",
          "<b>softmax on each row</b>: the weights of a row sum to 1",
          "<b>Y = weights × V</b>: each word's new vector"]


def frame(k):
    fig = go.Figure()
    mat(fig, 2.2, 8.2, X, "X", "black", rows=WORDS)
    if k >= 1:
        mat(fig, 6, 11.6, Q, "Q (queries)", GREEN)
        mat(fig, 6, 7.6, K, "K (keys)", PURPLE)
        mat(fig, 6, 3.6, V, "V (values)", BLUE)
    if k >= 2:
        mat(fig, 11.2, 9.6, S, "scores QK<sup>T</sup>", ORANGE, rows=WORDS, cols=WORDS)
    if k >= 3:
        mat(fig, 16.6, 9.6, W, "weights", BLUE, fmt="{:.2f}", cols=WORDS, shade=True)
    if k >= 4:
        mat(fig, 16.9, 3.6, Y, "Y (new vectors)", "black", fmt="{:.2f}", rows=WORDS)
    fig.update_layout(template="simple_white", width=1100, height=700, font=FONT, showlegend=False,
                      title=dict(text=TITLES[k], x=0.5, y=0.96),
                      xaxis=dict(visible=False, range=[0, 20.2]), yaxis=dict(visible=False, range=[-0.2, 12.6]),
                      margin=dict(l=10, r=10, t=60, b=10))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(5)], "matrix_walk", HERE, keys=[1, 2, 3, 4], fps=0.5, cols=2, holds=[1, 1, 1, 1, 4],
             width=820)
