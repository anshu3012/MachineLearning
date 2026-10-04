"""The same alpha means different penalties (Plotly), diabetes data (test size 0.2, random state 4, 353 training
observations). Coefficients of SGDRegressor(penalty="l2", alpha=0.001), run for 50,000 epochs with a constant
learning rate 0.1, against Ridge(alpha=0.353) = 0.001 x 353 and Ridge(alpha=0.001). SGD lands within 3 of the first
and up to about 840 away from the second."""
import warnings
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge, SGDRegressor
from sklearn.model_selection import train_test_split
from gifkit import BLUE, FONT, GREY, ORANGE

warnings.simplefilter("ignore")
here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
Xtr, _, ytr, _ = train_test_split(X, y, test_size=0.2, random_state=4)
sgd = SGDRegressor(penalty="l2", alpha=0.001, max_iter=50_000, tol=None, eta0=0.1, learning_rate="constant",
                   random_state=0).fit(Xtr, ytr)
r1, r2 = Ridge(alpha=0.001 * len(Xtr)).fit(Xtr, ytr), Ridge(alpha=0.001).fit(Xtr, ytr)
assert len(Xtr) == 353 and np.abs(sgd.coef_ - r1.coef_).max() < 3 and 800 < np.abs(sgd.coef_ - r2.coef_).max() < 900
names = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]
fig = go.Figure([go.Bar(x=names, y=r2.coef_, name="Ridge(alpha=0.001)", marker_color=GREY),
                 go.Bar(x=names, y=r1.coef_, name="Ridge(alpha=0.353)", marker_color=BLUE),
                 go.Bar(x=names, y=sgd.coef_, name="SGDRegressor(alpha=0.001)", marker_color=ORANGE)])
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, barmode="group",
                  xaxis=dict(title="feature"), yaxis=dict(title="coefficient"),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=80, r=30, t=20, b=130))
fig.write_image(here / "alpha_scale.png", scale=2)
