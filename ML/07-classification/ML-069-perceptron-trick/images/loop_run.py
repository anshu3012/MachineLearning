"""The perceptron trick as a run (Plotly frames -> GIF). Data: the first 12 placed and 12 not-placed students of
Figure 1 (separable.py, seed 3), both features standardised. Start line w = (w0, w1, w2) = (1, 1, -1), learning rate
0.1, random picks with seed 0. Each frame picks one student: if the point is on its correct side nothing changes
(y - y_hat = 0); if not, w <- w + 0.1 (y - y_hat) x and the line moves towards it. The run stops when no point is
misclassified: after 36 picks, 11 of which moved the line."""
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
LIM, LR = 2.6, 0.1
predict = lambda w: (A @ w > 0).astype(float)

w, pick = np.array([1.0, 1.0, -1.0]), np.random.default_rng(0)
steps = []                                   # (w before, j, y_hat, w after)
while (predict(w) != y).any():
    j = pick.integers(24)
    yh = float(A[j] @ w > 0)
    w2 = w + LR * (y[j] - yh) * A[j]
    steps.append((w, j, yh, w2))
    w = w2
assert len(steps) == 36 and sum(s[2] != y[s[1]] for s in steps) == 11, len(steps)


def side(w, sign):
    """Corners of the plot square where sign * (w0 + w1 x + w2 y) >= 0."""
    box = [(-LIM, -LIM), (LIM, -LIM), (LIM, LIM), (-LIM, LIM)]
    f = lambda p: sign * (w[0] + w[1] * p[0] + w[2] * p[1])
    out = []
    for a, b in zip(box, box[1:] + box[:1]):
        if f(a) >= 0:
            out.append(a)
        if f(a) * f(b) < 0:
            t = f(a) / (f(a) - f(b))
            out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    return np.array(out + out[:1])


def line(w):
    xs = np.array([-LIM, LIM]) if abs(w[2]) > abs(w[1]) else None
    if xs is not None:
        return xs, -(w[0] + w[1] * xs) / w[2]
    ys = np.array([-LIM, LIM])
    return -(w[0] + w[2] * ys) / w[1], ys


def frame(w, title, j=None, old=None):
    fig = go.Figure()
    for sign, c in ((1, GREEN), (-1, BLUE)):
        p = side(w, sign)
        fig.add_scatter(x=p[:, 0], y=p[:, 1], fill="toself", mode="none", fillcolor=c, opacity=0.13, showlegend=False)
    if old is not None:
        fig.add_scatter(x=line(old)[0], y=line(old)[1], mode="lines", line=dict(color=GREY, width=3, dash="dash"), name="line before")
    fig.add_scatter(x=line(w)[0], y=line(w)[1], mode="lines", line=dict(color="black", width=5), name="line now")
    wrong = predict(w) != y
    for k, c, name in ((1, GREEN, "placed (y = 1)"), (0, BLUE, "not placed (y = 0)")):
        m = y == k
        fig.add_scatter(x=Z[m, 0], y=Z[m, 1], mode="markers", showlegend=False,
                        marker=dict(size=15, color=c, symbol=np.where(wrong[m], "x", "circle"), line=dict(width=1.5, color="black")))
        fig.add_scatter(x=[None], y=[None], mode="markers", name=name, marker=dict(size=15, color=c, line=dict(width=1.5, color="black")))
    fig.add_scatter(x=[None], y=[None], mode="markers", name="cross: misclassified", marker=dict(size=15, color=GREY, symbol="x", line=dict(width=1.5, color="black")))
    if j is not None:
        fig.add_scatter(x=[Z[j, 0]], y=[Z[j, 1]], mode="markers", showlegend=False,
                        marker=dict(size=34, color="rgba(0,0,0,0)", line=dict(width=5, color=RED)))
    fig.update_layout(template="simple_white", width=1000, height=720, font=FONT, title=dict(text=title, x=0.5, y=0.95),
                      xaxis=dict(title="CGPA (standardised)", range=[-LIM, LIM]), yaxis=dict(title="IQ (standardised)", range=[-LIM, LIM]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.14), margin=dict(l=80, r=30, t=120, b=120))
    return fig


def figures():
    w0 = steps[0][0]
    figs = [frame(w0, f"start: any line. Crosses mark the {int((predict(w0) != y).sum())} misclassified students<br>green side: predicted placed; blue side: predicted not placed")]
    moved = []
    for i, (w, j, yh, w2) in enumerate(steps, 1):
        who = "placed" if y[j] == 1 else "not placed"
        said = "placed" if yh == 1 else "not placed"
        d = int(y[j] - yh)
        if d == 0:
            t = f"pick {i}: a {who} student, predicted {said}<br>y − ŷ = 0: correct, the line stays"
            figs.append(frame(w, t, j))
        else:
            act = "add 0.1 x: the line moves towards the point" if d > 0 else "subtract 0.1 x: the line moves towards the point"
            t = f"pick {i}: a {who} student, predicted {said}<br>y − ŷ = {'+1' if d > 0 else '−1'}: {act}"
            figs.append(frame(w2, t, j, old=w))
            moved.append(len(figs) - 1)
    figs.append(frame(steps[-1][3], f"after {len(steps)} picks no student is misclassified: stop<br>(convergence; {len(moved)} picks moved the line)"))
    return figs, moved


if __name__ == "__main__":
    figs, moved = figures()
    holds = [5] + [4 if i in moved else 2 for i in range(1, len(figs) - 1)] + [10]
    make_gif(figs, here / "loop_run", fps=2, holds=holds, keys=[0, moved[0], moved[len(moved) // 2], len(figs) - 1], width=800)
