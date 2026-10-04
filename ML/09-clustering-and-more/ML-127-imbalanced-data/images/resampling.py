"""The training data after random undersampling, random oversampling and SMOTE, each with the line logistic
regression learns on it (dashed: the line learned on the original data)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression
from imb import BLUE, RED, ORANGE, FONT, data, undersample, oversample, smote

here = Path(__file__).parent
Xtr, Xte, ytr, yte = data()
gx = np.linspace(-4.7, 3.3, 50)


def line(X, y):
    m = LogisticRegression().fit(X, y)
    (a, b), c = m.coef_[0], m.intercept_[0]
    return -(a * gx + c) / b


base = line(Xtr, ytr)
Xu, yu = undersample(Xtr, ytr)
Xo, yo = oversample(Xtr, ytr)
Xs, ys, new = smote(Xtr, ytr)
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06, subplot_titles=(
    "Random undersampling: 21 + 21 rows", "Random oversampling: 299 + 299 rows", "SMOTE: 299 + 21 + 278 new rows"))
leg = set()


def dots(col, X, colour, name, size=7, opacity=0.6, border=False):
    fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode="markers", name=name, showlegend=name not in leg,
                             legendgroup=name, marker=dict(color=colour, size=size, opacity=opacity,
                                                           line=dict(width=1, color="black") if border else None)), 1, col)
    leg.add(name)


dots(1, Xu[yu == 1], BLUE, "class 1 (majority)")
dots(1, Xu[yu == 0], RED, "class 0 (minority)", 9, 0.9, True)
dots(2, Xo[yo == 1], BLUE, "class 1 (majority)")
pts, times = np.unique(Xo[yo == 0], axis=0, return_counts=True)       # duplicates drawn as one bigger dot
fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="markers",
                         name="class 0, copied rows (bigger = more copies)",
                         marker=dict(color=RED, size=4 + 1.2 * times, opacity=0.9, line=dict(width=1, color="black"))), 1, 2)
dots(3, Xtr[ytr == 1], BLUE, "class 1 (majority)")
dots(3, new, ORANGE, "class 0, synthetic (SMOTE)", 6, 0.8)
dots(3, Xtr[ytr == 0], RED, "class 0 (minority)", 9, 0.9, True)
for col, (X, y) in enumerate([(Xu, yu), (Xo, yo), (Xs, ys)], start=1):
    fig.add_trace(go.Scatter(x=gx, y=base, mode="lines", line=dict(color="#6B6B6B", width=2, dash="dash"),
                             name="boundary on the original data", showlegend=col == 1), 1, col)
    fig.add_trace(go.Scatter(x=gx, y=line(X, y), mode="lines", line=dict(color="black", width=3),
                             name="boundary on the resampled data", showlegend=col == 1), 1, col)
    fig.update_xaxes(range=[-4.7, 3.3], title_text="x1", row=1, col=col)
    fig.update_yaxes(range=[-4, 4.3], title_text="x2" if col == 1 else None, row=1, col=col)
fig.update_layout(template="simple_white", width=1500, height=600, font=FONT,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.17), margin=dict(l=60, r=20, t=50, b=140))
fig.update_annotations(font=dict(family=FONT["family"], size=19))
fig.write_image(here / "resampling.png", scale=2)
fig.write_image(here / "resampling.pdf")
