"""Multiple linear regression with two inputs: 100 points in 3D and the fitted plane (Plotly).
Data from make_regression with a fixed seed so the numbers repeat."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=2, n_informative=2, noise=50, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
lr = LinearRegression().fit(X_train, y_train)
p = lr.predict(X_test)
print("coef", lr.coef_.round(3), "intercept", round(lr.intercept_, 3))
print("MAE", round(mean_absolute_error(y_test, p), 2), "MSE", round(mean_squared_error(y_test, p), 1),
      "R2", round(r2_score(y_test, p), 3))
g = np.linspace(-3, 3, 20)
G1, G2 = np.meshgrid(g, g)
Z = lr.intercept_ + lr.coef_[0] * G1 + lr.coef_[1] * G2
fig = go.Figure()
fig.add_trace(go.Surface(x=G1, y=G2, z=Z, colorscale=[[0, "#F58518"], [1, "#F58518"]], opacity=0.55, showscale=False))
fig.add_trace(go.Scatter3d(x=X[:, 0], y=X[:, 1], z=y, mode="markers",
                           marker=dict(size=4, color="#4C78A8", line=dict(width=0.5, color="white"))))
fig.update_layout(template="simple_white", width=900, height=620, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=15), margin=dict(l=0, r=0, t=50, b=0), scene_aspectmode="cube",
                  title=dict(text=f"target = {lr.intercept_:.1f} + {lr.coef_[0]:.1f} × feature1 + "
                                  f"{lr.coef_[1]:.1f} × feature2", x=0.5),
                  scene=dict(xaxis_title="feature1", yaxis_title="feature2", zaxis_title="target",
                             camera=dict(eye=dict(x=-1.4, y=-1.7, z=0.9))))
fig.write_image(here / "plane.png", scale=2)
fig.write_image(here / "plane.pdf")
