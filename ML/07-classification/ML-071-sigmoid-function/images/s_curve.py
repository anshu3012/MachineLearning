"""The sigmoid as a model of one feature (Plotly). Data: the 100 students of data/placement.csv (CGPA, placed or not).
Logistic regression on CGPA alone (almost no penalty, C = 1e6) gives w0 = -39.26, w1 = 6.53: P(placed) = 0.5 at CGPA 6.01.
1. s_curve.gif: the curve sigma(w0 + w1 CGPA) on the data. First w0 shifts the curve (the 0.5 crossing moves from
   CGPA 4.5 to 6.01, w1 = 1), then w1 steepens it (1 -> 6.53), ending on the fitted curve.
2. log_odds.png: the fitted curve as a probability (S-shape) and as log-odds ln(p / (1 - p)) = w0 + w1 CGPA (a straight line)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "placement.csv")
x, y = d.cgpa.values, d.placement.values
m = LogisticRegression(C=1e6).fit(x.reshape(-1, 1), y)
W0, W1 = float(m.intercept_[0]), float(m.coef_[0, 0])
CROSS = -W0 / W1
assert (round(W0, 2), round(W1, 2), round(CROSS, 2)) == (-39.26, 6.53, 6.01), (W0, W1, CROSS)
sig = lambda z: 1 / (1 + np.exp(-z))
P65 = sig(W0 + W1 * 6.5)
assert round(P65, 2) == 0.96, P65
xs = np.linspace(3, 9, 400)
minus = lambda t: t.replace("-", "−")


def frame(w1, cross, note, show_curve=True, read=False):
    w0 = -w1 * cross
    fig = go.Figure()
    for k, c, name in ((1, GREEN, "placed (1)"), (0, BLUE, "not placed (0)")):
        fig.add_scatter(x=x[y == k], y=y[y == k], mode="markers", marker=dict(size=13, color=c, opacity=0.55), name=name)
    fig.add_hline(y=0.5, line=dict(color=GREY, dash="dot", width=2))
    if show_curve:
        fig.add_scatter(x=xs, y=sig(w0 + w1 * xs), mode="lines", line=dict(color="black", width=5), showlegend=False)
        fig.add_scatter(x=[cross, cross], y=[0, 0.5], mode="lines", line=dict(color=RED, dash="dash", width=3), showlegend=False)
        fig.add_scatter(x=[cross], y=[0.5], mode="markers", marker=dict(size=16, color=RED), showlegend=False)
        fig.add_annotation(x=3.1, y=0.72, xanchor="left", showarrow=False, font=dict(size=24),
                           text=minus(f"w₀ = {w0:.2f}, w₁ = {w1:.2f}<br>P = 0.5 at CGPA {cross:.2f}"))
    if read:
        fig.add_scatter(x=[6.5, 6.5, 3], y=[0, P65, P65], mode="lines", line=dict(color=GREEN, width=3, dash="dash"), showlegend=False)
        fig.add_annotation(x=6.6, y=0.25, xanchor="left", showarrow=False, font=dict(size=22, color=GREEN), text=f"CGPA 6.5:<br>P(placed) = {P65:.2f}")
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, title=dict(text=note, x=0.5),
                      xaxis=dict(title="CGPA", range=[3, 9]), yaxis=dict(title="P(placed) = σ(w₀ + w₁ · CGPA)", range=[-0.08, 1.08]),
                      legend=dict(x=0.99, xanchor="right", y=0.2), margin=dict(l=90, r=30, t=70, b=70))
    return fig


def log_odds():
    ks = np.arange(4)
    cx = CROSS + ks / W1                      # CGPAs where the log-odds are 0, 1, 2, 3
    ps = sig(ks)
    assert [round(p, 3) for p in ps] == [0.5, 0.731, 0.881, 0.953]
    fig = make_subplots(1, 2, subplot_titles=("probability: an S-curve", "log-odds: a straight line"), horizontal_spacing=0.13)
    xr = np.linspace(5, 7, 200)
    fig.add_scatter(x=xr, y=sig(W0 + W1 * xr), mode="lines", line=dict(color="black", width=4), row=1, col=1)
    fig.add_scatter(x=xr, y=W0 + W1 * xr, mode="lines", line=dict(color="black", width=4), row=1, col=2)
    fig.add_scatter(x=cx, y=ps, mode="markers+text", marker=dict(size=14, color=RED), text=[f"{p:.3g}" for p in ps],
                    textposition="bottom right", textfont=dict(size=20, color=RED), row=1, col=1)
    fig.add_scatter(x=cx, y=ks, mode="markers+text", marker=dict(size=14, color=RED), text=[str(k) for k in ks],
                    textposition="bottom right", textfont=dict(size=20, color=RED), row=1, col=2)
    fig.add_hline(y=0, line=dict(color=GREY, dash="dot", width=2), row=1, col=2)
    fig.add_hline(y=0.5, line=dict(color=GREY, dash="dot", width=2), row=1, col=1)
    fig.update_xaxes(title="CGPA", range=[5, 7])
    fig.update_yaxes(title="P(placed)", range=[-0.05, 1.05], row=1, col=1)
    fig.update_yaxes(title="log-odds = w₀ + w₁ · CGPA", range=[-6.5, 6.5], row=1, col=2)
    fig.update_layout(template="simple_white", width=1150, height=520, font=FONT, showlegend=False, margin=dict(l=80, r=30, t=60, b=70))
    fig.update_annotations(font_size=24)
    fig.write_image(here / "log_odds.png", scale=2)


if __name__ == "__main__":
    log_odds()
    figs = [frame(1, 4.5, "the data: each student is a dot at 0 (not placed) or 1 (placed)", show_curve=False)]
    figs += [frame(1, c, "changing w₀ shifts the curve left or right") for c in (4.5, 5.0, 5.5, CROSS)]
    figs += [frame(w, CROSS, "a larger w₁ makes the curve steeper") for w in (2, 3, 4.5, W1)]
    figs.append(frame(W1, CROSS, "the fitted curve: read a probability for any CGPA", read=True))
    make_gif(figs, here / "s_curve", fps=1, holds=[3, 2, 1, 1, 2, 1, 1, 1, 2, 6], keys=[0, 1, 4, 9])
