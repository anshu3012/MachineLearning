"""KNN (5 neighbours) on the Social Network Ads data, raw vs standardized: the regions it predicts 'bought' for,
with the 120 test users on top. Also checks the numbers drawn in the TikZ figures (z_number_line, fit_transform).
Run: python knn_regions.py -> knn_regions.png (Plotly)"""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
df = pd.read_csv(HERE.parent / "data" / "Social_Network_Ads.csv").iloc[:, 2:]
X_train, X_test, y_train, y_test = train_test_split(df.drop(columns="Purchased"), df["Purchased"],
                                                    test_size=0.3, random_state=0)
sc = StandardScaler().fit(X_train)
# numbers the Note and its TikZ figures quote
assert np.allclose(sc.mean_, [37.86, 69807.14], atol=0.01) and np.allclose(sc.scale_, [10.20, 34579.29], atol=0.01)
assert list(X_train.iloc[0]) == [26, 15000] and np.allclose(sc.transform(X_train)[:1], [[-1.16, -1.58]], atol=0.01)
assert (len(X_train), len(X_test)) == (280, 120)

raw = KNeighborsClassifier(n_neighbors=5).fit(X_train.values, y_train)
scl = KNeighborsClassifier(n_neighbors=5).fit(sc.transform(X_train), y_train)
acc_raw, acc_scl = raw.score(X_test.values, y_test), scl.score(sc.transform(X_test), y_test)
assert round(acc_raw, 3) == 0.825 and round(acc_scl, 3) == 0.917

ages, sal = np.linspace(17, 61, 220), np.linspace(10000, 155000, 220)
A, S = np.meshgrid(ages, sal)
grid = np.c_[A.ravel(), S.ravel()]
fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=(
    f"Raw data: accuracy {acc_raw:.1%}", f"Standardized: accuracy {acc_scl:.1%}"))
for col, model, g in ((1, raw, grid), (2, scl, sc.transform(grid))):
    Z = model.predict(g).reshape(A.shape)
    fig.add_trace(go.Heatmap(x=ages, y=sal, z=Z, colorscale=[[0, "#dce6f2"], [1, "#fde3c8"]], showscale=False,
                             hoverinfo="skip"), 1, col)
    for lab, c, name in ((0, BLUE, "did not buy"), (1, ORANGE, "bought")):
        m = y_test == lab
        fig.add_trace(go.Scatter(x=X_test.Age[m], y=X_test.EstimatedSalary[m], mode="markers", name=name,
                                 marker=dict(color=c, size=9, line=dict(color="white", width=1)),
                                 showlegend=col == 1), 1, col)
fig.update_xaxes(title="Age", range=[17, 61])
fig.update_yaxes(range=[10000, 155000])
fig.update_yaxes(title="Estimated salary", col=1)
fig.update_layout(template="simple_white", width=1200, height=560, font=dict(family="Latin Modern Roman", size=22),
                  margin=dict(l=90, r=20, t=70, b=70), legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
fig.update_annotations(font_size=24)
fig.write_image(HERE / "knn_regions.png", scale=1.5)
print(acc_raw, acc_scl)
