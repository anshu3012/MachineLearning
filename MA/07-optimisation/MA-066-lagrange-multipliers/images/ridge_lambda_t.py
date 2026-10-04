"""Ridge as a constrained problem, on the diabetes data (10 standardised features, all 442 patients) (Plotly).
For each penalty strength lambda, Ridge's weights w satisfy the constraint ||w||^2 <= t with t = ||w||^2: each lambda
matches one circle size t. Small circles need large multipliers; once t reaches the OLS weights' size, the
constraint is inactive and lambda = 0."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
X = StandardScaler().fit_transform(X)
lams = np.logspace(-2, 5, 60)
ts = np.array([np.sum(Ridge(alpha=l).fit(X, y).coef_ ** 2) for l in lams])
t_ols = np.sum(LinearRegression().fit(X, y).coef_ ** 2)
assert np.all(np.diff(ts) < 0) and ts[0] < t_ols and ts[0] > 0.99 * t_ols
fig = go.Figure(go.Scatter(x=ts, y=lams, mode="lines+markers", line=dict(color=BLUE, width=4), marker=dict(size=6),
                           name="Ridge solution for each λ"))
fig.add_vline(x=t_ols, line=dict(color=RED, width=3, dash="dash"), opacity=1)
fig.add_annotation(x=np.log10(t_ols), y=4, xref="x", yref="y", text=f"OLS weights: ‖w‖² = {t_ols:,.0f}<br>larger t: inactive, λ = 0",
                   showarrow=False, xanchor="right", xshift=-8, font=dict(size=18, color=RED))
fig.update_layout(template="simple_white", width=950, height=580, font=FONT,
                  xaxis=dict(title="circle size t = ‖w‖² (log scale)", type="log", exponentformat="power"),
                  yaxis=dict(title="multiplier λ (Ridge alpha), log scale", type="log", exponentformat="power"),
                  legend=dict(x=0.6, y=0.98), margin=dict(l=90, r=30, t=20, b=70))
fig.write_image(here / "ridge_lambda_t.png", scale=2)
