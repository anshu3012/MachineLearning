"""SGDRegressor on the diabetes data (split random_state 2, max_iter 100, random_state 0), as in the Notebook
(Plotly). Test R2 for the shrinking "invscaling" schedule at four starting rates eta0, against the constant rate
0.01 and OLS. The schedule needs a larger start: 0.16 at eta0 = 0.01, 0.45 at eta0 = 0.2."""
import warnings
from pathlib import Path
import plotly.graph_objects as go
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.model_selection import train_test_split
from gifkit import BLUE, FONT, GREEN, GREY

here = Path(__file__).parent
warnings.simplefilter("ignore")
X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
ols = LinearRegression().fit(X_train, y_train).score(X_test, y_test)
const = SGDRegressor(max_iter=100, learning_rate="constant", eta0=0.01, random_state=0).fit(X_train, y_train)
etas = [0.01, 0.05, 0.1, 0.2]
inv = [SGDRegressor(max_iter=100, learning_rate="invscaling", eta0=e, random_state=0).fit(X_train, y_train) for e in etas]
r2 = [r.score(X_test, y_test) for r in inv]
assert [round(v, 2) for v in r2] == [0.16, 0.38, 0.43, 0.45] and round(const.score(X_test, y_test), 2) == 0.43
assert const.n_iter_ == 97 and inv[-1].n_iter_ == 75
fig = go.Figure()
fig.add_bar(x=[f"η₀ = {e}" for e in etas], y=r2, marker_color=BLUE, name='"invscaling": η₀ / t^0.25',
            text=[f"{v:.2f}" for v in r2], textposition="outside", textfont=dict(size=22))
fig.add_hline(y=const.score(X_test, y_test), line=dict(color=GREEN, width=3, dash="dash"), opacity=1)
fig.add_hline(y=ols, line=dict(color=GREY, width=3, dash="dot"), opacity=1)
fig.add_annotation(x=-0.45, y=const.score(X_test, y_test), xanchor="left", yshift=-16, showarrow=False,
                   text='"constant", η₀ = 0.01: 0.43', font=dict(size=19, color=GREEN))
fig.add_annotation(x=-0.45, y=ols, xanchor="left", yshift=14, showarrow=False, text=f"OLS: {ols:.2f}",
                   font=dict(size=19, color=GREY))
fig.update_layout(template="simple_white", width=1000, height=540, font=FONT, showlegend=True,
                  xaxis=dict(title="starting learning rate of the shrinking schedule"),
                  yaxis=dict(title="test R² after at most 100 epochs", range=[0, 0.55]),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=80, r=30, t=20, b=70))
fig.write_image(here / "sgd_eta0.png", scale=2)
