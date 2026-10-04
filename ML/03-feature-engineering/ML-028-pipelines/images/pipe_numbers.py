"""Charts from the Note's Titanic pipeline (same split, same five steps):
chi2 scores of SelectKBest (chi2_scores.png), the 5 cross-validation folds (cv_folds.png),
and cross-validated accuracy against the tree's max_depth (depth_tuning.png). Plotly."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=22)
df = pd.read_csv(HERE.parent / "data" / "titanic_train.csv").drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])
X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=["Survived"]), df["Survived"],
                                                    test_size=0.2, random_state=42)
pipe = Pipeline([
    ("trf1", ColumnTransformer([("impute_age", SimpleImputer(), [2]),
                                ("impute_embarked", SimpleImputer(strategy="most_frequent"), [6])],
                               remainder="passthrough")),
    ("trf2", ColumnTransformer([("ohe_sex_embarked", OneHotEncoder(sparse_output=False, handle_unknown="ignore"),
                                 [1, 3])], remainder="passthrough")),
    ("trf3", ColumnTransformer([("scale", MinMaxScaler(), slice(0, 10))])),
    ("trf4", SelectKBest(score_func=chi2, k=8)),
    ("trf5", DecisionTreeClassifier(random_state=42))]).fit(X_train, y_train)
assert df[["Age", "Embarked"]].isnull().sum().tolist() == [177, 2]  # column_needs.tex
assert round(pipe.score(X_test, y_test), 3) == 0.788
assert round(pipe.named_steps["trf1"].transformers_[0][1].statistics_[0], 2) == 29.50

# 1. chi2 scores: the 10 columns after trf3, in trf2's order
names = ["Embarked_C", "Embarked_Q", "Embarked_S", "Sex_female", "Sex_male", "Age", "Pclass", "SibSp", "Parch", "Fare"]
sel = pipe.named_steps["trf4"]
scores, kept = sel.scores_, sel.get_support()
assert sorted(np.array(names)[~kept]) == ["Age", "Embarked_Q"]
order = np.argsort(scores)
fig = go.Figure(go.Bar(x=scores[order], y=np.array(names)[order], orientation="h",
                       marker_color=[BLUE if kept[i] else RED for i in order],
                       text=[f"{scores[i]:.1f}" + ("" if kept[i] else "  dropped") for i in order],
                       textposition="outside", textfont=dict(color=[GREY if kept[i] else RED for i in order])))
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, showlegend=False,
                  xaxis=dict(title="chi-squared score (higher = more linked to Survived)",
                             range=[0, scores.max() * 1.3]), margin=dict(l=150, r=30, t=30, b=80))
fig.write_image(HERE / "chi2_scores.png", scale=1.5)

# 2. the five folds of cross_val_score(pipe, cv=5)
cv = cross_val_score(pipe, X_train, y_train, cv=5, scoring="accuracy")
assert round(cv.mean(), 3) == 0.787
fig = go.Figure()
for k in range(5):
    for part in range(5):
        test = part == k
        fig.add_trace(go.Bar(x=[1], y=[f"fold {k + 1}"], base=part, orientation="h", width=0.7,
                             marker=dict(color=ORANGE if test else BLUE, line=dict(color="white", width=3)),
                             showlegend=False, hoverinfo="skip"))
    fig.add_annotation(x=5.1, y=f"fold {k + 1}", text=f"{cv[k]:.1%}", showarrow=False, xanchor="left")
fig.add_annotation(x=2.5, y=-1.0, text=f"mean accuracy {cv.mean():.1%}", showarrow=False, font=dict(size=26))
for c, t in ((BLUE, "fit the whole pipeline (4 parts)"), (ORANGE, "test it (1 part)")):
    fig.add_trace(go.Bar(x=[None], y=[None], marker_color=c, name=t))
fig.update_layout(template="simple_white", width=1000, height=520, font=FONT, barmode="overlay",
                  xaxis=dict(visible=False, range=[0, 6]), yaxis=dict(autorange="reversed", range=[-1.4, 4.5]),
                  legend=dict(orientation="h", x=0, y=1.12), margin=dict(l=100, r=20, t=60, b=20))
fig.write_image(HERE / "cv_folds.png", scale=1.5)

# 3. tuning trf5__max_depth with GridSearchCV
depths = [1, 2, 3, 4, 5, None]
grid = GridSearchCV(pipe, {"trf5__max_depth": depths}, cv=5, scoring="accuracy").fit(X_train, y_train)
m = grid.cv_results_["mean_test_score"]
assert grid.best_params_ == {"trf5__max_depth": 3} and round(grid.best_score_, 3) == 0.803
assert round(grid.score(X_test, y_test), 3) == 0.793
labels = [str(d) if d else "None (no limit)" for d in depths]
fig = go.Figure(go.Scatter(x=labels, y=m, mode="lines+markers+text", text=[f"{v:.1%}" for v in m],
                           textposition=["top center", "bottom center", "top center", "bottom center", "top center", "top center"], line=dict(color=BLUE, width=3),
                           marker=dict(size=14, color=[RED if d == 3 else BLUE for d in depths])))
fig.add_annotation(x=2, y=m[2], text="best: depth 3", showarrow=True, ay=-55, ax=160, font=dict(color=RED))
fig.update_layout(template="simple_white", width=1000, height=520, font=FONT,
                  xaxis=dict(title="trf5__max_depth"), yaxis=dict(title="mean CV accuracy", tickformat=".0%",
                                                                 range=[m.min() - 0.02, m.max() + 0.02]),
                  margin=dict(l=110, r=30, t=30, b=80))
fig.write_image(HERE / "depth_tuning.png", scale=1.5)
print(dict(zip(names, scores.round(1))), cv.round(3), m.round(3))
