"""More figures for Note 55 (diabetes data, Plotly):
feature_corr: correlations between the 10 features (Section 2), s1 and s2 at 0.895;
r2_variance: R^2 = 1 - SS_res / SS_tot on the 89 test patients (Section 3);
lstsq_accuracy: coefficient error of inv, solve and lstsq on a design with a near-copy column (Section 6),
the same experiment as the Notebook's last cell."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
d = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(d.data, d.target, test_size=0.2, random_state=2)
names = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]


def save(fig, name, width, height):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False, font=FONT,
                      margin=dict(l=80, r=30, t=70, b=70))
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


# 1. correlation between features, on the training set (as in the Notebook)
C = np.corrcoef(X_train.T)
assert round(C[4, 5], 3) == 0.895
fig = go.Figure(go.Heatmap(z=C[::-1], x=names, y=names[::-1], zmin=-1, zmax=1, colorscale="RdBu", reversescale=True,
                           text=np.round(C[::-1], 2), texttemplate="%{text:.2f}", textfont=dict(size=15),
                           colorbar=dict(title="r")))
fig.add_shape(type="rect", x0=4.5, x1=5.5, y0=4.5, y1=5.5, line=dict(color="black", width=4), fillcolor="rgba(0,0,0,0)", opacity=1)
fig.add_shape(type="rect", x0=3.5, x1=4.5, y0=3.5, y1=4.5, line=dict(color="black", width=4), fillcolor="rgba(0,0,0,0)", opacity=1)
fig.update_xaxes(side="bottom", showline=False, ticks="")
fig.update_yaxes(showline=False, ticks="")
save(fig, "feature_corr", 820, 720)

# 2. R^2 as a share of spread: actual minus mean (total) vs actual minus prediction (residual)
pred = LinearRegression().fit(X_train, y_train).predict(X_test)
tot, res = y_test - y_test.mean(), y_test - pred
ss_tot, ss_res = (tot ** 2).sum(), (res ** 2).sum()
assert np.isclose(1 - ss_res / ss_tot, r2_score(y_test, pred)) and round(1 - ss_res / ss_tot, 2) == 0.44
jit = np.random.default_rng(0).uniform(-0.25, 0.25, len(y_test))
fig = go.Figure()
for row, (v, c, lab) in enumerate([(res, ORANGE, f"actual − prediction<br>sum of squares {ss_res:,.0f}"),
                                   (tot, BLUE, f"actual − mean<br>sum of squares {ss_tot:,.0f}")]):
    fig.add_trace(go.Scatter(x=v, y=row + jit, mode="markers", marker=dict(color=c, size=10, opacity=0.75)))
    fig.add_annotation(x=-235, y=row, xanchor="left", showarrow=False, align="left", text=lab, font=dict(color=c))
fig.add_vline(x=0, line=dict(color=GREY, width=2), opacity=1)
fig.add_annotation(x=0.5, y=1.02, xref="paper", yref="paper", yanchor="bottom", showarrow=False, font=dict(size=22),
                   text=f"R² = 1 − {ss_res:,.0f} / {ss_tot:,.0f} = {1 - ss_res / ss_tot:.2f}")
fig.update_xaxes(title="error on the 89 test patients", range=[-240, 200])
fig.update_yaxes(visible=False, range=[-0.5, 1.5])
save(fig, "r2_variance", 1000, 440)

# 3. inv vs solve vs lstsq when one column is almost a copy of another (Notebook's last cell, same seed)
rng = np.random.default_rng(1)
rows = []
for eps in [1e-3, 1e-5, 1e-7]:
    Z = np.c_[np.ones(200), rng.normal(size=(200, 3))]
    Z = np.c_[Z, Z[:, 1] + eps * rng.normal(size=200)]
    true = np.array([1., 2, 3, 4, 5]); t = Z @ true
    err = lambda b: np.abs(b - true).max()
    rows.append((eps, err(np.linalg.inv(Z.T @ Z) @ Z.T @ t), err(np.linalg.solve(Z.T @ Z, Z.T @ t)),
                 err(np.linalg.lstsq(Z, t, rcond=None)[0])))
print(rows)
_, i7, s7, l7 = rows[2]
assert 0.01 < i7 < 1 and 0.01 < s7 < 1 and l7 < 1e-7 and rows[1][3] < 1e-9
fig = go.Figure()
for j, (lab, c) in enumerate([("inv", RED), ("solve", ORANGE), ("lstsq", GREEN)], start=1):
    fig.add_trace(go.Bar(x=[f"noise {r[0]:.0e}" for r in rows], y=[r[j] for r in rows], name=lab, marker_color=c,
                         text=[f"{r[j]:.0e}" for r in rows], textposition="outside"))
fig.update_layout(barmode="group")
fig.update_yaxes(type="log", title="largest coefficient error", range=[-14, 1], dtick=2, exponentformat="power")
fig.update_xaxes(title="size of the noise that separates the copied column from the original")
save(fig, "lstsq_accuracy", 1000, 520)
fig.update_layout(showlegend=True, legend=dict(orientation="h", x=0, y=1.08))
fig.write_image(here / "lstsq_accuracy.png", scale=2)
fig.write_image(here / "lstsq_accuracy.pdf")
