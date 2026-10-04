"""Rule 1 of section 5 as a picture (Plotly): bagging (bootstrap=True) against pasting (bootstrap=False) on 100 noisy
sine datasets, everything else equal (notebook's last cell): mean correlation between trees, variance and squared
bias of the ensemble."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
rng = np.random.default_rng(0)
x_line = np.linspace(0, 6, 400)[:, None]
truth = np.sin(x_line.ravel())
sets = []
for _ in range(100):
    x = rng.uniform(0, 6, 60)
    sets.append((x[:, None], np.sin(x) + rng.normal(0, 0.4, 60)))
res = {}
for bootstrap in (True, False):
    preds, corrs = [], []
    for Xs, ys in sets:
        m = BaggingRegressor(DecisionTreeRegressor(), n_estimators=100, max_samples=0.5,
                             bootstrap=bootstrap, random_state=0).fit(Xs, ys)
        preds.append(m.predict(x_line))
        trees = np.array([e.predict(x_line) for e in m.estimators_])
        corrs.append(np.corrcoef(trees)[np.triu_indices(100, 1)].mean())
    P = np.array(preds)
    res[bootstrap] = (np.mean(corrs), P.var(0).mean(), ((P.mean(0) - truth) ** 2).mean())
print(res)
b, p = res[True], res[False]
assert (round(b[0], 2), round(p[0], 2), round(b[1], 3), round(p[1], 3), round(b[2], 4), round(p[2], 4)) == \
    (0.82, 0.84, 0.041, 0.055, 0.0019, 0.0013)                                     # section 5, rule 1
titles = ("correlation between trees", "variance of the ensemble", "squared bias")
fig = make_subplots(1, 3, horizontal_spacing=0.1, subplot_titles=titles)
fmt = (".2f", ".3f", ".4f")
for j in range(3):
    fig.add_trace(go.Bar(x=["bagging", "pasting"], y=[b[j], p[j]], marker_color=["#4C78A8", "#F58518"],
                         text=[f"{b[j]:{fmt[j]}}", f"{p[j]:{fmt[j]}}"], textposition="outside", showlegend=False), 1, j + 1)
    fig.update_yaxes(range=[0, max(b[j], p[j]) * 1.25], showticklabels=False, row=1, col=j + 1)
fig.update_annotations(font_size=22)
fig.update_layout(template="simple_white", width=1150, height=480, font=dict(family="Latin Modern Roman", size=22),
                  margin=dict(l=30, r=20, t=60, b=50), bargap=0.3)
fig.write_image(HERE / "bag_vs_paste.png", scale=2); fig.write_image(HERE / "bag_vs_paste.pdf")
