"""Heart data, section 6.4: is the grid-tuned forest really better? Nested cross-validation, 5 outer folds x 4 repeats.
For each of the 20 outer folds: the default forest's score, the grid-tuned forest's score (both on data the search
never saw), and the grid's own best inner score (optimistic). The 20 grid searches run once, on topgro, and are
cached in nested_cv.json; delete the json to recompute. (Plotly)"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold, cross_validate

HERE = Path(__file__).parent
CACHE = HERE / "nested_cv.json"
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
X, y = df.iloc[:, :-1], df.iloc[:, -1]
param_grid = {"n_estimators": [20, 60, 100, 120], "max_features": [0.2, 0.6, 1.0], "max_depth": [2, 8, None],
              "max_samples": [0.5, 0.75, 1.0]}

if not CACHE.exists():                                   # same code as the Notebook
    outer = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=0)
    default = cross_validate(RandomForestClassifier(random_state=42, n_jobs=-1), X, y, cv=outer)["test_score"]
    nested = cross_validate(GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, n_jobs=-1),
                            X, y, cv=outer, return_estimator=True)
    CACHE.write_text(json.dumps(dict(default=default.tolist(), tuned=nested["test_score"].tolist(),
                                     inner=[float(s.best_score_) for s in nested["estimator"]])))
d = {k: np.array(v) for k, v in json.loads(CACHE.read_text()).items()}
default, tuned, inner = d["default"], d["tuned"], d["inner"]
assert [round(v.mean(), 3) for v in (default, tuned, inner)] == [0.819, 0.814, 0.845]
assert int((tuned > default).sum()) == 5 and int((tuned == default).sum()) == 5
print(default.mean(), tuned.mean(), inner.mean())

k = np.arange(1, 21)
fig = go.Figure()
for i in range(20):                                       # one grey line per outer fold: default -> tuned
    fig.add_trace(go.Scatter(x=[default[i], tuned[i]], y=[k[i]] * 2, mode="lines", showlegend=False,
                             line=dict(color="#CCCCCC", width=2)))
for v, name, c, sym in [(inner, "the grid's own best score (optimistic)", "#E45756", "x"),
                        (default, "default forest, unseen fold", "#4C78A8", "circle"),
                        (tuned, "grid-tuned forest, unseen fold", "#F58518", "diamond")]:
    fig.add_trace(go.Scatter(x=v, y=k, mode="markers", name=f"{name}: mean {v.mean():.3f}",
                             marker=dict(color=c, size=13, symbol=sym)))
    fig.add_vline(x=v.mean(), line=dict(color=c, width=2, dash="dash"))
fig.update_xaxes(title="accuracy")
fig.update_yaxes(title="outer fold", tickvals=[1, 5, 10, 15, 20], range=[0, 21])
fig.update_layout(template="simple_white", width=1100, height=820, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=80, r=20, t=150, b=70), legend=dict(x=0, y=1.02, yanchor="bottom"))
fig.write_image(HERE / "nested_cv.png", scale=2)
fig.write_image(HERE / "nested_cv.pdf")
