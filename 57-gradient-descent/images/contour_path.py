"""Gradient descent on m and b together (100-point data): the path on the contour map of the loss, and the loss per
epoch (Plotly). Start m = -127.82, b = 150, learning rate 0.001, 30 epochs, as in the original example."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import x100, y100, BLUE, ORANGE, RED, GREEN, GREY, FONT

here = Path(__file__).parent
m, b, lr = -127.82, 150.0, 0.001
ms, bs, cost = [m], [b], [float(np.sum((y100 - m * x100 - b) ** 2))]
for _ in range(30):
    gb = -2 * np.sum(y100 - m * x100 - b)
    gm = -2 * np.sum((y100 - m * x100 - b) * x100)
    b, m = b - lr * gb, m - lr * gm
    ms.append(m); bs.append(b); cost.append(float(np.sum((y100 - m * x100 - b) ** 2)))
print("final m, b", round(m, 2), round(b, 2), "cost", round(cost[0]), "->", round(cost[-1]))
mg, bg = np.linspace(-150, 150, 120), np.linspace(-150, 170, 120)
Z = np.array([[np.sum((y100 - mm * x100 - bb) ** 2) for mm in mg] for bb in bg])
fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.12,
                    subplot_titles=("Path of (m, b) on the loss contours", "Loss after each epoch"))
fig.add_trace(go.Contour(x=mg, y=bg, z=Z, colorscale="Blues", reversescale=True, showscale=False, ncontours=25,
                         line=dict(width=0.5)), 1, 1)
fig.add_trace(go.Scatter(x=ms, y=bs, mode="lines+markers", line=dict(color=ORANGE, width=3),
                         marker=dict(size=6, color=ORANGE)), 1, 1)
fig.add_trace(go.Scatter(x=[ms[0]], y=[bs[0]], mode="markers+text", text=["start"], textposition="top right",
                         marker=dict(size=12, color=RED), textfont=dict(color=RED, size=15)), 1, 1)
fig.add_trace(go.Scatter(x=list(range(31)), y=cost, mode="lines+markers", line=dict(color=BLUE, width=3)), 1, 2)
fig.update_xaxes(title="m (slope)", row=1, col=1); fig.update_yaxes(title="b (intercept)", row=1, col=1)
fig.update_xaxes(title="epoch", row=1, col=2); fig.update_yaxes(title="loss", type="log", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=470, showlegend=False, font=FONT,
                  margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=16)
fig.write_image(here / "contour_path.png", scale=2)
fig.write_image(here / "contour_path.pdf")
