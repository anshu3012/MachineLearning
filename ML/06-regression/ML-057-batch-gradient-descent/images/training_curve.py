"""Batch gradient descent (from zero coefficients, learning rate 0.04) on the diabetes data, 200 training observations,
averaged over 50 random train/test splits: training and test R2 after each epoch, against OLS (Plotly).
Left: the 10 original features. Right: 65 features (the 10 plus their squares and pairwise products)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
designs = {"10 features, 200 training observations": X,
           "65 features, 200 training observations": PolynomialFeatures(2, include_bias=False).fit_transform(X)}
EPOCHS, LR, SPLITS = 2000, 0.04, 50
keep = np.unique(np.logspace(0, np.log10(EPOCHS), 70).astype(int)) - 1     # epochs to plot (0-based)

fig = make_subplots(rows=1, cols=2, subplot_titles=list(designs), horizontal_spacing=0.08)
for col, (name, Xd) in enumerate(designs.items(), start=1):
    tr, te, ols_te, ols_tr = np.zeros(EPOCHS), np.zeros(EPOCHS), [], []
    for s in range(SPLITS):
        Xa, Xb, ya, yb = train_test_split(Xd, y, train_size=200, random_state=s)
        sc = StandardScaler().fit(Xa); Xa, Xb = sc.transform(Xa), sc.transform(Xb)
        ols = LinearRegression().fit(Xa, ya)
        ols_tr.append(ols.score(Xa, ya)); ols_te.append(ols.score(Xb, yb))
        w, b = np.zeros(Xa.shape[1]), 0.0
        for e in range(EPOCHS):
            err = ya - (Xa @ w + b)
            b -= LR * (-2 * err.mean()); w -= LR * (-2 * Xa.T @ err / len(Xa))
            tr[e] += 1 - np.mean((ya - (Xa @ w + b)) ** 2) / np.var(ya)
            te[e] += 1 - np.mean((yb - (Xb @ w + b)) ** 2) / np.var(yb)
    tr, te = tr / SPLITS, te / SPLITS
    ep = keep + 1
    show = col == 1
    fig.add_trace(go.Scatter(x=ep, y=tr[keep], mode="lines", name="training R² (gradient descent)", showlegend=show,
                             line=dict(color="#4C78A8", width=4)), row=1, col=col)
    fig.add_trace(go.Scatter(x=ep, y=te[keep], mode="lines", name="test R² (gradient descent)", showlegend=show,
                             line=dict(color="#F58518", width=4)), row=1, col=col)
    fig.add_trace(go.Scatter(x=[1, EPOCHS], y=[np.mean(ols_te)] * 2, mode="lines", name="test R² (OLS)", showlegend=show,
                             line=dict(color="#F58518", dash="dash", width=2)), row=1, col=col)
    best = te.argmax()
    fig.add_annotation(x=np.log10(best + 1), y=te[best], ax=70, ay=-45, text=f"best: {te[best]:.3f} at epoch {best + 1}",
                       font=dict(size=14), arrowcolor="#6B6B6B", row=1, col=col)
    print(name, "best test", round(te[best], 3), "epoch", best + 1, "final test", round(te[-1], 3),
          "OLS test", round(np.mean(ols_te), 3), "OLS train", round(np.mean(ols_tr), 3), "final train", round(tr[-1], 3))
fig.update_xaxes(title="epoch (log scale)", type="log")
fig.update_yaxes(title="R² (average of 50 splits)", range=[-0.05, 0.85], col=1)
fig.update_yaxes(range=[-0.05, 0.85], col=2)
fig.update_layout(template="simple_white", width=1100, height=500, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=70, r=30, t=60, b=110))
fig.write_image(here / "training_curve.png", scale=2)
fig.write_image(here / "training_curve.pdf")
