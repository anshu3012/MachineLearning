"""Reading the coefficients: slices of the fitted plane at feature2 = -1, 0, 1 are parallel lines of slope beta1;
neighbouring slices sit beta2 apart (Plotly). Same model as plane.py."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=2, n_informative=2, noise=50, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
lr = LinearRegression().fit(X_train, y_train)
b0, (b1, b2) = lr.intercept_, lr.coef_
f = lambda x1, x2: b0 + b1 * x1 + b2 * x2
xs = np.array([-2.0, 2.0])
fig = go.Figure()
for x2, c in ((-1, "#9ECAE9"), (0, "#4C78A8"), (1, "#1F3B5C")):
    fig.add_trace(go.Scatter(x=xs, y=f(xs, x2), mode="lines", line=dict(color=c, width=4), name=f"feature2 = {x2}"))
# slope triangle on the feature2 = 0 line: one step right, beta1 up
fig.add_trace(go.Scatter(x=[0, 1, 1], y=[f(0, 0), f(0, 0), f(1, 0)], mode="lines", line=dict(color="#F58518", width=3, dash="dot"), showlegend=False))
fig.add_annotation(x=0.75, y=f(0, 0) - 25, text="+1 in feature1", showarrow=False, font=dict(size=18, color="#F58518"))
fig.add_annotation(x=1.04, y=f(0.5, 0), text=f"+{b1:.1f}", xanchor="left", showarrow=False, font=dict(size=20, color="#F58518"))
# gap between slices: beta2
fig.add_annotation(x=-1.5, y=f(-1.5, 1), ax=-1.5, ay=f(-1.5, 0), xref="x", yref="y", axref="x", ayref="y",
                   arrowhead=3, arrowwidth=3, arrowcolor="#E45756")
fig.add_annotation(x=-1.9, y=f(-1.5, 1) + 45, text=f"+1 in feature2: +{b2:.1f}", xanchor="left", showarrow=False,
                   font=dict(size=18, color="#E45756"))
fig.update_layout(template="simple_white", width=900, height=520, legend=dict(x=0.66, y=0.04, traceorder="reversed"),
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=30, t=30, b=60),
                  xaxis=dict(title="feature1", range=[-2, 2], dtick=1), yaxis=dict(title="predicted target"))
fig.write_image(here / "coef_slices.png", scale=2)
fig.write_image(here / "coef_slices.pdf")
