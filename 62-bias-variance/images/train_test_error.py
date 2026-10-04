"""Training error vs test error for one training set (Plotly), two figures with the same layout:
bias_fit.png     (Section 2): a straight line misses even the points it was trained on -> large training error.
variance_fit.png (Section 3): a degree-11 curve passes near its training points but misses new points at the
                 same inputs -> small training error, large test error.
The drawn set is training set 0 of common.py; new data = set 1 (same 20 inputs, new noise). The errors printed on the
figure are averages over all 10,000 training sets, each tested on the next set's targets."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import fits, f, xs, X, Y

here = Path(__file__).parent
BLUE, ORANGE, GREY, RED = "#4C78A8", "#F58518", "#6B6B6B", "#E45756"
x = X.ravel()


def errors(d):
    P, G = fits(d)
    train = float(np.mean((P - Y) ** 2))                       # each model on its own training targets
    test = float(np.mean((P[:, :-1] - Y[:, 1:]) ** 2))        # each model on the next set's targets (new noise)
    return P, G, train, test


P1, G1, tr1, te1 = errors(1)
P11, G11, tr11, te11 = errors(11)
print(f"degree 1: train {tr1:.3f} test {te1:.3f} | degree 11: train {tr11:.3f} test {te11:.3f}")
assert tr1 > 0.6 and te1 > 0.6                    # high bias: large error on training AND new data
assert tr11 < tr1 / 5 and te11 > 3 * tr11         # high variance: tiny training error, test error several times larger


def sticks(xv, yv, pv, color, width):
    xx, yy = [], []
    for a, b, c in zip(xv, yv, pv):
        xx += [a, a, None]; yy += [b, c, None]
    return go.Scatter(x=xx, y=yy, mode="lines", line=dict(color=color, width=width), showlegend=False)


def figure(name, title, curve, pred, show_new, note):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=f(xs), mode="lines", name="true wave", line=dict(color="black", width=3, dash="dash")))
    fig.add_trace(sticks(x, Y[:, 0], pred, BLUE, 2.5))
    if show_new:
        fig.add_trace(sticks(x + 0.04, Y[:, 1], pred, RED, 2.5))
    fig.add_trace(go.Scatter(x=xs, y=np.clip(curve, -4, 4), mode="lines", name="model", line=dict(color=ORANGE, width=4)))
    fig.add_trace(go.Scatter(x=x, y=Y[:, 0], mode="markers", name="training points (errors in blue)",
                             marker=dict(size=11, color=BLUE)))
    if show_new:
        fig.add_trace(go.Scatter(x=x + 0.04, y=Y[:, 1], mode="markers", name="new points, same inputs (errors in red)",
                                 marker=dict(size=11, color="white", line=dict(color=RED, width=2.5))))
    fig.add_annotation(x=0.5, y=-0.27, xref="paper", yref="paper", showarrow=False, text=note, font=dict(size=21))
    fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=title, x=0.5, font=dict(size=24)), xaxis=dict(title="x"),
                      yaxis=dict(title="y", range=[-3.5, 3.5]), margin=dict(l=60, r=20, t=60, b=140),
                      legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"))
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


figure("bias_fit", "A straight line misses even its own training points", G1[:, 0], P1[:, 0], False,
       f"average over 10,000 training sets: training error {tr1:.2f}, test error {te1:.2f}")
figure("variance_fit", "Degree 11: near its training points, far from new ones", G11[:, 0], P11[:, 0], True,
       f"average over 10,000 training sets: training error {tr11:.2f}, test error {te11:.2f}")
