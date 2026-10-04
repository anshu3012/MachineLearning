"""Section 5: the out-of-bag table of the Note's forest (heart disease data, 242 training observations,
RandomForestClassifier(oob_score=True, random_state=42), 100 trees), built from estimators_samples_.
Top: one row per tree, one column per observation; orange = the tree missed that observation.
Bottom: for each observation, the number of trees that missed it (its OOB voters).
Run: python oob_table.py  -> oob_table.png (Plotly)"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
X, y = df.iloc[:, :-1], df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf = RandomForestClassifier(oob_score=True, random_state=42).fit(X_train, y_train)
n_trees, n_rows = len(rf.estimators_), len(X_train)
in_bag = np.zeros((n_trees, n_rows), dtype=bool)
for t, rows in enumerate(rf.estimators_samples_):
    in_bag[t, rows] = True
oob = ~in_bag
per_row = oob.sum(axis=0)
# the Note's numbers (section 5)
assert round(oob.mean(), 3) == 0.367 and per_row.min() == 24 and per_row.max() == 47 and round(per_row.mean(), 1) == 36.7
assert (round(oob.mean(axis=1).min(), 2), round(oob.mean(axis=1).max(), 2)) == (0.32, 0.41)   # per-tree OOB share
assert round(rf.oob_score_, 3) == 0.835

fig = make_subplots(2, 1, row_heights=[0.68, 0.32], shared_xaxes=True, vertical_spacing=0.06,
                    subplot_titles=("each tree (row) misses about 37% of the observations (orange)",
                                    "each observation is missed by 24 to 47 trees"))
fig.add_trace(go.Heatmap(z=oob.astype(int), colorscale=[[0, "#DCE6F2"], [1, "#F58518"]], showscale=False,
                         x=np.arange(1, n_rows + 1), y=np.arange(1, n_trees + 1)), 1, 1)
fig.add_trace(go.Bar(x=np.arange(1, n_rows + 1), y=per_row, marker_color="#F58518", marker_line_width=0), 2, 1)
fig.add_hline(y=per_row.mean(), line=dict(color="black", dash="dash", width=2), row=2, col=1)
fig.add_annotation(x=n_rows, xanchor="right", y=per_row.mean() + 9, xref="x2", yref="y2",
                   text=f"mean {per_row.mean():.1f}", showarrow=False, font_size=18, bgcolor="white")
fig.update_yaxes(title="tree", autorange="reversed", row=1, col=1)
fig.update_yaxes(title="trees that<br>missed it", range=[0, 60], row=2, col=1)
fig.update_xaxes(title="training observation", row=2, col=1)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1100, height=700, font=dict(family="Latin Modern Roman", size=19),
                  margin=dict(l=90, r=20, t=50, b=70), showlegend=False)
fig.write_image(HERE / "oob_table.png", scale=2)
fig.write_image(HERE / "oob_table.pdf")
