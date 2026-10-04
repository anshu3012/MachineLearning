"""The weights search of section 4.3 as a picture (Plotly): soft-vote accuracy on the heart disease data for
every weight triple (logistic regression, random forest, KNN), each weight from 1 to 3: 27 combinations, scored
by the same repeated stratified 10-fold cross-validation (5 shuffles). The best cell, (3, 3, 2), is outlined.
Each model is fitted once per fold; the 27 weighted averages of their probabilities are then computed from
those fits, which is what VotingClassifier(voting="soft", weights=...) does. Scores are cached in
data/weights_grid.csv."""
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
CSV = HERE.parent / "data" / "weights_grid.csv"


def compute():
    from sklearn.base import clone
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    heart = pd.read_csv(HERE.parent / "data" / "heart.csv", encoding="utf-8-sig")
    X, y = heart.drop(columns="target"), heart["target"].to_numpy()
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=5, random_state=0)
    est = [make_pipeline(StandardScaler(), LogisticRegression()), RandomForestClassifier(random_state=42),
           make_pipeline(StandardScaler(), KNeighborsClassifier())]
    triples = list(product([1, 2, 3], repeat=3))
    acc = {t: [] for t in triples}
    for tr, te in cv.split(X, y):
        proba = [clone(m).fit(X.iloc[tr], y[tr]).predict_proba(X.iloc[te]) for m in est]
        for t in triples:
            avg = sum(w * p for w, p in zip(t, proba)) / sum(t)
            acc[t].append((avg.argmax(axis=1) == y[te]).mean())
    return pd.DataFrame([(*t, np.mean(a)) for t, a in acc.items()], columns=["lr", "rf", "knn", "accuracy"])


if __name__ == "__main__":
    if not CSV.exists():
        compute().to_csv(CSV, index=False)
    df = pd.read_csv(CSV)
    get = lambda i, j, k: df[(df.lr == i) & (df.rf == j) & (df.knn == k)].accuracy.iloc[0]
    assert round(get(1, 1, 1), 3) == 0.841 and round(get(3, 3, 2), 3) == 0.844          # section 4.3
    best = df.loc[df.accuracy.idxmax()]
    assert (best.lr, best.rf, best.knn) == (3, 3, 2)
    print(df.sort_values("accuracy", ascending=False).head(5), df.accuracy.min())
    fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06,
                        subplot_titles=[f"KNN weight = {k}" for k in (1, 2, 3)])
    for c, k in enumerate((1, 2, 3), 1):
        z = [[get(i, j, k) for i in (1, 2, 3)] for j in (1, 2, 3)]            # rows: rf weight, columns: lr weight
        fig.add_trace(go.Heatmap(z=z, x=["1", "2", "3"], y=["1", "2", "3"], zmin=df.accuracy.min(),
                                 zmax=df.accuracy.max(), colorscale="Greens", showscale=False, xgap=3, ygap=3,
                                 text=[[f"{v:.3f}" for v in row] for row in z], texttemplate="%{text}",
                                 textfont=dict(size=24)), 1, c)
        fig.update_xaxes(title="logistic regression weight", type="category", row=1, col=c)
    fig.update_yaxes(title="random forest weight", type="category", row=1, col=1)
    fig.update_yaxes(type="category")
    fig.add_shape(type="rect", xref="x2", yref="y2", x0=1.5, x1=2.5, y0=1.5, y1=2.5, line=dict(color="#E45756", width=7), fillcolor="rgba(0,0,0,0)", layer="above")
    fig.add_shape(type="rect", xref="x", yref="y", x0=-0.5, x1=0.5, y0=-0.5, y1=0.5,
                  line=dict(color="black", width=5, dash="dash"), fillcolor="rgba(0,0,0,0)", layer="above")
    fig.add_annotation(xref="paper", yref="paper", x=0.5, y=-0.42, showarrow=False, font=dict(size=24),
                       text="red: best weights (3, 3, 2), 0.844 &nbsp;&nbsp;&nbsp; dashed: equal weights (1, 1, 1), 0.841")
    fig.update_layout(template="simple_white", width=1300, height=560,
                      font=dict(family="Latin Modern Roman", size=22, color="black"),
                      margin=dict(l=90, r=20, t=60, b=150))
    fig.update_annotations(selector=lambda a: a.y is not None and a.y > 0.9, font_size=26)
    fig.write_image(HERE / "weights_grid.png", scale=2)
    fig.write_image(HERE / "weights_grid.pdf")
