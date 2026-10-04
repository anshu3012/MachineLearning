"""Our normal-equation class on the diabetes data: its coefficients next to scikit-learn's, and predicted vs actual (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
d = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(d.data, d.target, test_size=0.2, random_state=2)
Xb = np.insert(X_train, 0, 1, axis=1)
beta = np.linalg.inv(Xb.T @ Xb) @ Xb.T @ y_train
sk = LinearRegression().fit(X_train, y_train)
pred = np.insert(X_test, 0, 1, axis=1) @ beta
print("R2", round(r2_score(y_test, pred), 4), "max diff", np.abs(beta[1:] - sk.coef_).max())
fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                    subplot_titles=("Coefficients: our class vs scikit-learn", f"Test set: R² = {r2_score(y_test, pred):.2f}"))
fig.add_trace(go.Bar(x=d.feature_names, y=beta[1:], name="our class", marker_color="#4C78A8"), 1, 1)
fig.add_trace(go.Bar(x=d.feature_names, y=sk.coef_, name="scikit-learn", marker_color="#F58518"), 1, 1)
fig.add_trace(go.Scatter(x=y_test, y=pred, mode="markers", marker=dict(size=8, color="#4C78A8", opacity=0.7),
                         showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=[25, 350], y=[25, 350], mode="lines", line=dict(color="#6B6B6B", dash="dash"),
                         showlegend=False), 1, 2)
fig.update_xaxes(title="input column", row=1, col=1)
fig.update_yaxes(title="coefficient", row=1, col=1)
fig.update_xaxes(title="actual disease progression", row=1, col=2)
fig.update_yaxes(title="predicted", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=470, barmode="group",
                  font=dict(family="Latin Modern Roman", size=15), legend=dict(x=0.02, y=0.98),
                  margin=dict(l=70, r=20, t=60, b=60))
fig.update_annotations(font_size=17)
fig.write_image(here / "results.png", scale=2)
fig.write_image(here / "results.pdf")
