"""Argmax against softmax (Plotly frames -> GIF), on the Note's query flower (scores 2.81, 1.84, -4.66). The setosa
score slides from -3 to 6 while the other two stay fixed. Left: the three softmax probabilities, always adding up to 1.
Right: the setosa output against its score: argmax is a step (slope 0 on both sides, so gradient descent gets no
signal), softmax is a smooth curve with slope p(1 - p)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, make_gif

here = Path(__file__).parent
REST = np.array([1.840, -4.655])                      # versicolor and virginica scores, fixed
names = ["setosa", "versicolor", "virginica"]


def soft(z1):
    e = np.exp(np.r_[z1, REST]); return e / e.sum()


grid = np.linspace(-3, 6, 181)
curve = np.array([soft(z)[0] for z in grid])
step = (grid > REST[0]).astype(float)
p0 = soft(2.815)
assert np.allclose(p0.round(3), [0.726, 0.274, 0.000], atol=6e-4) and round(p0[0] * (1 - p0[0]), 2) == 0.20


def frame(z1):
    p = soft(z1)
    fig = make_subplots(1, 2, column_widths=[0.45, 0.55], horizontal_spacing=0.13,
                        subplot_titles=[f"softmax probabilities (sum = {p.sum():.0f})", "setosa output against setosa score"])
    fig.update_annotations(font_size=21)
    fig.add_trace(go.Bar(x=names, y=p, marker_color=[BLUE, ORANGE, GREEN], text=[f"{v:.2f}" for v in p],
                         textposition="outside", showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=grid, y=step, mode="lines", line=dict(color=GREY, width=3, dash="dash", shape="hv"), name="argmax (slope 0)"), 1, 2)
    fig.add_trace(go.Scatter(x=grid, y=curve, mode="lines", line=dict(color=BLUE, width=4), name="softmax"), 1, 2)
    fig.add_trace(go.Scatter(x=[z1], y=[p[0]], mode="markers", marker=dict(size=16, color=BLUE, line=dict(color="black", width=2)), showlegend=False), 1, 2)
    fig.update_yaxes(range=[0, 1.18], row=1, col=1)
    fig.update_yaxes(range=[-0.05, 1.18], row=1, col=2)
    fig.update_xaxes(title=f"setosa score = {z1:.2f}, softmax slope = {p[0] * (1 - p[0]):.2f}".replace("-", "−"), range=[-3, 6], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT,
                      legend=dict(orientation="h", x=0.78, xanchor="center", y=-0.25), margin=dict(l=60, r=30, t=60, b=120))
    return fig


if __name__ == "__main__":
    zs = list(np.linspace(-3, 6, 19)) + [2.815]
    make_gif([frame(z) for z in zs], here / "compete", fps=4, holds=[3] + [1] * 18 + [10], keys=[2, 19], cols=1)
