"""The 128-128 network on make_moons trained with eight values of the L2 strength, from 0 to 1: the decision
surface, the 256 first-layer weights, and the training and validation loss (cross-entropy only, without the
penalty). Data: data/lambda_sweep*.{csv,npz} (Notebook, section 6). Plotly frames: one value of lambda per frame.
Run: python lambda_sweep.py -> lambda_sweep.gif, lambda_sweep_frames.png"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, RED, GREY
from frames import save

HERE = Path(__file__).parent
D = HERE.parent / "data"
s = pd.read_csv(D / "lambda_sweep.csv")
w = pd.read_csv(D / "lambda_sweep_weights.csv")
g = np.load(D / "lambda_sweep_grid.npz")
pts = pd.read_csv(D / "points.csv")
xs, ys = np.unique(g["x1"]), np.unique(g["x2"])
FONT = dict(family="Latin Modern Roman", size=22)
LAMS = list(s.lam)
VERDICT = {0: "overfits", 0.001: "overfits a little", 0.3: "underfits", 1.0: "underfits: all weights near 0"}
assert len(LAMS) == 8 and s.val_loss_data.idxmin() not in (0, 7)        # the best lambda is in the middle


def frame(k):
    lam = LAMS[k]
    key = f"{lam:g}"
    z = g[key].reshape(len(ys), len(xs))
    fig = make_subplots(1, 3, column_widths=[0.36, 0.3, 0.34], horizontal_spacing=0.08,
                        subplot_titles=("decision boundary", "first-layer weights", "loss without the penalty"))
    fig.add_trace(go.Heatmap(x=xs, y=ys, z=(z > 0.5).astype(int), showscale=False, opacity=0.2, zmin=0, zmax=1,
                             colorscale=[[0, ORANGE], [1, BLUE]]), 1, 1)
    if z.min() < 0.5 < z.max():
        fig.add_trace(go.Contour(x=xs, y=ys, z=z, showscale=False, contours=dict(start=0.5, end=0.5, size=1, coloring="lines"),
                                 colorscale=[[0, "black"], [1, "black"]], line=dict(width=3)), 1, 1)
    for cls, c in ((0, ORANGE), (1, BLUE)):
        q = pts[pts.y == cls]
        fig.add_trace(go.Scatter(x=q.x1, y=q.x2, mode="markers", marker=dict(color=c, size=8, line=dict(width=1, color="white"))), 1, 1)
    fig.add_trace(go.Histogram(x=w[key], xbins=dict(start=-3, end=3, size=0.1), marker_color=GREEN), 1, 2)
    fig.add_annotation(x=2.9, y=np.log10(120), xref="x2", yref="y2", xanchor="right", showarrow=False,
                       text=f"largest |w|<br>{s.largest_w[k]:.2f}", font=dict(size=20))
    x = list(range(8))
    for col, c, name in (("train_loss_data", GREY, "training"), ("val_loss_data", RED, "validation")):
        fig.add_trace(go.Scatter(x=x, y=s[col], mode="lines+markers", line=dict(color=c, width=3), marker=dict(size=7)), 1, 3)
        fig.add_trace(go.Scatter(x=[k], y=[s[col][k]], mode="markers", marker=dict(color=c, size=18, line=dict(color="black", width=2))), 1, 3)
        fig.add_annotation(x=3.5, y=0.86 if name == "validation" else 0.78, xref="x3", yref="y3",
                           xanchor="center", showarrow=False, text=name, font=dict(color=c, size=20))
    fig.update_xaxes(range=[-2, 3], showticklabels=False, row=1, col=1)
    fig.update_yaxes(range=[-1.75, 2.25], showticklabels=False, row=1, col=1)
    fig.update_xaxes(range=[-3, 3], title="weight", row=1, col=2)
    fig.update_yaxes(type="log", range=[0, 2.5], dtick=1, title="number of weights", row=1, col=2)
    fig.update_xaxes(tickvals=x, ticktext=[f"{v:g}" for v in LAMS], tickangle=60, title="λ", row=1, col=3)
    fig.update_yaxes(range=[0, 0.9], row=1, col=3)
    fig.update_annotations(font=dict(size=22), selector=lambda a: a.yref == "paper")
    verdict = VERDICT.get(lam, "a smooth boundary that follows the moons")
    fig.update_layout(template="simple_white", width=1300, height=520, font=FONT, showlegend=False,
                      title=dict(text=f"λ = {lam:g}: training accuracy {s.train_acc[k]:.0%}, {verdict}", x=0.5, y=0.97),
                      margin=dict(l=20, r=20, t=110, b=90))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(8)]
    seq = [0] * 4 + [k for k in range(8) for _ in range(3)] + [7] * 4 + [4] * 6
    save("lambda_sweep", figs, seq, [0, 2, 4, 7], HERE, fps=1.6, gif_width=900)
