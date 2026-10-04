"""The best score of a grid is a little lucky (Plotly), the Notebook's Boston grid: the 90 settings' cross-validated
R2 on the grid's 5 folds, sorted (bars), the winner at 0.725, and the same winning setting re-scored on 10 fresh
shuffles of 5-fold CV (RepeatedKFold, random_state 0): 0.663."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.model_selection import GridSearchCV, RepeatedKFold, cross_val_score, train_test_split
from sklearn.tree import DecisionTreeRegressor
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
b = pd.read_csv(here.parent / "data" / "boston.csv")
X, y = b.drop(columns="MEDV"), b["MEDV"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
params = {"max_depth": [2, 4, 6, 8, None], "criterion": ["squared_error", "absolute_error"],
          "max_features": [0.25, 0.5, 1.0], "min_samples_split": [2, 0.05, 0.25]}
grid = GridSearchCV(DecisionTreeRegressor(random_state=42), params, cv=5).fit(Xtr, ytr)
scores = np.sort(grid.cv_results_["mean_test_score"])
fresh = cross_val_score(DecisionTreeRegressor(random_state=42, **grid.best_params_), Xtr, ytr,
                        cv=RepeatedKFold(n_splits=5, n_repeats=10, random_state=0)).mean()
assert len(scores) == 90 and round(grid.best_score_, 3) == 0.725 and round(fresh, 3) == 0.663
fig = go.Figure(go.Bar(x=np.arange(1, 91), y=scores, marker_color=[ORANGE if i == 89 else GREY for i in range(90)],
                       name="the 90 settings on the grid's 5 folds"))
fig.add_hline(y=fresh, line=dict(color=BLUE, width=3, dash="dash"), opacity=1)
fig.add_annotation(x=90, y=scores[-1], text=f"winner on the same folds: {scores[-1]:.3f}", ax=-170, ay=-35,
                   font=dict(size=19, color=ORANGE), arrowcolor=ORANGE)
fig.add_annotation(x=5, y=fresh, text=f"same winner on 10 fresh shuffles of the folds: {fresh:.3f}", showarrow=False,
                   xanchor="left", yshift=16, font=dict(size=19, color=BLUE))
fig.update_layout(template="simple_white", width=1050, height=540, font=FONT, showlegend=False,
                  xaxis=dict(title="the 90 grid settings, sorted by cross-validated R²"), yaxis=dict(title="cross-validated R²", range=[0, 0.85]),
                  margin=dict(l=80, r=30, t=30, b=70))
fig.write_image(here / "selection_bias.png", scale=2)
