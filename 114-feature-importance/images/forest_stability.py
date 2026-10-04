"""Section 5: why the forest averages its trees. The notebook's stability test on the section 6 data: 20 bootstrap
resamples of the 700 training observations; on each, one decision tree and one random forest are trained.
Each dot is one resample's importance of a feature: one tree (left) against the forest (right).
Run: python forest_stability.py  -> forest_stability.png (Plotly)"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
X, y = make_classification(n_samples=1000, n_features=4, n_informative=3, n_redundant=1, flip_y=0.1, random_state=0)
df = pd.DataFrame(X.round(1), columns=["x1", "x2", "x3", "x4"])
rng = np.random.default_rng(0)
df["random_id"] = rng.permutation(len(df))
df["random_coin"] = rng.integers(0, 2, len(df))
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.3, random_state=0)
r = np.random.default_rng(2)                                  # same loop as the notebook
tree_imp, forest_imp = [], []
for k in range(20):
    idx = r.choice(len(X_train), len(X_train), replace=True)
    tree_imp.append(DecisionTreeClassifier(random_state=k).fit(X_train.iloc[idx], y_train[idx]).feature_importances_)
    forest_imp.append(RandomForestClassifier(random_state=k, n_jobs=-1).fit(X_train.iloc[idx], y_train[idx])
                      .feature_importances_)
tree_imp, forest_imp = np.array(tree_imp), np.array(forest_imp)
ratio = forest_imp.std(axis=0).mean() / tree_imp.std(axis=0).mean()
print("std one tree", tree_imp.std(axis=0).round(3), "forest", forest_imp.std(axis=0).round(3), "ratio", ratio.round(2))
assert round(ratio, 2) == 0.25 and round(tree_imp.std(axis=0).mean(), 3) == 0.043 and round(forest_imp.std(axis=0).mean(), 3) == 0.011

cols = list(df.columns)
fig = make_subplots(1, 2, shared_yaxes=True, horizontal_spacing=0.04,
                    subplot_titles=(f"one decision tree", f"random forest (100 trees)"))
jit = np.random.default_rng(0).uniform(-0.18, 0.18, 20)
for col, imp, c in ((1, tree_imp, "#E45756"), (2, forest_imp, "#4C78A8")):
    for j, name in enumerate(cols):
        fig.add_trace(go.Scatter(x=imp[:, j], y=len(cols) - 1 - j + jit, mode="markers", showlegend=False,
                                 marker=dict(color=c, size=9, opacity=0.75)), 1, col)
fig.update_yaxes(tickvals=list(range(len(cols))), ticktext=cols[::-1], range=[-0.5, len(cols) - 0.5], col=1)
fig.update_xaxes(title="feature importance", range=[-0.01, 0.55])
fig.update_annotations(font_size=22)
fig.update_layout(template="simple_white", width=1200, height=520, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=20, r=20, t=50, b=70))
fig.write_image(HERE / "forest_stability.png", scale=2)
fig.write_image(HERE / "forest_stability.pdf")
