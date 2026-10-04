"""Useless features (Plotly): the diabetes data (test size 0.2, random state 2) with 10 extra columns of pure random
noise, on the same scale as the real ones (seed 0). Ridge (alpha 0.1) keeps every noise coefficient non-zero; Lasso
(alpha 0.3) sets all 10 to exactly 0 and keeps 4 real features. Over 100 different noise draws Lasso zeroes 9.65 of
the 10 noise columns on average and Ridge none."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
d = load_diabetes()
X, y = d.data, d.target


def fit(seed):
    Z = np.random.default_rng(seed).normal(0, X.std(), (len(y), 10))
    a, b, ya, yb = train_test_split(np.c_[X, Z], y, test_size=0.2, random_state=2)
    return [(m.fit(a, ya).coef_, m.score(b, yb)) for m in (LinearRegression(), Ridge(alpha=0.1), Lasso(alpha=0.3))]


(_, r_ols), (c_r, r_r), (c_l, r_l) = fit(0)
kept = [d.feature_names[i] for i in range(10) if c_l[i] != 0]
runs = [fit(s) for s in range(100)]
mean_l = np.mean([(r[2][0][10:] == 0).sum() for r in runs])
mean_r = np.mean([(r[1][0][10:] == 0).sum() for r in runs])
assert (c_l[10:] == 0).all() and (c_r[10:] != 0).all() and kept == ["bmi", "bp", "s3", "s5"], kept
assert (round(mean_l, 2), mean_r) == (9.65, 0) and [round(v, 3) for v in (r_ols, r_r, r_l)] == [0.376, 0.403, 0.405], (mean_l, r_ols, r_r, r_l)
names = d.feature_names + [f"noise {i}" for i in range(1, 11)]
fig = go.Figure([go.Bar(x=names, y=c_r, name=f"Ridge, alpha 0.1 (test R² {r_r:.2f})", marker_color=BLUE),
                 go.Bar(x=names, y=c_l, name=f"Lasso, alpha 0.3 (test R² {r_l:.2f})", marker_color=ORANGE)])
fig.add_vrect(x0=9.5, x1=19.5, fillcolor="grey", opacity=0.12, line_width=0)
fig.add_annotation(x=14.5, y=430, text="10 useless features: random noise<br>Lasso: all exactly 0", showarrow=False,
                   font=dict(size=22))
fig.add_annotation(x=4.5, y=-330, text="10 real features", showarrow=False, font=dict(size=22))
fig.update_layout(template="simple_white", width=1100, height=600, font=FONT, barmode="group",
                  yaxis=dict(title="coefficient", range=[-400, 560]), xaxis=dict(tickangle=-45),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=80, r=20, t=20, b=110))
fig.write_image(here / "useless.png", scale=2)
