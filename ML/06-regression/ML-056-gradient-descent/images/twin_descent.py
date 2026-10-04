"""Gradient descent on b seen from both sides, on the 4-point example (m fixed at 78.35, learning rate 0.1, start
b = 100). Left: the line and its four residuals. Right: the loss curve L(b), the tangent at the current b and an
arrow for the step. The steps shrink by themselves as the tangent flattens: 59.07, 11.81, 2.36, 0.47, 0.09.
Plotly frames -> GIF. Idea after StatQuest, "Gradient Descent, Step-by-Step"."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from common import M4, x4, y4, loss_b, slope_b, descend_b
from gifkit import make_gif, FONT, BLUE, ORANGE, GREEN, RED, GREY

here = Path(__file__).parent
LR = 0.1
bs = descend_b(100, LR, 5)
steps = [LR * slope_b(b) for b in bs[:-1]]
assert [round(b, 2) for b in bs] == [100, 40.93, 29.11, 26.75, 26.28, 26.18]
assert [round(s, 2) for s in steps] == [59.07, 11.81, 2.36, 0.47, 0.09]
grid = np.linspace(-5, 112, 200)
xs = np.array([x4.min() - 0.3, x4.max() + 0.3])


def frame(k):
    b, last = bs[k], k == len(bs) - 1
    g = slope_b(b)
    head = (f"after 5 steps: b = {b:.2f} (best b = 26.16); the steps shrank by themselves" if last else
            f"step {k + 1}:  b = {b:.2f},  slope = {g:.1f},  step = 0.1 × {g:.1f} = {LR * g:.2f}")
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                        subplot_titles=[f"the line  y = 78.35x + {b:.2f}  and its residuals", "the loss L(b)"])
    fig.add_scatter(x=xs, y=M4 * xs + b, mode="lines", line=dict(color=ORANGE, width=4), row=1, col=1)
    for xi, yi in zip(x4, y4):
        fig.add_scatter(x=[xi, xi], y=[yi, M4 * xi + b], mode="lines", line=dict(color=RED, width=4), row=1, col=1)
    fig.add_scatter(x=x4, y=y4, mode="markers", marker=dict(size=15, color=BLUE), row=1, col=1)
    fig.add_scatter(x=grid, y=[loss_b(v) for v in grid], mode="lines", line=dict(color=BLUE, width=4), row=1, col=2)
    fig.add_scatter(x=bs[:k], y=[loss_b(v) for v in bs[:k]], mode="markers", marker=dict(size=10, color=GREY), row=1, col=2)
    w = 14
    fig.add_scatter(x=[b - w, b + w], y=[loss_b(b) - w * g, loss_b(b) + w * g], mode="lines",
                    line=dict(color="black", width=3), row=1, col=2)
    fig.add_scatter(x=[b], y=[loss_b(b)], mode="markers", marker=dict(size=17, color=ORANGE), row=1, col=2)
    if not last:
        fig.add_annotation(x=bs[k + 1], y=2500, ax=b, ay=2500, xref="x2", yref="y2", axref="x2", ayref="y2", text="",
                           arrowhead=3, arrowwidth=4, arrowcolor=GREEN)
        fig.add_annotation(x=(b + bs[k + 1]) / 2, y=5200, text=f"step {LR * g:.2f}", showarrow=False,
                           font=dict(size=22, color=GREEN), row=1, col=2)
    fig.update_xaxes(title_text="x", row=1, col=1)
    fig.update_yaxes(title_text="y", range=[-90, 200], row=1, col=1)
    fig.update_xaxes(title_text="b (intercept)", range=[-8, 114], row=1, col=2)
    fig.update_yaxes(title_text="loss", range=[0, 40000], row=1, col=2)
    for a in fig.layout.annotations[:2]:
        a.font.size = 22
        a.y = 1.0
    fig.update_layout(template="simple_white", width=1300, height=640, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5, font=dict(size=25)), margin=dict(l=80, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    make_gif([frame(k) for k in range(6)], here / "twin_descent", fps=1, holds=[3, 3, 3, 2, 2, 6], keys=[0, 1, 2, 5],
             cols=2, width=900)
