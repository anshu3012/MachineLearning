"""Ridge by batch gradient descent on the diabetes data: test R² and distance from the exact answer per epoch (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=4)
alpha, lr = 0.001, 0.005
Xb = np.insert(Xtr, 0, 1, axis=1)
A, c = Xb.T @ Xb, Xb.T @ ytr
I = np.identity(A.shape[0]); I[0, 0] = 0
exact = Ridge(alpha=alpha, solver="cholesky").fit(Xtr, ytr)
w_exact = np.r_[exact.intercept_, exact.coef_]
r2_exact = exact.score(Xte, yte)

w = np.r_[0.0, np.ones(X.shape[1])]
marks = set(np.unique(np.logspace(0, 6, 300).astype(int))) | {10, 100, 500, 5000, 50000, 10**6}
ep, r2, dist = [], [], []
for e in range(1, 10**6 + 1):
    w -= lr * (A @ w - c + alpha * I @ w)
    if e in marks:
        ep.append(e); r2.append(r2_score(yte, Xte @ w[1:] + w[0])); dist.append(np.abs(w - w_exact).max())
for e in (10, 100, 500, 5000, 50000, 10**6):
    i = ep.index(e); print(e, round(r2[i], 4), round(dist[i], 1))
print("exact", r2_exact)

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("Test R² per epoch", "Largest gap from the exact coefficients"))
fig.add_trace(go.Scatter(x=ep, y=r2, mode="lines", line=dict(color="#4C78A8", width=4), name="gradient descent"), 1, 1)
fig.add_trace(go.Scatter(x=[1, 10**6], y=[r2_exact] * 2, mode="lines", line=dict(color="#E45756", width=3, dash="dash"),
                         name=f"exact answer (R² {r2_exact:.3f})"), 1, 1)
i500 = ep.index(500)
fig.add_trace(go.Scatter(x=[500], y=[r2[i500]], mode="markers+text", marker=dict(size=12, color="#F58518"),
                         text=[f"500 epochs: {r2[i500]:.3f}"], textposition="top center", textfont=dict(color="#F58518"),
                         showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=ep, y=dist, mode="lines", line=dict(color="#4C78A8", width=4), showlegend=False), 1, 2)
fig.update_xaxes(type="log", title="epoch", dtick=1, exponentformat="power")
fig.update_yaxes(range=[0, 0.52], title="test R²", row=1, col=1)
fig.update_yaxes(type="log", title="largest gap (log scale)", exponentformat="power", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=460, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(x=0.15, y=0.05), margin=dict(l=70, r=30, t=60, b=60))
fig.write_image(here / "convergence.png", scale=2)
fig.write_image(here / "convergence.pdf")
