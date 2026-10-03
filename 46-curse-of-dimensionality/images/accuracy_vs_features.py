"""Real measurement: KNN accuracy on the digits data as features are added.
Left part: the 64 real pixels, most useful first. Right part: 64 pixels plus useless random columns."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_digits
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier

here = Path(__file__).parent
X, y = load_digits(return_X_y=True)
order = np.argsort(-mutual_info_classif(X, y, random_state=0))     # most useful pixel first
noise = np.random.default_rng(0).uniform(0, 16, (len(X), 400))      # columns with no information
score = lambda Z: cross_val_score(KNeighborsClassifier(), Z, y, cv=5).mean()

k_real = [1, 2, 4, 8, 12, 16, 24, 32, 40, 48, 56, 64]
acc_real = [score(X[:, order[:k]]) for k in k_real]
n_noise = [25, 50, 100, 150, 200, 300, 400]
acc_noise = [score(np.hstack([X, noise[:, :n]])) for n in n_noise]
for k, a in zip(k_real, acc_real): print(k, round(a, 3))
for n, a in zip(n_noise, acc_noise): print(64 + n, round(a, 3))

BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
fig = go.Figure()
fig.add_vrect(x0=64, x1=470, fillcolor=RED, opacity=0.07, line_width=0)
fig.add_trace(go.Scatter(x=k_real, y=acc_real, mode="lines+markers", name="real pixels added",
                         line=dict(color=BLUE, width=4), marker=dict(size=8)))
fig.add_trace(go.Scatter(x=[64] + [64 + n for n in n_noise], y=[acc_real[-1]] + acc_noise, mode="lines+markers",
                         name="useless columns added", line=dict(color=RED, width=4, dash="dash"), marker=dict(size=8)))
best = int(np.argmax(acc_real))
fig.add_annotation(x=k_real[best], y=acc_real[best], ax=40, ay=60, text=f"best: {acc_real[best]:.0%}",
                   font=dict(size=16), arrowcolor=GREY)
fig.add_annotation(x=464, y=acc_noise[-1], ax=-90, ay=-90, text=f"{acc_noise[-1]:.0%} with 464 columns",
                   font=dict(size=16), arrowcolor=GREY)
fig.add_annotation(x=265, y=0.30, text="more columns, worse model", showarrow=False, font=dict(size=17, color=RED))
fig.update_layout(template="simple_white", width=950, height=500, font=dict(family="Latin Modern Roman", size=17),
                  title=dict(text="KNN on 8×8 digit images: accuracy as columns are added", x=0.5),
                  xaxis=dict(title="Number of input columns", range=[0, 470]),
                  yaxis=dict(title="Accuracy (5-fold cross-validation)", tickformat=".0%", range=[0, 1.02]),
                  legend=dict(x=0.45, y=0.55), margin=dict(l=80, r=30, t=70, b=60))
fig.write_image(here / "accuracy_vs_features.png", scale=2)
fig.write_image(here / "accuracy_vs_features.pdf")
