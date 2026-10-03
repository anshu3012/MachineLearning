"""Real measurement for Note 45: cross-validated accuracy of logistic regression for each set of columns.
Every new column is built inside a pipeline, so each fold builds it from its own training rows."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic.csv").dropna(subset=["Age"])
y = df["Survived"]


def add_columns(X):
    X = X.copy()
    X["Family_size"] = X["SibSp"] + X["Parch"] + 1
    X["Family_type"] = np.select([X["Family_size"] == 1, X["Family_size"] <= 4], [0, 1], 2)
    X["Title"] = X["Name"].str.split(", ").str[1].str.split(".").str[0]
    X["Is_Married"] = (X["Title"] == "Mrs").astype(int)
    return X


def model(cols, onehot=()):
    pick = make_column_transformer(
        (OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=10), list(onehot)),
        ("passthrough", [c for c in cols if c not in onehot]))
    return make_pipeline(FunctionTransformer(add_columns), pick, LogisticRegression(max_iter=1000))


BASE = ["Age", "Pclass", "SibSp", "Parch"]
SETS = [("Age, Pclass, SibSp, Parch", model(BASE)),
        ("+ Family_size", model(BASE + ["Family_size"])),
        ("Family_type as 0/1/2<br>(replaces SibSp, Parch)", model(["Age", "Pclass", "Family_type"])),
        ("Family_type one-hot<br>(replaces SibSp, Parch)", model(["Age", "Pclass", "Family_type"], ["Family_type"])),
        ("+ Is_Married", model(BASE + ["Is_Married"])),
        ("+ Title one-hot", model(BASE + ["Title"], ["Title"]))]
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=10, random_state=0)
cols = ["Age", "Pclass", "SibSp", "Parch", "Name"]
res = [(name, cross_val_score(m, df[cols], y, cv=cv)) for name, m in SETS]
for name, s in res: print(f"{name.replace('<br>', ' '):45s} {s.mean():.4f} +- {s.std():.4f}")

BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
names = [n for n, _ in res][::-1]
means = [s.mean() for _, s in res][::-1]
stds = [s.std() for _, s in res][::-1]
colour = [GREY if i == len(names) - 1 else (BLUE if i >= 2 else ORANGE) for i in range(len(names))]
fig = go.Figure(go.Scatter(x=means, y=names, mode="markers+text", marker=dict(size=16, color=colour),
                           error_x=dict(array=stds, color=GREY, thickness=2, width=8),
                           text=[f"{m:.1%}" for m in means], textposition="top center",
                           textfont=dict(size=20)))
fig.update_layout(template="simple_white", width=900, height=600, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=21),
                  xaxis=dict(title="Accuracy (10 × 10-fold cross-validation; bar = ±1 std)",
                             tickformat=".0%", range=[0.6, 0.88]),
                  margin=dict(l=20, r=30, t=20, b=70))
fig.write_image(here / "scores.png", scale=2)
fig.write_image(here / "scores.pdf")
