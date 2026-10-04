"""Push and pull, point by point (Plotly frames -> GIF). Data: the 24 standardised students of the perceptron-trick
Note (12 placed, 12 not placed). Start: the line where the step perceptron stopped there, w = (0.30, 1.39, 0.12)
(recomputed below). Now the sigmoid rule w <- w + 0.5 (y - sigma(w . x)) x runs on random picks (seed 0). Every pick
moves the line. The arrow starts on the line next to the picked student: it points away from a correctly classified
student (push) and towards a misclassified one (pull); its length is |y - y_hat|. The script checks that the smallest
distance from the line to a student grows from 0.14 to 0.54 over 40 picks, and that all 40 picks are pushes
(every student is already correct)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
rng = np.random.default_rng(3)
placed = np.c_[rng.normal(8.0, 0.45, 40), rng.normal(118, 6, 40)][:12]
not_placed = np.c_[rng.normal(6.0, 0.45, 40), rng.normal(92, 6, 40)][:12]
X = np.r_[placed, not_placed]
y = np.r_[np.ones(12), np.zeros(12)]
Z = (X - X.mean(0)) / X.std(0)
A = np.c_[np.ones(24), Z]
LIM, LR, PICKS = 2.6, 0.5, 40
sig = lambda z: 1 / (1 + np.exp(-z))

w, pick = np.array([1.0, 1.0, -1.0]), np.random.default_rng(0)       # the step perceptron of the previous Note
while ((A @ w > 0) != y).any():
    j = pick.integers(24)
    w = w + 0.1 * (y[j] - float(A[j] @ w > 0)) * A[j]
W_STEP = w.copy()
gap = lambda w: np.abs(A @ w).min() / np.hypot(w[1], w[2])            # smallest distance from the line to a student
pick = np.random.default_rng(0)
steps = []                                                            # (w before, j, y_hat, w after)
for _ in range(PICKS):
    j = pick.integers(24)
    yh = sig(A[j] @ w)
    w2 = w + LR * (y[j] - yh) * A[j]
    steps.append((w, j, yh, w2))
    w = w2


def line(w):
    if abs(w[2]) > abs(w[1]):
        xs = np.array([-LIM, LIM])
        return xs, -(w[0] + w[1] * xs) / w[2]
    ys = np.array([-LIM, LIM])
    return -(w[0] + w[2] * ys) / w[1], ys


def frame(w, title, j=None, old=None, d=0.0, pull=False):
    fig = go.Figure()
    if old is not None:
        fig.add_scatter(x=line(old)[0], y=line(old)[1], mode="lines", line=dict(color=GREY, width=3, dash="dash"), name="line before")
    fig.add_scatter(x=line(w)[0], y=line(w)[1], mode="lines", line=dict(color="black", width=5), name="line now")
    for k, c, name in ((1, GREEN, "placed (y = 1)"), (0, BLUE, "not placed (y = 0)")):
        fig.add_scatter(x=Z[y == k, 0], y=Z[y == k, 1], mode="markers", name=name, marker=dict(size=15, color=c, line=dict(width=1.5, color="black")))
    if j is not None:
        p, n = Z[j], old[1:] / np.hypot(old[1], old[2])
        foot = p - (A[j] @ old) / np.hypot(old[1], old[2]) * n        # nearest point of the old line
        away = (foot - p) / np.linalg.norm(foot - p)
        tip = foot + (-away if pull else away) * 1.6 * abs(d)
        fig.add_scatter(x=[p[0]], y=[p[1]], mode="markers", showlegend=False, marker=dict(size=34, color="rgba(0,0,0,0)", line=dict(width=5, color=RED)))
        fig.add_scatter(x=[p[0], foot[0]], y=[p[1], foot[1]], mode="lines", line=dict(color=RED, width=2, dash="dot"), showlegend=False)
        fig.add_annotation(x=tip[0], y=tip[1], ax=foot[0], ay=foot[1], xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                           arrowhead=2, arrowsize=1.2, arrowwidth=5, arrowcolor=RED)
    fig.update_layout(template="simple_white", width=1000, height=720, font=FONT, title=dict(text=title, x=0.5, y=0.95),
                      xaxis=dict(title="CGPA (standardised)", range=[-LIM, LIM]), yaxis=dict(title="IQ (standardised)", range=[-LIM, LIM]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.14), margin=dict(l=80, r=30, t=120, b=120))
    return fig


if __name__ == "__main__":
    assert (round(gap(W_STEP), 2), round(gap(w), 2)) == (0.14, 0.54), (gap(W_STEP), gap(w))
    assert not any((s[2] > 0.5) != y[s[1]] for s in steps)
    figs = [frame(W_STEP, "the step perceptron has stopped: every student is correct,<br>but the line is only 0.14 from the nearest student")]
    for i, (w0, j, yh, w2) in enumerate(steps, 1):
        d = y[j] - yh
        pull = (yh > 0.5) != y[j]
        kind = "misclassified: pull" if pull else "correct: push"
        t = (f"pick {i}: ŷ = σ(z) = {yh:.2f}, y − ŷ = {d:+.2f}".replace("-", "−") + f"<br>{kind}, strength {abs(d):.2f}")
        figs.append(frame(w2, t, j, old=w0, d=d, pull=pull))
    figs.append(frame(w, f"after {PICKS} picks: the line has moved into the gap<br>smallest distance to a student: {gap(W_STEP):.2f} → {gap(w):.2f}", old=W_STEP))
    make_gif(figs, here / "push_pull_run", fps=2, holds=[6] + [3] * PICKS + [10], keys=[0, 1, 2, len(figs) - 1], width=800)
