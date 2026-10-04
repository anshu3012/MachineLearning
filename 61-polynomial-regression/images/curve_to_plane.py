"""The trick of polynomial regression in one picture (Plotly 3D): the 160 training points, plotted against x and the
new feature x^2, lie close to a flat plane, y = 1.92 + 1.04 x + 0.82 x^2. Fitting that plane is ordinary linear
regression; seen from the side (y against x) the plane's edge is the curve."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from data61 import X_test, X_train, y_test, y_train
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
x, y = X_train.ravel(), y_train
F = np.c_[x, x ** 2]
lr = LinearRegression().fit(F, y)
assert np.allclose(np.round([lr.intercept_, *lr.coef_], 2), [1.92, 1.04, 0.82])
assert round(lr.score(np.c_[X_test, X_test ** 2], y_test), 2) == 0.83
g1, g2 = np.meshgrid(np.linspace(-3, 3, 30), np.linspace(0, 9, 30))
fig = go.Figure([go.Surface(x=g1, y=g2, z=lr.intercept_ + lr.coef_[0] * g1 + lr.coef_[1] * g2, opacity=0.55,
                            colorscale=[[0, ORANGE], [1, ORANGE]], showscale=False, name="plane"),
                 go.Scatter3d(x=x, y=x ** 2, z=y, mode="markers", marker=dict(size=4, color=BLUE)),
                 go.Scatter3d(x=np.linspace(-3, 3, 100), y=np.linspace(-3, 3, 100) ** 2,
                              z=lr.intercept_ + lr.coef_[0] * np.linspace(-3, 3, 100) + lr.coef_[1] * np.linspace(-3, 3, 100) ** 2,
                              mode="lines", line=dict(color="black", width=8))])
fig.update_layout(width=950, height=760, font=FONT, showlegend=False,
                  title=dict(text="with the new feature x², the curve lies on a flat plane:<br>ŷ = 1.92 + 1.04 x + 0.82 x²", x=0.5),
                  scene=dict(xaxis_title="x", yaxis_title="x² (new feature)", zaxis_title="y", aspectmode="cube",
                             camera=dict(eye=dict(x=-1.6, y=-1.7, z=0.7)),
                             xaxis=dict(tickfont=dict(size=14)), yaxis=dict(tickfont=dict(size=14)), zaxis=dict(tickfont=dict(size=14))),
                  margin=dict(l=0, r=0, t=90, b=0))
fig.write_image(here / "curve_to_plane.png", scale=2)
