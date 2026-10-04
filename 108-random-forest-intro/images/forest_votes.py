"""Section 5.4: RandomForestClassifier(random_state=42) on the same 100 observations; how its 100 trees vote on the
query point (observation 7, true class 0). (Plotly)"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

HERE = Path(__file__).parent
X, y = make_classification(n_samples=100, n_features=5, n_redundant=0, n_informative=5, n_clusters_per_class=1,
                           random_state=4)
df = pd.DataFrame(X, columns=["col1", "col2", "col3", "col4", "col5"]).round(3)
df["target"] = y
rf = RandomForestClassifier(random_state=42).fit(df.iloc[:, :5], df["target"])
q = df.iloc[[7], :5].to_numpy()
votes = np.array([int(t.predict(q)[0]) for t in rf.estimators_])
counts = np.bincount(votes, minlength=2)
assert len(votes) == 100 and rf.predict(df.iloc[[7], :5])[0] == 0
print("votes for class 0, 1:", counts, " forest proba:", rf.predict_proba(df.iloc[[7], :5])[0])
fig = go.Figure(go.Bar(x=["class 0 (true class)", "class 1"], y=counts, marker_color=["#4C78A8", "#F58518"],
                       text=[f"{c} trees" for c in counts], textposition="outside", textfont_size=22))
fig.update_yaxes(title="trees voting for the class", range=[0, 112])
fig.update_layout(template="simple_white", width=800, height=480, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=80, r=20, t=20, b=60), bargap=0.45)
fig.write_image(HERE / "forest_votes.png", scale=2)
fig.write_image(HERE / "forest_votes.pdf")
