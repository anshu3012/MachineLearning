"""Choosing k on the breast cancer data: test accuracy (the shortcut) and 5-fold CV accuracy on the training set (Plotly)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
ks = np.arange(1, 16)
test_acc, cv_acc = [], []
for k in ks:
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    cv_acc.append(cross_val_score(model, X_train, y_train, cv=5).mean())
    test_acc.append(model.fit(X_train, y_train).score(X_test, y_test))
print("test", np.round(test_acc, 3)); print("cv  ", np.round(cv_acc, 3))
fig = go.Figure()
fig.add_trace(go.Scatter(x=ks, y=test_acc, mode="lines+markers", line=dict(color="#E45756", width=3), marker=dict(size=9),
                         name="accuracy on the test set (leaks the test set)"))
fig.add_trace(go.Scatter(x=ks, y=cv_acc, mode="lines+markers", line=dict(color="#4C78A8", width=3), marker=dict(size=9),
                         name="5-fold cross-validation accuracy on the training set"))
for arr, col, ax, ay in ((test_acc, "#E45756", 0, -40), (cv_acc, "#4C78A8", -70, 80)):
    b = int(np.argmax(arr))
    fig.add_trace(go.Scatter(x=[ks[b]], y=[arr[b]], mode="markers", showlegend=False,
                             marker=dict(size=18, color=col, symbol="circle-open", line=dict(width=3))))
    fig.add_annotation(x=ks[b], y=arr[b], ax=ax, ay=ay, text=f"best: k = {ks[b]}", font=dict(size=17, color=col),
                       arrowcolor=col, bgcolor="white")
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=17),
                  xaxis=dict(title="k (number of neighbours)", dtick=1), yaxis=dict(title="accuracy", range=[0.93, 1.0]),
                  legend=dict(x=0.35, y=0.08), margin=dict(l=70, r=20, t=30, b=60))
fig.write_image(here / "k_accuracy.png", scale=2); fig.write_image(here / "k_accuracy.pdf")
