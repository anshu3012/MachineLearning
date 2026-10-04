"""Plotly chart for Note 39: error of the filled Titanic ages (hidden known ages) for k = 1..20, KNN vs mean imputation."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"

df = pd.read_csv(here.parent / "data" / "titanic_knn.csv")
known = df.loc[df["Age"].notna(), ["Age", "Pclass", "Fare", "SibSp", "Parch"]].reset_index(drop=True)


def fill_error(k=None, weights="uniform"):
    # same experiment as section 7 of the Notebook: hide 20% of known ages, fill, mean absolute error, 20 seeds
    errors = []
    for s in range(20):
        tr, te = train_test_split(known, test_size=0.2, random_state=s)
        hidden = te.copy()
        hidden["Age"] = np.nan
        if k is None:
            filled = np.full(len(te), tr["Age"].mean())
        else:
            sc = StandardScaler().fit(tr)
            imp = KNNImputer(n_neighbors=k, weights=weights).fit(sc.transform(tr))
            filled = sc.inverse_transform(imp.transform(sc.transform(hidden)))[:, 0]
        errors.append(mean_absolute_error(te["Age"], filled))
    return np.mean(errors)


ks = [1, 2, 3, 5, 7, 10, 15, 20]
fig = go.Figure()
for w, colour, dash in [("uniform", BLUE, "solid"), ("distance", ORANGE, "dash")]:
    fig.add_trace(go.Scatter(x=ks, y=[fill_error(k, w) for k in ks], name=f"KNN, {w}",
                             mode="lines+markers", line=dict(color=colour, width=3, dash=dash), marker_size=9))
mean_err = fill_error(None)
fig.add_hline(y=mean_err, line=dict(color=GREY, width=2, dash="dot"))
fig.add_annotation(x=20, y=mean_err, text=f"mean imputation {mean_err:.2f}", showarrow=False, yshift=16,
                   xanchor="right", font=dict(color=GREY, size=18))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=80, r=20, t=30, b=70), legend=dict(x=0.98, xanchor="right", y=0.80),
                  xaxis=dict(title="n_neighbors (k)", tickvals=ks),
                  yaxis=dict(title="error of filled age (years)"))
fig.write_image(here / "fill_error_vs_k.png", scale=2)
fig.write_image(here / "fill_error_vs_k.pdf")
