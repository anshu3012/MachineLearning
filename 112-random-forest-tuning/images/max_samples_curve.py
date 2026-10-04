"""Heart data, section 5: fewer observations per tree -> trees less alike -> a slightly better forest.
Left: mean 10-fold CV accuracy (20 runs, 500 trees) against max_samples, each run a faint dot.
Right: average correlation between two trees' predicted probabilities on the 61 test patients.
The heavy part (100 cross-validations of 500-tree forests) runs once, on topgro, and is cached in
max_samples_curve.json; delete the json to recompute. (Plotly)"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

HERE = Path(__file__).parent
CACHE = HERE / "max_samples_curve.json"
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
X, y = df.iloc[:, :-1], df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
SHARES = [None, 0.75, 0.5, 0.3, 0.2]


def tree_correlation(share):
    forest = RandomForestClassifier(n_estimators=500, max_samples=share, random_state=0).fit(X_train, y_train)
    p = np.array([t.predict_proba(X_test.values)[:, 1] for t in forest.estimators_])
    c = np.corrcoef(p)
    return float(c[np.triu_indices_from(c, k=1)].mean())


if not CACHE.exists():                                   # same code as the Notebook
    runs = {str(s): [float(cross_val_score(RandomForestClassifier(n_estimators=500, max_samples=s, random_state=seed,
                                                                  n_jobs=-1), X, y,
                                           cv=StratifiedKFold(10, shuffle=True, random_state=seed)).mean())
                     for seed in range(20)] for s in SHARES}
    CACHE.write_text(json.dumps(dict(runs=runs, corr={str(s): tree_correlation(s) for s in (None, 0.2)})))
d = json.loads(CACHE.read_text())
runs = {k: np.array(v) for k, v in d["runs"].items()}
means = [round(runs[str(s)].mean(), 3) for s in SHARES]
assert means == [0.826, 0.825, 0.829, 0.833, 0.834], means          # the Note's table
assert int((runs["0.2"] > runs["None"]).sum()) == 16                # 20% beats all in 16 of 20 runs
corr = [round(d["corr"][k], 2) for k in ("None", "0.2")]
assert corr == [0.44, 0.34], corr
print(means, corr)

labels = ["all", "75%", "50%", "30%", "20%"]
fig = make_subplots(1, 2, column_widths=[0.68, 0.32], horizontal_spacing=0.12,
                    subplot_titles=["(a) mean cross-validated accuracy", "(b) how alike two trees are"])
rng = np.random.default_rng(0)
for i, s in enumerate(SHARES):
    r = runs[str(s)]
    fig.add_trace(go.Scatter(x=i + rng.uniform(-0.12, 0.12, len(r)), y=r, mode="markers", showlegend=i == 0,
                             name="one run (new folds, new forest)", marker=dict(color="#BBBBBB", size=8)), 1, 1)
fig.add_trace(go.Scatter(x=list(range(5)), y=means, mode="lines+markers", name="mean of 20 runs",
                         line=dict(color="#4C78A8", width=4), marker=dict(size=13)), 1, 1)
for i, m in enumerate(means):
    fig.add_annotation(x=i, y=0.8515, text=f"<b>mean {m:.3f}</b>", showarrow=False,
                       font=dict(size=20, color="#4C78A8"), row=1, col=1)
fig.add_trace(go.Bar(x=["all", "20%"], y=corr, text=[f"{c:.2f}" for c in corr], textposition="outside",
                     marker_color=["#4C78A8", "#F58518"], showlegend=False), 1, 2)
fig.update_xaxes(tickvals=list(range(5)), ticktext=labels, title="observations per tree (max_samples)", row=1, col=1)
fig.update_xaxes(title="observations per tree", row=1, col=2)
fig.update_yaxes(title="accuracy", range=[0.8, 0.853], row=1, col=1)
fig.update_yaxes(title="average correlation", range=[0, 0.55], row=1, col=2)
fig.update_annotations(font_size=22)
fig.update_layout(template="simple_white", width=1300, height=560, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=80, r=20, t=60, b=80), legend=dict(x=0.01, y=0.0, yanchor="bottom", bgcolor="rgba(255,255,255,0.8)"))
fig.write_image(HERE / "max_samples_curve.png", scale=2)
fig.write_image(HERE / "max_samples_curve.pdf")
