"""The hidden-age test of section 7.3 on one split (random_state = 0): 143 known ages are hidden and filled. Mean
imputation gives every hidden passenger the same age (a flat line); the KNN imputer (k = 10, features scaled) gives
each one an age from similar passengers, closer to the truth on average. Same code as the Notebook's fill_error."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_knn.csv")
known = df.loc[df["Age"].notna(), ["Age", "Pclass", "Fare", "SibSp", "Parch"]].reset_index(drop=True)
tr, te = train_test_split(known, test_size=0.2, random_state=0)
hidden = te.copy(); hidden["Age"] = np.nan
mean_fill = np.full(len(te), tr["Age"].mean())
sc = StandardScaler().fit(tr)
knn_fill = sc.inverse_transform(KNNImputer(n_neighbors=10).fit(sc.transform(tr)).transform(sc.transform(hidden)))[:, 0]
e_mean, e_knn = mean_absolute_error(te["Age"], mean_fill), mean_absolute_error(te["Age"], knn_fill)
assert len(known) == 714 and e_knn < e_mean
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.05, subplot_titles=[
    f"mean imputation: fill error {e_mean:.2f} years", f"KNN imputer, k = 10: fill error {e_knn:.2f} years"])
for c, f, col in ((1, mean_fill, "#4C78A8"), (2, knn_fill, "#F58518")):
    fig.add_scatter(x=te["Age"], y=f, mode="markers", marker=dict(size=8, color=col, opacity=0.7), row=1, col=c)
    fig.add_scatter(x=[0, 80], y=[0, 80], mode="lines", line=dict(color="#9a9a9a", dash="dash"), row=1, col=c)
    fig.update_xaxes(title_text="true age (hidden)", range=[0, 80], row=1, col=c)
fig.update_yaxes(title_text="filled age", range=[0, 80], row=1, col=1)
for a in fig.layout.annotations[:2]:
    a.font.size = 19
fig.update_layout(template="simple_white", width=1300, height=560, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=60, b=60))
fig.write_image(here / "hidden_ages.png", scale=2)
fig.write_image(here / "hidden_ages.pdf")
