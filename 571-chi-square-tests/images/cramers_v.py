"""Chi-square grows with the sample, Cramer's V does not (Plotly). Left: the Titanic sex-by-survival pattern at a
tenth, the actual and ten times the 891 passengers: chi-square 26.3, 263.1, 2631 (no Yates correction), while
V stays 0.54. Right: V for sex (0.54) and class (0.34) against survival."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
t = pd.read_csv(here.parent / "data" / "titanic_train.csv")
sex = pd.crosstab(t.Sex, t.Survived).to_numpy()
cls = pd.crosstab(t.Pclass, t.Survived).to_numpy()
V = lambda tab: np.sqrt(stats.chi2_contingency(tab, correction=False).statistic / (tab.sum() * (min(tab.shape) - 1)))
chis = [stats.chi2_contingency(sex * f, correction=False).statistic for f in (0.1, 1, 10)]
vs = [V(sex * f) for f in (0.1, 1, 10)]
assert round(chis[1], 1) == 263.1 and np.allclose(vs, vs[1]) and round(vs[1], 2) == 0.54 and round(V(cls), 2) == 0.34
fig = make_subplots(1, 2, column_widths=[0.6, 0.4], horizontal_spacing=0.14,
                    subplot_titles=["same pattern, more passengers", "strength of each relationship"])
fig.update_annotations(font_size=22)
labels = ["89 passengers", "891 (actual)", "8,910 passengers"]
fig.add_trace(go.Bar(x=labels, y=chis, marker_color=BLUE,
                     text=[f"χ² = {c:.1f}<br><span style='color:{ORANGE}'>V = {v:.2f}</span>" for c, v in zip(chis, vs)],
                     textposition="outside", textfont=dict(size=19)), 1, 1)
fig.add_trace(go.Bar(x=["sex", "class"], y=[vs[1], V(cls)], marker_color=[ORANGE, ORANGE],
                     text=[f"V = {vs[1]:.2f}", f"V = {V(cls):.2f}"], textposition="outside", textfont=dict(size=20)), 1, 2)
fig.update_yaxes(type="log", title="χ² (log scale)", range=[0.5, 4.3], row=1, col=1)
fig.update_yaxes(title="Cramér's V", range=[0, 1], row=1, col=2)
fig.update_layout(template="simple_white", width=1250, height=540, font=FONT,
                  showlegend=False, margin=dict(l=80, r=30, t=60, b=70))
fig.write_image(here / "cramers_v.png", scale=2)
