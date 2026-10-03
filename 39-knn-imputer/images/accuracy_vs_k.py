"""Plotly chart for Note 39: test accuracy of logistic regression after KNN imputation of Age, for k = 1..10."""
import warnings
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")   # lbfgs convergence warnings on unscaled Fare, as in the Notebook
here = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"

df = pd.read_csv(here.parent / "data" / "titanic_knn.csv")
X_train, X_test, y_train, y_test = train_test_split(df.drop(columns="Survived"), df["Survived"],
                                                    test_size=0.2, random_state=2)


def accuracy(imputer):
    model = LogisticRegression().fit(imputer.fit_transform(X_train), y_train)
    return accuracy_score(y_test, model.predict(imputer.transform(X_test)))


ks = list(range(1, 11))
fig = go.Figure()
for w, colour, dash in [("uniform", BLUE, "solid"), ("distance", ORANGE, "dash")]:
    fig.add_trace(go.Scatter(x=ks, y=[accuracy(KNNImputer(n_neighbors=k, weights=w)) for k in ks], name=f"KNN, {w}",
                             mode="lines+markers", line=dict(color=colour, width=3, dash=dash), marker_size=9))
mean_acc = accuracy(SimpleImputer())
fig.add_hline(y=mean_acc, line=dict(color=GREY, width=2, dash="dot"))
fig.add_annotation(x=10, y=mean_acc, text=f"mean imputation {mean_acc:.3f}", showarrow=False, yshift=-16,
                   xanchor="right", font=dict(color=GREY, size=18))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=80, r=20, t=30, b=70), legend=dict(x=0.98, xanchor="right", y=0.98),
                  xaxis=dict(title="n_neighbors (k)", dtick=1), yaxis=dict(title="test accuracy", range=[0.685, 0.725]))
fig.write_image(here / "accuracy_vs_k.png", scale=2)
fig.write_image(here / "accuracy_vs_k.pdf")
