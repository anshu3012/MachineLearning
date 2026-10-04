"""Where gradient descent ends depends on where it starts (Plotly frames). All six weights of the Note's 2-2-1
regression network are tied to one value a, biases 0. For student 1 the prediction is 2 a (16 a) = 32 a^2, so the
loss (4 - 32 a^2)^2 has two valleys, at a = -0.354 and a = +0.354, with a hilltop at a = 0 between them.
Three balls start at -0.55, 0 and 0.5 and follow the same update rule (learning rate 0.0003).
Run: python two_valleys.py -> two_valleys.gif, two_valleys_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, GREY, save_gif

HERE = Path(__file__).parent
L = lambda a: (4 - 32 * a ** 2) ** 2
dL = lambda a: -128 * a * (4 - 32 * a ** 2)
x, W = np.array([8.0, 8.0]), lambda a: (np.full((2, 2), a), np.full(2, a))
assert np.isclose(W(0.3)[1] @ (W(0.3)[0].T @ x), 32 * 0.3 ** 2)            # the tied network really predicts 32 a^2
STARTS, LR, STEPS = [-0.55, 0.0, 0.5], 0.0003, 40
paths = np.array([STARTS])
for _ in range(STEPS):
    paths = np.vstack([paths, paths[-1] - LR * dL(paths[-1])])
MIN = np.sqrt(1 / 8)
assert np.allclose(paths[-1], [-MIN, 0, MIN], atol=0.01)                  # left valley, stuck on the hilltop, right valley
grid = np.linspace(-0.62, 0.62, 400)


def frame(k):
    fig = go.Figure(go.Scatter(x=grid, y=L(grid), mode="lines", line=dict(color=GREY, width=4), showlegend=False))
    for j, (c, name) in enumerate(((BLUE, "start −0.55"), (GREEN, "start 0"), (ORANGE, "start 0.5"))):
        fig.add_trace(go.Scatter(x=paths[:k + 1, j], y=L(paths[:k + 1, j]), mode="lines", line=dict(color=c, width=2), showlegend=False))
        fig.add_trace(go.Scatter(x=[paths[k, j]], y=[L(paths[k, j])], mode="markers", marker=dict(color=c, size=20),
                                 name=f"{name}: now at {paths[k, j]:.3f}".replace("-", "−")))
    fig.update_layout(template="simple_white", width=1000, height=620, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"update {k}", x=0.5), xaxis=dict(title="a, the value shared by all six weights"),
                      yaxis=dict(title="loss of student 1", range=[-2, 75]), legend=dict(x=0.5, xanchor="center", y=0.98),
                      margin=dict(l=80, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    ks = list(range(0, 16)) + list(range(18, STEPS + 1, 4))
    save_gif([frame(k) for k in ks], "two_valleys", [0, 3, 8, len(ks) - 1], HERE, fps=3, hold=6)
    print(paths[[0, 1, 5, STEPS]].round(3))
