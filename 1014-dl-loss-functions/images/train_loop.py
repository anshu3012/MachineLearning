"""Section 3: gradient descent moves a line and watches its MSE loss fall, on the 30 points of Figure 3 that follow
y = 2x + 1 (outliers left out). Start m = 0, b = 0; learning rate 0.01. Plotly frames -> train_loop.gif + _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, GREY, FONT, save_gif

here = Path(__file__).parent
d = np.load(here.parent / "data" / "outlier_fit.npz")
x, y = d["x"][~d["is_out"]], d["y"][~d["is_out"]]
assert len(x) == 30
m, b, lr, hist = 0.0, 0.0, 0.01, []
for step in range(501):
    e = y - (m * x + b)
    hist.append((m, b, np.mean(e ** 2)))
    m, b = m + lr * 2 * np.mean(e * x), b + lr * 2 * np.mean(e)
loss = np.array([h[2] for h in hist])
assert np.all(np.diff(loss) < 0)                    # every step lowers the loss
assert round(loss[0]) == 156 and round(loss[2], 2) == 1.45 and round(loss[500], 2) == 0.12   # the Note text
best = np.polyfit(x, y, 1)
assert loss[-1] < 1.05 * np.mean((y - np.polyval(best, x)) ** 2)   # ends at the least-squares line
SHOW = [0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 500]


def frame(k):
    m, b, L = hist[k]
    fig = make_subplots(rows=1, cols=2, subplot_titles=("the line", "its loss (MSE)"), horizontal_spacing=0.12)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(color=GREY, size=9), showlegend=False), 1, 1)
    xs = np.array([0, 10])
    fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color=BLUE, width=5), showlegend=False), 1, 1)
    steps = [s for s in SHOW if s <= k]
    fig.add_trace(go.Scatter(x=list(range(len(steps))), y=loss[steps], mode="lines+markers", line=dict(color=RED, width=4),
                             marker=dict(size=10), showlegend=False), 1, 2)
    fig.update_xaxes(title_text="x", range=[0, 10.3], row=1, col=1)
    fig.update_yaxes(title_text="y", range=[-1, 23], row=1, col=1)
    fig.update_xaxes(title_text="step", range=[-0.5, len(SHOW) - 0.5], tickvals=list(range(len(SHOW)))[::2],
                     ticktext=[str(s) for s in SHOW[::2]], row=1, col=2)
    fig.update_yaxes(title_text="loss", type="log", range=[-1.0, 2.3], row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=500, font=dict(FONT, size=20),
                      title=dict(text=f"step {k}:  ŷ = {m:.2f}x + {b:.2f},  loss = {L:.2f}", x=0.5),
                      margin=dict(l=70, r=30, t=100, b=60))
    fig.update_annotations(font_size=22)
    return fig


if __name__ == "__main__":
    print("loss start/end:", round(loss[0], 1), round(loss[-1], 3), "fit:", hist[-1][:2], best)
    save_gif([frame(k) for k in SHOW], "train_loop", [2, len(SHOW) - 1], here, fps=2, cols=1)
