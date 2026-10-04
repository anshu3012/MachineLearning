"""Section 5: the forest built by hand. Three sampling settings x three trees, each cell one tree's vote for the
query (observation 7, true class 0), with the features and depth it got; the right column is the majority.
Same data, seed and draw order as the Notebook. (Plotly)"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
X, y = make_classification(n_samples=100, n_features=5, n_redundant=0, n_informative=5, n_clusters_per_class=1,
                           random_state=4)
df = pd.DataFrame(X, columns=["col1", "col2", "col3", "col4", "col5"]).round(3)
df["target"] = y
rng = np.random.default_rng(4)
query = df.iloc[[7]]


def sample_rows(d, share):
    return d.sample(int(share * len(d)), replace=True, random_state=rng.integers(10**9))


def sample_features(d, share):
    cols = list(rng.choice(d.columns[:-1], int(share * (d.shape[1] - 1)), replace=False))
    return d[cols + ["target"]]


SETTINGS = [("row sampling<br>20 obs., all 5 features", lambda: sample_rows(df, 0.2)),
            ("column sampling<br>100 obs., 4 features", lambda: sample_features(df, 0.8)),
            ("combined<br>50 obs., 2 features", lambda: sample_features(sample_rows(df, 0.5), 0.5))]
rows = []
for name, make in SETTINGS:                              # same order as the Notebook, so the same draws
    cells = []
    for _ in range(3):
        d = make()
        inputs = d.columns[:-1]
        tree = DecisionTreeClassifier(random_state=0).fit(d[inputs], d["target"])
        cells.append((int(tree.predict(query[inputs])[0]), tree.get_depth(), list(inputs)))
    rows.append((name, cells))
votes = [[c[0] for c in cells] for _, cells in rows]
depths = [[c[1] for c in cells] for _, cells in rows]
assert int(query["target"].iloc[0]) == 0
assert votes == [[1, 0, 0], [0, 0, 0], [0, 0, 1]], votes
assert depths == [[2, 2, 2], [6, 3, 3], [4, 5, 6]], depths
print(votes, depths)

C = {0: "#4C78A8", 1: "#F58518"}
fig = go.Figure()
for r, (name, cells) in enumerate(rows):
    yy = 2 - r
    for k, (v, dep, inp) in enumerate(cells):
        feats = "all 5 features" if len(inp) == 5 else ", ".join(inp)
        fig.add_shape(type="rect", x0=k + 0.05, x1=k + 0.95, y0=yy + 0.06, y1=yy + 0.94, fillcolor=C[v], opacity=0.85,
                      line=dict(color="black", width=4 if v == 1 else 0))
        fig.add_annotation(x=k + 0.5, y=yy + 0.62, text=f"<b>tree {k + 1} votes {v}</b>", showarrow=False,
                           font=dict(color="white", size=22))
        fig.add_annotation(x=k + 0.5, y=yy + 0.3, text=f"{feats}<br>depth {dep}", showarrow=False,
                           font=dict(color="white", size=16))
    maj = max(set(votes[r]), key=votes[r].count)
    fig.add_shape(type="rect", x0=3.25, x1=4.15, y0=yy + 0.06, y1=yy + 0.94, fillcolor=C[maj], opacity=1, line=dict(width=0), layer="above")
    fig.add_annotation(x=3.7, y=yy + 0.5, text=f"<b>majority: {maj}</b><br>{votes[r].count(maj)} of 3 votes",
                       showarrow=False, font=dict(color="white", size=21))
    fig.add_annotation(x=-0.08, y=yy + 0.5, text=name, showarrow=False, xanchor="right", font=dict(size=19))
fig.add_annotation(x=1.5, y=3.18, text="three trees, each on its own random subset", showarrow=False, font=dict(size=21))
fig.add_annotation(x=3.7, y=3.18, text="the forest", showarrow=False, font=dict(size=21))
fig.update_xaxes(visible=False, range=[-1.3, 4.2])
fig.update_yaxes(visible=False, range=[-0.05, 3.35])
fig.update_layout(template="simple_white", width=1350, height=640, font=dict(family="Latin Modern Roman", size=18),
                  margin=dict(l=10, r=10, t=10, b=10))
fig.write_image(HERE / "hand_votes.png", scale=2)
fig.write_image(HERE / "hand_votes.pdf")
