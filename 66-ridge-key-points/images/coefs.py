"""Diabetes Ridge coefficients: bars at four alphas, and paths for alpha 0 to 2 (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
d = load_diabetes()
names = d.feature_names
Xtr, Xte, ytr, yte = train_test_split(d.data, d.target, test_size=0.2, random_state=2)

alphas = [0, 10, 100, 1000]
fig = make_subplots(rows=2, cols=2, vertical_spacing=0.18, horizontal_spacing=0.1,
                    subplot_titles=[" "] * 4)
for k, a in enumerate(alphas):
    r = Ridge(alpha=a).fit(Xtr, ytr)
    c = r.coef_
    fig.add_trace(go.Bar(x=names, y=c, marker_color=["#E45756" if v < 0 else "#4C78A8" for v in c]), k // 2 + 1, k % 2 + 1)
    fig.layout.annotations[k].text = f"alpha = {a}: largest |coef| {np.abs(c).max():.1f}, test R² {r.score(Xte, yte):.2f}".replace("-", "−")
fig.update_layout(template="simple_white", width=1100, height=700, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=15), margin=dict(l=60, r=30, t=50, b=40))
fig.write_image(here / "bars.png", scale=2)
fig.write_image(here / "bars.pdf")

grid = np.linspace(0, 2, 201)
C = np.array([Ridge(alpha=a).fit(Xtr, ytr).coef_ for a in grid])
fig = go.Figure()
fig.add_trace(go.Scatter(x=[0, 2], y=[0, 0], mode="lines", line=dict(color="black", width=3), showlegend=False))
strong = {"s1": "#E45756", "s5": "#4C78A8", "s2": "#F58518", "age": "#54A24B"}
for j, n in enumerate(names):
    col = strong.get(n, "#BBBBBB")
    fig.add_trace(go.Scatter(x=grid, y=C[:, j], mode="lines", line=dict(color=col, width=4 if n in strong else 2),
                             showlegend=False))
    fig.add_annotation(x=0, y=C[0, j], text=n, showarrow=False, xanchor="right", xshift=-6,
                       font=dict(color=col if n in strong else "#888888", size=14))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=16),
                  margin=dict(l=90, r=30, t=60, b=60),
                  title=dict(text="The largest coefficients (s1, s5, s2) fall fastest; small ones such as age barely move", x=0.5),
                  xaxis=dict(title="alpha", range=[-0.15, 2]), yaxis=dict(title="coefficient"))
fig.write_image(here / "paths.png", scale=2)
fig.write_image(here / "paths.pdf")
