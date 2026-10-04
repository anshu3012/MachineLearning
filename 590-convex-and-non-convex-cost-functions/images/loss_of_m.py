"""The loss is a function of the parameters (Plotly frames -> GIF). The data stays fixed: the Note's 21 points
x = -2, -1.8, ..., 2 with y = 1.5 tanh(2x). Only the slope m of the line y = m x (b = 0) changes, from -1 to 3.
Left: the line on the data, with its errors. Right: the mean squared error as a function of m, a curve whose lowest
point is m = 1.02, loss 0.18."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
xs = np.linspace(-2, 2, 21)
ys = 1.5 * np.tanh(2 * xs)
L = lambda m: float(np.mean((ys - m * xs) ** 2))
grid = np.linspace(-1, 3, 401)
best = grid[np.argmin([L(m) for m in grid])]
assert round(best, 2) == 1.02 and round(L(best), 2) == 0.18 and round(L(-1), 2) == 6.18 and round(L(3), 2) == 5.91
MS = list(np.round(np.linspace(-1, 3, 21), 2)) + [round(best, 2)]


def frame(m):
    fig = make_subplots(1, 2, horizontal_spacing=0.12,
                        subplot_titles=[f"the model y = {m:.2f} x on the fixed data", "the loss as a function of m"])
    fig.update_annotations(font_size=22)
    sx, sy = [], []
    for x, y in zip(xs, ys):
        sx += [x, x, None]; sy += [y, m * x, None]
    fig.add_trace(go.Scatter(x=sx, y=sy, mode="lines", line=dict(color=RED, width=2)), 1, 1)
    fig.add_trace(go.Scatter(x=[-2.2, 2.2], y=[-2.2 * m, 2.2 * m], mode="lines", line=dict(color=ORANGE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers", marker=dict(size=9, color=GREY)), 1, 1)
    fig.add_trace(go.Scatter(x=grid, y=[L(g) for g in grid], mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
    fig.add_trace(go.Scatter(x=[m], y=[L(m)], mode="markers+text", text=[f"loss {L(m):.2f}"], textposition="top right" if m < 0 else ("top left" if m > 2 else "top center"),
                             textfont=dict(size=20, color=ORANGE), marker=dict(size=16, color=ORANGE)), 1, 2)
    fig.update_xaxes(title="x", range=[-2.2, 2.2], row=1, col=1)
    fig.update_yaxes(title="y", range=[-4, 4], row=1, col=1)
    fig.update_xaxes(title="slope m (the parameter)", range=[-1.1, 3.1], row=1, col=2)
    fig.update_yaxes(title="mean squared error", range=[0, 7.2], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=540, font=FONT, showlegend=False,
                      margin=dict(l=70, r=30, t=60, b=70))
    return fig


if __name__ == "__main__":
    make_gif([frame(m) for m in MS], here / "loss_of_m", fps=4, holds=[3] + [1] * (len(MS) - 2) + [8],
             keys=[0, len(MS) - 1], cols=1)
