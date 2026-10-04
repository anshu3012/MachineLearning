"""Impurity-based importance against permutation importance, with two useless columns added: a random number for every
row (high cardinality) and a random coin flip (two values) (Plotly)."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
X, y = make_classification(n_samples=1000, n_features=4, n_informative=3, n_redundant=1, flip_y=0.1, random_state=0)
df = pd.DataFrame(X.round(1), columns=["x1", "x2", "x3", "x4"])
rng = np.random.default_rng(0)
df["random_id"] = rng.permutation(len(df))             # 1,000 different values, no link to y
df["random_coin"] = rng.integers(0, 2, len(df))        # 2 values, no link to y
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.3, random_state=0)
rf = RandomForestClassifier(random_state=0, n_jobs=-1).fit(X_train, y_train)
perm = permutation_importance(rf, X_test, y_test, n_repeats=20, random_state=0, n_jobs=-1)
cols = list(df.columns)[::-1]                          # first column at the top
mdi = pd.Series(rf.feature_importances_, df.columns)[cols]
pm = pd.Series(perm.importances_mean, df.columns)[cols]
ps = pd.Series(perm.importances_std, df.columns)[cols]
print(mdi.round(3).to_dict(), pm.round(3).to_dict())
colours = ["#E45756" if c.startswith("random") else "#4C78A8" for c in cols]
fig = make_subplots(1, 2, shared_yaxes=True, horizontal_spacing=0.05,
                    subplot_titles=["(a) impurity-based (feature_importances_)",
                                    "(b) permutation importance on the test set"])
fig.add_trace(go.Bar(x=mdi, y=cols, orientation="h", marker_color=colours, text=[f"{v:.3f}" for v in mdi],
                     textposition="outside"), 1, 1)
fig.add_trace(go.Bar(x=pm, y=cols, orientation="h", marker_color=colours,
                     error_x=dict(type="data", array=ps, color="#6B6B6B")), 1, 2)
for c in cols:                                         # value labels just past the error bar
    fig.add_annotation(x=max(pm[c], 0) + ps[c] + 0.006, y=c, text=f"{pm[c]:.3f}", showarrow=False, xanchor="left",
                       xref="x2", yref="y2")
fig.update_xaxes(range=[0, 0.33], title="share of impurity decrease", col=1)
fig.update_xaxes(range=[-0.02, 0.27], title="drop in test accuracy", col=2)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1300, height=540, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=20, r=20, t=50, b=60))
fig.write_image(HERE / "mdi_vs_permutation.png", scale=2)
fig.write_image(HERE / "mdi_vs_permutation.pdf")
