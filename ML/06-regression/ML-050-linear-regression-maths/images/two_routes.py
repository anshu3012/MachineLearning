"""Two routes to the best line on the 160 training students. Closed form (OLS): one formula lands straight on
m = 0.558, b = -0.896. Non-closed form (gradient descent from m = 0, b = 0, learning rate 0.018 on the mean squared
error): many small steps downhill on the contour map of E(m, b). Left: the line on the data; right: the route.
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import B, M, X_train, y_train
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

HERE = Path(__file__).parent
x, y = X_train["cgpa"].to_numpy(), y_train.to_numpy()
n = len(x)
E = lambda m, b: float(((y - m * x - b) ** 2).sum())

# Gradient descent on the mean squared error E / n, until m and b are within 0.001 and 0.01 of the OLS values.
m, b, LR, path = 0.0, 0.0, 0.018, [(0.0, 0.0)]
while not (abs(m - M) < 1e-3 and abs(b - B) < 1e-2):
    r = y - m * x - b
    m, b = m + LR * 2 * (r * x).mean(), b + LR * 2 * r.mean()
    path.append((m, b))
STEPS = len(path) - 1
assert STEPS == 6112, STEPS                                    # the step count quoted in the Note
path = np.array(path)

ms, bs = np.linspace(-0.05, 0.85, 160), np.linspace(-1.7, 0.4, 160)
Z = np.log10([[E(mm, bb) for mm in ms] for bb in bs])


def frame(k, ols=False):
    fig = make_subplots(1, 2, horizontal_spacing=0.11,
                        subplot_titles=["the line on the data", "the route on the error map E(m, b)"])
    fig.update_annotations(font_size=22)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=6, color=GREY, opacity=0.6)), 1, 1)
    xs = np.array([4, 10])
    fig.add_trace(go.Contour(x=ms, y=bs, z=Z, colorscale="Blues", reversescale=True, showscale=False, opacity=0.6,
                             contours=dict(size=0.12), line=dict(width=0.5)), 1, 2)
    fig.add_trace(go.Scatter(x=[M], y=[B], mode="markers", marker=dict(symbol="x", size=18, color="black")), 1, 2)
    if ols:
        fig.add_trace(go.Scatter(x=xs, y=M * xs + B, mode="lines", line=dict(color=ORANGE, width=5)), 1, 1)
        fig.add_annotation(x=M, y=B, ax=0, ay=0, axref="x2", ayref="y2", xref="x2", yref="y2", showarrow=True,
                           arrowhead=3, arrowsize=1.6, arrowwidth=4, arrowcolor=ORANGE)
        title = "closed form (OLS): one formula, one jump to the best line"
    else:
        mk, bk = path[k]
        fig.add_trace(go.Scatter(x=xs, y=M * xs + B, mode="lines", line=dict(color="black", width=2, dash="dash")), 1, 1)
        fig.add_trace(go.Scatter(x=xs, y=mk * xs + bk, mode="lines", line=dict(color=BLUE, width=5)), 1, 1)
        fig.add_trace(go.Scatter(x=path[:k + 1, 0], y=path[:k + 1, 1], mode="lines+markers",
                                 line=dict(color=BLUE, width=2), marker=dict(size=5, color=BLUE)), 1, 2)
        fig.add_trace(go.Scatter(x=[mk], y=[bk], mode="markers",
                                 marker=dict(size=16, color=BLUE, line=dict(color="white", width=2))), 1, 2)
        title = f"gradient descent: step {k:,} of {STEPS:,}"
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=12, color=GREY, symbol="square")), 1, 2)
    fig.add_annotation(x=0, y=0, xref="x2", yref="y2", text="start", showarrow=False, yshift=22, font=dict(size=20))
    fig.add_annotation(x=0.5, y=1.2, xref="paper", yref="paper", showarrow=False, font=dict(size=28), text=title)
    fig.update_xaxes(title="CGPA", range=[4, 10], row=1, col=1)
    fig.update_yaxes(title="package", range=[-0.5, 6.5], row=1, col=1)
    fig.update_xaxes(title="m (slope)", range=[-0.05, 0.85], row=1, col=2)
    fig.update_yaxes(title="b (intercept)", range=[-1.7, 0.4], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=600, showlegend=False, font=FONT,
                      margin=dict(l=70, r=30, t=130, b=70))
    return fig


if __name__ == "__main__":
    ks = [0, 1, 2, 3, 5, 8, 13, 20, 35, 60, 100, 200, 400, 800, 1500, 3000, STEPS]
    figs = [frame(0, ols=True)] + [frame(k) for k in ks]
    make_gif(figs, HERE / "two_routes", fps=3, holds=[8] + [2] * (len(ks) - 1) + [10], keys=[0, 3, 11, len(figs) - 1],
             width=900)
