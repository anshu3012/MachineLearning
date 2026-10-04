"""Why an ensemble helps: (a) three classifiers' boundaries and their majority-vote boundary; (b) four regression
lines and their mean (Plotly)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_moons
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"

# (a) classification: three different algorithms, same data
X, y = make_moons(n_samples=400, noise=0.35, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=0)
models = {"logistic regression": LogisticRegression(), "decision tree (depth 3)": DecisionTreeClassifier(max_depth=3, random_state=0),
          "KNN (k = 5)": KNeighborsClassifier(5)}
xs, ys = np.linspace(-2, 3, 300), np.linspace(-1.6, 2.1, 300)
XX, YY = np.meshgrid(xs, ys)
grid = np.c_[XX.ravel(), YY.ravel()]
preds, acc = {}, {}
for name, m in models.items():
    m.fit(X_tr, y_tr)
    preds[name] = m.predict(grid).reshape(XX.shape)
    acc[name] = m.score(X_te, y_te)
vote = (sum(preds.values()) >= 2).astype(int)
vote_test = (sum(m.predict(X_te) for m in models.values()) >= 2).astype(int)
acc["majority vote"] = (vote_test == y_te).mean()
print({k: round(v, 3) for k, v in acc.items()})

fig = make_subplots(1, 2, subplot_titles=("(a) classification: three models and the vote",
                                          "(b) regression: four lines and their mean"), horizontal_spacing=0.08)
fig.add_trace(go.Heatmap(x=xs, y=ys, z=vote, colorscale=[[0, "#FDE5CC"], [1, "#DCE6F2"]], showscale=False,
                         hoverinfo="skip"), 1, 1)
for cls, c in ((0, ORANGE), (1, BLUE)):
    m = y_tr == cls
    fig.add_trace(go.Scatter(x=X_tr[m, 0], y=X_tr[m, 1], mode="markers", showlegend=False,
                             marker=dict(color=c, size=6, line=dict(color="white", width=0.5))), 1, 1)
for (name, Z), c in zip(preds.items(), (GREEN, RED, PURPLE)):
    fig.add_trace(go.Contour(x=xs, y=ys, z=Z, contours=dict(start=0.5, end=0.5, coloring="none"), showscale=False,
                             line=dict(color=c, width=2, dash="dot"), name=f"{name}: {acc[name]:.2f}",
                             showlegend=True, hoverinfo="skip"), 1, 1)
fig.add_trace(go.Contour(x=xs, y=ys, z=vote, contours=dict(start=0.5, end=0.5, coloring="none"), showscale=False,
                         line=dict(color="black", width=4), name=f"majority vote: {acc['majority vote']:.2f}",
                         hoverinfo="skip"), 1, 1)

# (b) regression: four lines, each fitted to a different random half of the data, and their mean
rng = np.random.default_rng(7)
x = rng.uniform(0, 10, 60)
yv = 2 + 0.8 * x + rng.normal(0, 2.2, 60)
fig.add_trace(go.Scatter(x=x, y=yv, mode="markers", marker=dict(color=GREY, size=7), showlegend=False), 1, 2)
line_x = np.array([0, 10])
lines = []
for c in (GREEN, RED, PURPLE, ORANGE):
    idx = rng.choice(60, 10, replace=False)
    lr = LinearRegression().fit(x[idx, None], yv[idx])
    ly = lr.predict(line_x[:, None])
    lines.append(ly)
    fig.add_trace(go.Scatter(x=line_x, y=ly, mode="lines", line=dict(color=c, width=2, dash="dot"),
                             showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=line_x, y=np.mean(lines, axis=0), mode="lines", line=dict(color="black", width=4),
                         showlegend=False), 1, 2)
mean_line = np.mean(lines, axis=0)
fig.add_annotation(x=7, y=mean_line[0] + 0.7 * (mean_line[1] - mean_line[0]), xref="x2", yref="y2", ax=60, ay=70,
                   text="mean of the four", showarrow=True, arrowwidth=2, font=dict(size=17), bgcolor="white")

fig.update_xaxes(range=[xs[0], xs[-1]], title="x1", row=1, col=1)
fig.update_yaxes(range=[ys[0], ys[-1]], title="x2", row=1, col=1)
fig.update_xaxes(title="input", row=1, col=2)
fig.update_yaxes(title="output", row=1, col=2)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1300, height=600, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(orientation="h", x=0.0, y=-0.16, title_text="test accuracy  "),
                  margin=dict(l=70, r=20, t=60, b=110))
fig.write_image(HERE / "why_it_works.png", scale=2)
fig.write_image(HERE / "why_it_works.pdf")
