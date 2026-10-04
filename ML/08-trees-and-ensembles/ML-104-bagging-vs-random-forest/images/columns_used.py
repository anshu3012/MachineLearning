"""How many of the 5 columns each tree actually splits on: 100 bagged trees (max_features=2, tree level) against the
100 trees of a random forest (max_features=2, node level) (Plotly)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_classification
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier

HERE = Path(__file__).parent
X, y = make_classification(n_features=5, n_redundant=0, n_informative=5, n_clusters_per_class=1, random_state=42)
bag = BaggingClassifier(n_estimators=100, max_features=2, random_state=42).fit(X, y)
rf = RandomForestClassifier(n_estimators=100, max_features=2, random_state=42).fit(X, y)


def n_columns(tree, cols):
    """Distinct original columns used by a tree's splits (leaves have feature -2); cols maps the tree's own columns."""
    f = tree.tree_.feature
    return len(set(np.asarray(cols)[f[f >= 0]]))


bag_counts = [n_columns(t, c) for t, c in zip(bag.estimators_, bag.estimators_features_)]
rf_counts = [n_columns(t, range(5)) for t in rf.estimators_]
ks = [1, 2, 3, 4, 5]
print("bagging", np.bincount(bag_counts, minlength=6)[1:], "random forest", np.bincount(rf_counts, minlength=6)[1:])
fig = go.Figure([go.Bar(x=ks, y=np.bincount(bag_counts, minlength=6)[1:], name="bagging (features drawn per tree)",
                        marker_color="#4C78A8", text=[v or "" for v in np.bincount(bag_counts, minlength=6)[1:]], textposition="outside"),
                 go.Bar(x=ks, y=np.bincount(rf_counts, minlength=6)[1:], name="random forest (features drawn per node)",
                        marker_color="#F58518", text=[v or "" for v in np.bincount(rf_counts, minlength=6)[1:]], textposition="outside")])
fig.update_xaxes(title="number of different features the tree splits on (out of 5)", tickvals=ks)
fig.update_yaxes(title="number of trees (out of 100)", range=[0, 112])
fig.update_layout(template="simple_white", barmode="group", width=1100, height=560,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=80, r=20, t=30, b=80),
                  legend=dict(x=0.45, y=0.98))
fig.write_image(HERE / "columns_used.png", scale=2)
fig.write_image(HERE / "columns_used.pdf")
