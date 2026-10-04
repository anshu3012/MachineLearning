"""Two models scored on the same 10 cross-validation folds of the breast cancer data (scikit-learn's copy of the
Wisconsin diagnostic data, 569 tumours, 30 features): scaled logistic regression against a decision tree
(random_state=0), KFold(10, shuffle=True, random_state=0). Each fold gives a pair of accuracies, joined by a
line, as each person gave a pair of weights. ttest_rel on the ten pairs."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

here = Path(__file__).parent
X, y = load_breast_cancer(return_X_y=True)
cv = KFold(10, shuffle=True, random_state=0)
a = cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), X, y, cv=cv)
b = cross_val_score(DecisionTreeClassifier(random_state=0), X, y, cv=cv)
res = stats.ttest_rel(a, b)
print(f"logistic {a.mean():.3f}, tree {b.mean():.3f}, t = {res.statistic:.2f}, p = {res.pvalue:.4f}, "
      f"logistic wins {(a > b).sum()} of 10")
assert (a > b).sum() == 9 and (a < b).sum() == 0 and round(res.statistic, 2) == 4.96 and round(res.pvalue, 3) == 0.001
fig = go.Figure()
for i in range(10):
    c = "#54A24B" if a[i] > b[i] else ("#E45756" if a[i] < b[i] else "#6B6B6B")
    fig.add_scatter(x=["logistic regression", "decision tree"], y=[a[i], b[i]], mode="lines+markers",
                    line=dict(color=c, width=2.5), marker=dict(size=10))
fig.update_yaxes(title_text="accuracy on the fold", tickformat=".2f")
fig.update_xaxes(range=[-0.35, 1.35])
fig.update_layout(template="simple_white", width=700, height=480, showlegend=False,
                  title=dict(text=f"10 folds: paired t = {res.statistic:.2f}, p = {res.pvalue:.3f}", x=0.5),
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=80, r=30, t=60, b=50))
fig.write_image(here / "cv_paired.png", scale=2)
fig.write_image(here / "cv_paired.pdf")
