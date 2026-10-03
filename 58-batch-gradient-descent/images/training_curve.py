"""Batch gradient descent on the diabetes data (learning rate 0.5): R2 on the training and test sets after each epoch,
against the exact OLS values (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
ols = LinearRegression().fit(X_train, y_train)
b, w, lr = 0.0, np.ones(10), 0.5
epochs, tr, te = [], [], []
for e in range(1, 10001):
    err = y_train - (X_train @ w + b)
    b -= lr * (-2 * err.mean())
    w -= lr * (-2 * X_train.T @ err / len(X_train))
    if e in set(np.unique(np.logspace(0, 4, 60).astype(int))):
        epochs.append(e); tr.append(r2_score(y_train, X_train @ w + b)); te.append(r2_score(y_test, X_test @ w + b))
fig = go.Figure()
fig.add_trace(go.Scatter(x=epochs, y=tr, mode="lines", name="training R² (gradient descent)", line=dict(color="#4C78A8", width=4)))
fig.add_trace(go.Scatter(x=epochs, y=te, mode="lines", name="test R² (gradient descent)", line=dict(color="#F58518", width=4)))
for val, colour, name in ((ols.score(X_train, y_train), "#4C78A8", "training R² (OLS)"),
                          (ols.score(X_test, y_test), "#F58518", "test R² (OLS)")):
    fig.add_trace(go.Scatter(x=[1, 10000], y=[val, val], mode="lines", name=name, line=dict(color=colour, dash="dash", width=2)))
i1000 = epochs.index(min(epochs, key=lambda e: abs(e - 1000)))
fig.add_annotation(x=np.log10(epochs[i1000]), y=te[i1000], ax=40, ay=70, text=f"epoch 1000: test R² {te[i1000]:.3f}",
                   font=dict(size=15), arrowcolor="#6B6B6B")
fig.update_layout(template="simple_white", width=950, height=480, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=70, r=30, t=50, b=60),
                  title=dict(text="Batch gradient descent on the diabetes data, learning rate 0.5", x=0.5),
                  xaxis=dict(title="epoch (log scale)", type="log"), yaxis=dict(title="R²", range=[-0.05, 0.6]))
print("final", round(tr[-1], 4), round(te[-1], 4), "ols", round(ols.score(X_train, y_train), 4), round(ols.score(X_test, y_test), 4))
fig.write_image(here / "training_curve.png", scale=2)
fig.write_image(here / "training_curve.pdf")
