"""When Ridge helps (Plotly): diabetes data, 40 training observations, 200 random splits (seeds 0-199), features
standardised on the training part. Mean test R2 of plain linear regression and of Ridge with alpha chosen by 5-fold
cross-validation on the training part (RidgeCV), with one feature (bmi) and with all 10 features.
Also checked (no figure): one feature with only 3 training observations, alpha by leave-one-out; mean test R2 is
-3.44 for linear regression and -1.79 for Ridge."""
import warnings
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from gifkit import BLUE, FONT, GREY

warnings.simplefilter("ignore")
here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
alphas = np.logspace(-3, 3, 25)
res = {}
for name, cols in (("1 feature (bmi)", [2]), ("10 features", list(range(10)))):
    ols, rid = [], []
    for s in range(200):
        a, b, ya, yb = train_test_split(X[:, cols], y, train_size=40, random_state=s)
        ols.append(make_pipeline(StandardScaler(), LinearRegression()).fit(a, ya).score(b, yb))
        rid.append(make_pipeline(StandardScaler(), RidgeCV(alphas=alphas, cv=5)).fit(a, ya).score(b, yb))
    res[name] = (np.mean(ols), np.mean(rid))
g1 = res["1 feature (bmi)"][1] - res["1 feature (bmi)"][0]
g10 = res["10 features"][1] - res["10 features"][0]
assert round(g1, 2) == -0.01 and round(g10, 2) == 0.10, res
few = [[], []]
for s in range(200):
    a, b, ya, yb = train_test_split(X[:, [2]], y, train_size=3, random_state=s)
    few[0].append(make_pipeline(StandardScaler(), LinearRegression()).fit(a, ya).score(b, yb))
    few[1].append(make_pipeline(StandardScaler(), RidgeCV(alphas=alphas)).fit(a, ya).score(b, yb))
assert (round(np.mean(few[0]), 2), round(np.mean(few[1]), 2)) == (-3.44, -1.79), np.mean(few, axis=1)
names = list(res)
fig = go.Figure([go.Bar(x=names, y=[res[n][0] for n in names], name="linear regression", marker_color=GREY,
                        text=[f"{res[n][0]:.2f}" for n in names], textposition="outside", textfont=dict(size=20)),
                 go.Bar(x=names, y=[res[n][1] for n in names], name="Ridge (alpha by cross-validation)", marker_color=BLUE,
                        text=[f"{res[n][1]:.2f}" for n in names], textposition="outside", textfont=dict(size=20))])
fig.update_layout(template="simple_white", width=900, height=520, font=FONT, barmode="group",
                  yaxis=dict(title="mean test R² (200 splits, 40 training observations)", range=[0, 0.55]),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=90, r=30, t=20, b=60))
fig.write_image(here / "one_vs_many.png", scale=2)
