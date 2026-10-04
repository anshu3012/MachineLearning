"""Section 7.2: the 10 combinations a naive RandomizedSearchCV draws from one big grid. Those that pair bootstrap=False
with a max_samples value fail (score NaN), so only half the search does any work. (Plotly)"""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split

warnings.filterwarnings("ignore")                       # the failed fits warn; the figure shows them instead
HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
X, y = df.iloc[:, :-1], df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
param_grid = {"n_estimators": [20, 60, 100, 120], "max_features": [0.2, 0.6, 1.0], "max_depth": [2, 8, None],
              "max_samples": [0.5, 0.75, 1.0]}
big_grid = dict(param_grid, bootstrap=[True, False], min_samples_split=[2, 5], min_samples_leaf=[1, 2])
naive = RandomizedSearchCV(RandomForestClassifier(random_state=42), big_grid, cv=5, n_jobs=-1, random_state=42,
                           error_score=np.nan).fit(X_train, y_train)
res = pd.DataFrame(naive.cv_results_)
failed = res["mean_test_score"].isna()
assert int(failed.sum()) == 5                                        # the Note: 5 of the 10 failed
assert (res.loc[failed, "param_bootstrap"] == False).all()           # every failure is bootstrap=False  # noqa: E712
print(res[["param_bootstrap", "param_max_samples", "mean_test_score"]])

fig = go.Figure()
for i, r in res.iterrows():
    ok = not np.isnan(r["mean_test_score"])
    label = f"bootstrap={r['param_bootstrap']}, max_samples={r['param_max_samples']}"
    fig.add_trace(go.Bar(x=[r["mean_test_score"] if ok else 0.9], y=[f"draw {i + 1}"], orientation="h", showlegend=False,
                         marker_color="#4C78A8" if ok else "#F6C6C6",
                         text=[f"{r['mean_test_score']:.3f}   {label}" if ok else f"FAILED, no score (NaN)   {label}"],
                         textposition="inside", insidetextanchor="start", textfont=dict(size=19, color="white" if ok else "#8B0000")))
fig.update_xaxes(title="cross-validated accuracy", range=[0, 0.9])
fig.update_yaxes(autorange="reversed")
fig.update_layout(template="simple_white", width=1100, height=620, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=100, r=20, t=20, b=70), bargap=0.25)
fig.write_image(HERE / "search_trap.png", scale=2)
fig.write_image(HERE / "search_trap.pdf")
