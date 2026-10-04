"""Three almost identical inputs plus three pure-noise inputs: coefficients from four models (Plotly)."""
from pathlib import Path
import numpy as np
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
warnings.simplefilter("ignore")

here = Path(__file__).parent
rng = np.random.default_rng(0)
n = 200
z = rng.standard_normal(n)
X = np.c_[z + 0.05 * rng.standard_normal(n), z + 0.05 * rng.standard_normal(n), z + 0.05 * rng.standard_normal(n),
          rng.standard_normal((n, 3))]
y = 3 * z + rng.standard_normal(n)
names = ["x1", "x2", "x3", "noise1", "noise2", "noise3"]
models = [("Linear regression", LinearRegression()), ("Ridge (alpha 10)", Ridge(alpha=10)),
          ("Lasso (alpha 0.1)", Lasso(alpha=0.1)), ("Elastic Net (alpha 0.1, l1_ratio 0.5)", ElasticNet(alpha=0.1, l1_ratio=0.5))]
fig = make_subplots(rows=1, cols=4, shared_yaxes=True, horizontal_spacing=0.03, subplot_titles=[m[0] for m in models])
for k, (name, m) in enumerate(models):
    c = m.fit(X, y).coef_
    print(name, c.round(2))
    fig.add_trace(go.Bar(x=names, y=c, marker_color=["#4C78A8"] * 3 + ["#BBBBBB"] * 3,
                         text=[f"{v:.2f}".replace("-", "−") for v in c], textposition="outside", textfont=dict(size=12)), 1, k + 1)
fig.update_yaxes(range=[-1.4, 2.6])
fig.update_yaxes(title="coefficient", row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=460, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=15), margin=dict(l=70, r=20, t=50, b=50))
for a in fig.layout.annotations:
    a.font.size = 15
fig.write_image(here / "grouping.png", scale=2)
fig.write_image(here / "grouping.pdf")
