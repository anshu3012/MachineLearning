"""Hypothesis tests for feature selection: scikit-learn's f_classif runs one ANOVA F test per feature of the wine
dataset (178 wines, 13 features, 3 classes). Bars: the F statistic per feature; SelectKBest(k=5) keeps the five
highest (orange). Every p-value here is far below 0.05, so the F score, not the p-value, does the ranking."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.datasets import load_wine
from sklearn.feature_selection import SelectKBest, f_classif

here = Path(__file__).parent
w = load_wine()
F, p = f_classif(w.data, w.target)
kept = SelectKBest(f_classif, k=5).fit(w.data, w.target).get_support()
order = np.argsort(F)[::-1]
assert w.data.shape == (178, 13) and kept.sum() == 5 and set(np.where(kept)[0]) == set(order[:5])
names = np.array(w.feature_names)[order]
fig = go.Figure(go.Bar(x=names, y=F[order], marker_color=np.where(kept[order], "#F58518", "#4C78A8"),
                       text=[f"p = {v:.0e}" for v in p[order]], textposition="outside", textfont=dict(size=12)))
fig.update_layout(template="simple_white", width=1300, height=560, font=dict(family="Latin Modern Roman", size=17),
                  title=dict(text="One ANOVA F test per wine feature: SelectKBest(k = 5) keeps the orange five", x=0.5),
                  xaxis=dict(tickangle=-40), yaxis=dict(title="F statistic (f_classif)", range=[0, F.max() * 1.15]),
                  margin=dict(l=80, r=20, t=70, b=170))
fig.write_image(here / "feature_tests.png", scale=2)
fig.write_image(here / "feature_tests.pdf")
