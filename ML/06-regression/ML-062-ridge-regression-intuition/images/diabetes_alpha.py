"""Diabetes data: coefficient paths (one split) and mean test R2 over 200 splits for two training sizes (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
d = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(d.data, d.target, test_size=0.2, random_state=45)
alphas = np.logspace(-4, 5, 60)
coefs, r2 = [], []
for a in alphas:
    m = Ridge(alpha=a).fit(X_train, y_train); coefs.append(m.coef_); r2.append(m.score(X_test, y_test))
coefs = np.array(coefs)
# Mean test R2 over 200 random splits, small (40) vs full (353) training set.
mean_r2, ols_r2 = {}, {}
for n in (40, 353):
    r, o = np.zeros(len(alphas)), 0.0
    for s in range(200):
        Xa, Xb, ya, yb = train_test_split(d.data, d.target, train_size=n, random_state=s)
        r += [Ridge(alpha=a).fit(Xa, ya).score(Xb, yb) / 200 for a in alphas]
        o += LinearRegression().fit(Xa, ya).score(Xb, yb) / 200
    mean_r2[n], ols_r2[n] = r, o
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=("Each coefficient shrinks towards 0", "Mean test R² (200 splits)"))
pal = ["#4C78A8", "#F58518", "#E45756", "#72B7B2", "#54A24B", "#EECA3B", "#B279A2", "#FF9DA6", "#9D755D", "#BAB0AC"]
for j, name in enumerate(d.feature_names):
    fig.add_trace(go.Scatter(x=alphas, y=coefs[:, j], mode="lines", name=name, line=dict(color=pal[j], width=2.5)), 1, 1)
for n, col in ((40, "#E45756"), (353, "#4C78A8")):
    fig.add_trace(go.Scatter(x=alphas, y=mean_r2[n], mode="lines", line=dict(color=col, width=4), showlegend=False), 1, 2)
    fig.add_trace(go.Scatter(x=[alphas[0], alphas[-1]], y=[ols_r2[n]] * 2, mode="lines",
                             line=dict(color=col, dash="dash", width=1.5), showlegend=False), 1, 2)
    fig.add_annotation(x=np.log10(alphas[0]), y={40: 0.23, 353: 0.53}[n], xref="x2", yref="y2", xanchor="left",
                       text=f"{n} training observations", showarrow=False, font=dict(color=col, size=14))
fig.update_xaxes(type="log", title="α (log scale)", row=1, col=1); fig.update_xaxes(type="log", title="α (log scale)", row=1, col=2)
fig.update_yaxes(title="coefficient", row=1, col=1); fig.update_yaxes(title="test R²", range=[-0.05, 0.6], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=480, font=dict(family="Latin Modern Roman", size=15),
                  margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=16)
for n in (40, 353):
    i = int(np.argmax(mean_r2[n]))
    print(n, "ols", round(ols_r2[n], 3), "best alpha", round(alphas[i], 4), "R2", round(mean_r2[n][i], 3))
fig.write_image(here / "diabetes_alpha.png", scale=2)
fig.write_image(here / "diabetes_alpha.pdf")
