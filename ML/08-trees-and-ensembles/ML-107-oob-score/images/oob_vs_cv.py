"""Section 4: the notebook's 50 random splits of the heart disease data (500 trees each). For every split, the OOB
score (x) against the 5-fold cross-validation score (blue) and against the 61-patient test accuracy (grey).
Blue points hug the diagonal (OOB = CV); grey points scatter (the small test set is the noisy estimate).
Heavy (300 forests of 500 trees): run on topgro with tools/remote_run.sh ML/08-trees-and-ensembles/ML-107-oob-score "cd images && python oob_vs_cv.py"
Run: python oob_vs_cv.py  -> oob_vs_cv.png (Plotly)"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
X, y = df.iloc[:, :-1], df.iloc[:, -1]
results = []
for seed in range(50):                                         # same loop as the notebook
    a, b, c, d = train_test_split(X, y, test_size=0.2, random_state=seed)
    forest = RandomForestClassifier(n_estimators=500, oob_score=True, random_state=seed, n_jobs=-1).fit(a, c)
    cv5 = cross_val_score(RandomForestClassifier(n_estimators=500, random_state=seed, n_jobs=-1), a, c, cv=5).mean()
    results.append((forest.oob_score_, forest.score(b, d), cv5))
oob, test, cv = np.array(results).T
gap_cv, gap_test = np.abs(oob - cv).mean(), np.abs(oob - test).mean()
print("means", oob.mean().round(3), cv.mean().round(3), test.mean().round(3), "gaps", gap_cv.round(3), gap_test.round(3))
assert (round(oob.mean(), 3), round(cv.mean(), 3), round(test.mean(), 3)) == (0.820, 0.820, 0.831)
assert round(gap_cv, 3) == 0.011 and round(gap_test, 3) == 0.038

fig = go.Figure([go.Scatter(x=[0.7, 0.95], y=[0.7, 0.95], mode="lines", line=dict(color="black", dash="dash", width=2),
                            name="equal to the OOB score"),
                 go.Scatter(x=oob, y=test, mode="markers", name=f"test accuracy, 61 patients (gap {gap_test:.3f})",
                            marker=dict(color="#9A9A9A", size=12, symbol="circle-open", line_width=2)),
                 go.Scatter(x=oob, y=cv, mode="markers", name=f"5-fold cross-validation (gap {gap_cv:.3f})",
                            marker=dict(color="#4C78A8", size=11))])
fig.update_xaxes(title="OOB score of the split", range=[0.72, 0.9])
fig.update_yaxes(title="other estimate", range=[0.7, 0.95], scaleanchor="x")
fig.update_layout(template="simple_white", width=900, height=800, font=dict(family="Latin Modern Roman", size=21),
                  title=dict(text="50 random splits of the heart disease data", x=0.5),
                  margin=dict(l=80, r=20, t=60, b=70), legend=dict(x=0.02, y=0.99, bgcolor="rgba(255,255,255,0.8)"))
fig.write_image(HERE / "oob_vs_cv.png", scale=2)
fig.write_image(HERE / "oob_vs_cv.pdf")
