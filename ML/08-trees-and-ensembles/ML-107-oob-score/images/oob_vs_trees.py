"""Heart disease data: OOB score against test accuracy as the number of trees grows (Plotly)."""
import warnings
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
X, y = df.iloc[:, :-1], df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
ns = [5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500]
oob, test = [], []
for n in ns:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")      # with 5 trees a few rows have no OOB prediction (scikit-learn warns)
        rf = RandomForestClassifier(n_estimators=n, oob_score=True, random_state=42, n_jobs=-1).fit(X_train, y_train)
    oob.append(rf.oob_score_)
    test.append(rf.score(X_test, y_test))
print([round(v, 3) for v in oob], [round(v, 3) for v in test])
fig = go.Figure([go.Scatter(x=ns, y=oob, mode="lines+markers", name="OOB score (242 training rows)",
                            line=dict(color="#F58518", width=3), marker=dict(size=9)),
                 go.Scatter(x=ns, y=test, mode="lines+markers", name="test accuracy (61 test rows)",
                            line=dict(color="#4C78A8", width=3, dash="dash"), marker=dict(size=9))])
fig.update_xaxes(title="number of trees (n_estimators)", type="log", tickvals=ns)
fig.update_yaxes(title="accuracy", range=[0.65, 0.9])
fig.update_layout(template="simple_white", width=1100, height=520, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=80, r=20, t=30, b=70), legend=dict(x=0.45, y=0.08))
fig.write_image(HERE / "oob_vs_trees.png", scale=2)
fig.write_image(HERE / "oob_vs_trees.pdf")
