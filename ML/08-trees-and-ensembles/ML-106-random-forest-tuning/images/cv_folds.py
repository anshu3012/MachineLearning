"""Heart data, section 4: one 61-patient test split against 10-fold cross-validation, for the random forest and
logistic regression. Each dot is one fold's accuracy; the star is the single split of section 3. (Plotly)"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
X, y = df.iloc[:, :-1], df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
models = {"random forest": RandomForestClassifier(random_state=42), "logistic regression": LogisticRegression(max_iter=5000)}
split = {n: m.fit(X_train, y_train).score(X_test, y_test) for n, m in models.items()}
folds = {n: cross_val_score(m, X, y, cv=10) for n, m in models.items()}
assert [round(split[n], 3) for n in models] == [0.836, 0.885]
assert [round(folds[n].mean(), 3) for n in models] == [0.832, 0.818]
print({n: (folds[n].min().round(3), folds[n].max().round(3)) for n in models})

fig = go.Figure()
for i, (n, c) in enumerate(zip(models, ["#4C78A8", "#F58518"])):
    f = folds[n]
    fig.add_trace(go.Scatter(x=f, y=i + np.linspace(-0.18, 0.18, 10), mode="markers", name="one fold of 10" if i == 0 else None,
                             showlegend=i == 0, marker=dict(color="#BBBBBB", size=12, line=dict(color=c, width=2))))
    fig.add_trace(go.Scatter(x=[f.mean()] * 2, y=[i - 0.3, i + 0.3], mode="lines", showlegend=False,
                             line=dict(color=c, width=5)))
    fig.add_annotation(x=f.mean(), y=i + 0.38, text=f"10-fold mean {f.mean():.3f}", showarrow=False,
                       font=dict(color=c, size=20))
    fig.add_trace(go.Scatter(x=[split[n]], y=[i - 0.38], mode="markers+text", text=[f"one split {split[n]:.3f}"],
                             textposition="bottom center", showlegend=False, textfont=dict(size=20),
                             marker=dict(symbol="star", size=20, color="#E45756")))
fig.update_yaxes(tickvals=[0, 1], ticktext=list(models), range=[-0.75, 0.6 + 1])
fig.update_xaxes(title="accuracy")
fig.update_layout(template="simple_white", width=1200, height=560, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=190, r=30, t=30, b=70), legend=dict(x=0.01, y=1.0))
fig.write_image(HERE / "cv_folds.png", scale=2)
fig.write_image(HERE / "cv_folds.pdf")
