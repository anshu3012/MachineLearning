"""Confusion matrices (Plotly): heart disease (logistic regression vs decision tree), iris (3 classes), digits (10 classes)."""
from pathlib import Path
import numpy as np
import pandas as pd
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_digits, load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
warnings.simplefilter("ignore")

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=16)
df = pd.read_csv(here.parent / "data" / "heart.csv")
Xtr, Xte, ytr, yte = train_test_split(df.iloc[:, :-1], df.iloc[:, -1], test_size=0.2, random_state=2)
models = [("Logistic regression", make_pipeline(StandardScaler(), LogisticRegression())),
          ("Decision tree", DecisionTreeClassifier(random_state=1))]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.15, subplot_titles=[" ", " "])
names = [["TN", "FP"], ["FN", "TP"]]
for k, (name, m) in enumerate(models):
    p = m.fit(Xtr, ytr).predict(Xte)
    cm = confusion_matrix(yte, p)
    print(name, accuracy_score(yte, p), cm.tolist())
    good = np.array([[1, 0], [0, 1]])
    fig.add_trace(go.Heatmap(z=good, x=["predicted 0<br>(no disease)", "predicted 1<br>(disease)"],
                             y=["actual 0<br>(no disease)", "actual 1<br>(disease)"],
                             colorscale=[[0, "#F8D3D3"], [1, "#D6ECD2"]], showscale=False, zmin=0, zmax=1,
                             text=[[f"{names[i][j]}<br><b>{cm[i, j]}</b>" for j in range(2)] for i in range(2)],
                             texttemplate="%{text}", textfont=dict(size=22)), 1, k + 1)
    fig.layout.annotations[k].text = f"{name}: accuracy {accuracy_score(yte, p):.3f}"
fig.update_yaxes(autorange="reversed")
fig.update_layout(template="simple_white", width=1100, height=470, font=font, margin=dict(l=110, r=20, t=50, b=60))
fig.write_image(here / "heart.png", scale=2); fig.write_image(here / "heart.pdf")

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, column_widths=[0.38, 0.62], subplot_titles=[" ", " "])
for k, (loader, labels) in enumerate(((load_iris, ["setosa", "versicolor", "virginica"]), (load_digits, [str(i) for i in range(10)]))):
    X, y = loader(return_X_y=True)
    a, b, c, d = train_test_split(X, y, test_size=0.2, random_state=1)
    p = LogisticRegression(max_iter=10000).fit(a, c).predict(b)
    cm = confusion_matrix(d, p)
    print(loader.__name__, accuracy_score(d, p))
    fig.add_trace(go.Heatmap(z=np.log1p(cm), x=labels, y=labels, colorscale="Blues", showscale=False,
                             text=cm, texttemplate="%{text}", textfont=dict(size=16 if k == 0 else 12)), 1, k + 1)
    fig.layout.annotations[k].text = f"{'Iris (3 classes)' if k == 0 else 'Digits (10 classes)'}: accuracy {accuracy_score(d, p):.3f}"
fig.update_yaxes(autorange="reversed", title="actual")
fig.update_xaxes(title="predicted")
fig.update_layout(template="simple_white", width=1150, height=520, font=font, margin=dict(l=90, r=20, t=50, b=60))
fig.write_image(here / "multiclass.png", scale=2); fig.write_image(here / "multiclass.pdf")
