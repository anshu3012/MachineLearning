"""Out-of-bag observations (Plotly). (a) Share of the 8,000 training observations a tree never draws, against
max_samples: theory (1 - 1/n)^(max_samples * n), and the mean over 500 fitted trees at 0.25 and 1.0.
(b) The out-of-bag score against the real test accuracy for the section 4 model (notebook settings)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
X, y = make_classification(n_samples=10000, n_features=10, n_informative=3, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
n = len(X_train)


def oob_share(bag):
    return np.mean([1 - len(np.unique(s)) / n for s in bag.estimators_samples_])


fit = lambda s: BaggingClassifier(DecisionTreeClassifier(), n_estimators=500, max_samples=s, bootstrap=True,
                                  oob_score=True, random_state=42, n_jobs=-1).fit(X_train, y_train)
bag, full = fit(0.25), fit(1.0)
m25, m100 = oob_share(bag), oob_share(full)
oob, test = bag.oob_score_, bag.score(X_test, y_test)
print(f"OOB share at 0.25: {m25:.3f}, at 1.0: {m100:.3f}; OOB score {oob:.4f}, test {test:.4f}")
assert round(m25, 2) == 0.78 and round(m100, 2) == 0.37 and round(oob, 4) == 0.9429 and round(test, 3) == 0.945
s = np.linspace(0.05, 1.0, 100)
fig = make_subplots(1, 2, column_widths=[0.62, 0.38], horizontal_spacing=0.14,
                    subplot_titles=("(a) share of rows a tree never sees", "(b) out-of-bag score vs test"))
fig.add_trace(go.Scatter(x=s, y=(1 - 1 / n) ** (s * n), mode="lines", line=dict(color="#4C78A8", width=4),
                         name="theory"), 1, 1)
fig.add_trace(go.Scatter(x=[0.25, 1.0], y=[m25, m100], mode="markers+text", marker=dict(size=16, color="#F58518"),
                         text=[f"{m25:.0%}", f"{m100:.0%}"], textposition=["top right", "top center"],
                         name="500 fitted trees"), 1, 1)
fig.add_trace(go.Bar(x=["OOB score", "test accuracy"], y=[oob, test], marker_color=["#F58518", "#54A24B"],
                     text=[f"{oob:.3f}", f"{test:.3f}"], textposition="outside", showlegend=False), 1, 2)
fig.update_xaxes(title="max_samples (share of the 8,000 rows)", row=1, col=1)
fig.update_yaxes(title="share never drawn", range=[0, 1.05], tickformat=".0%", row=1, col=1)
fig.update_yaxes(range=[0.9, 0.96], row=1, col=2)
fig.update_annotations(font_size=22)
fig.update_layout(template="simple_white", width=1200, height=540, font=dict(family="Latin Modern Roman", size=21),
                  legend=dict(x=0.3, y=0.95), margin=dict(l=90, r=20, t=60, b=80))
fig.write_image(HERE / "oob_share.png", scale=2); fig.write_image(HERE / "oob_share.pdf")
