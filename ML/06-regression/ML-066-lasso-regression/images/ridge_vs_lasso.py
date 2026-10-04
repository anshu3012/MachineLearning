"""Ridge against Lasso on the diabetes split of the Note (test size 0.2, random state 2) (Plotly). Both use
alpha 0.1 (test R2 0.45 and 0.43); Lasso sets three coefficients to exactly 0 (age, s2,
s4), Ridge (alpha 0.1) keeps all ten non-zero."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import train_test_split
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
X, y = load_diabetes(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=2)
names = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]
la, ri = Lasso(alpha=0.1).fit(Xtr, ytr), Ridge(alpha=0.1).fit(Xtr, ytr)
zero = [names[i] for i in np.flatnonzero(la.coef_ == 0)]
assert zero == ["age", "s2", "s4"] and np.all(ri.coef_ != 0)
assert round(la.score(Xte, yte), 2) == 0.43 and round(ri.score(Xte, yte), 2) == 0.45
fig = go.Figure([go.Bar(x=names, y=ri.coef_, name=f"Ridge, alpha 0.1 (test R² {ri.score(Xte, yte):.2f}): 0 coefficients at 0", marker_color=BLUE),
                 go.Bar(x=names, y=la.coef_, name=f"Lasso, alpha 0.1 (test R² {la.score(Xte, yte):.2f}): 3 coefficients exactly 0", marker_color=ORANGE)])
for n in zero:
    fig.add_annotation(x=n, y=0, text="0", showarrow=False, yshift=-14, xshift=14, font=dict(size=18, color=ORANGE))
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, barmode="group",
                  xaxis=dict(title="feature"), yaxis=dict(title="coefficient"),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=80, r=30, t=20, b=140))
fig.write_image(here / "ridge_vs_lasso.png", scale=2)
