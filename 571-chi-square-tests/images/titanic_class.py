"""Titanic passengers by class and outcome: observed counts against the counts expected if class and survival were
independent (Plotly). First class has far more survivors than expected, third class far fewer."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from gifkit import BLUE, FONT, GREY

here = Path(__file__).parent
titanic = pd.read_csv(here.parent / "data" / "titanic_train.csv")
table = pd.crosstab(titanic["Pclass"], titanic["Survived"])
res = stats.chi2_contingency(table)
expected = res.expected_freq
assert table.loc[1, 1] == 136 and round(expected[0, 1]) == 83 and table.loc[3, 1] == 119 and round(expected[2, 1]) == 188
assert round(res.statistic, 1) == 102.9
fig = make_subplots(1, 2, shared_yaxes=True, horizontal_spacing=0.06, subplot_titles=["died", "survived"])
fig.update_annotations(font_size=22)
classes = [f"class {c}" for c in table.index]
for col, j in ((1, 0), (2, 1)):
    fig.add_trace(go.Bar(x=classes, y=table.iloc[:, j], name="observed", marker_color=BLUE, showlegend=col == 1,
                         text=table.iloc[:, j], textposition="outside", textfont=dict(size=18)), 1, col)
    fig.add_trace(go.Bar(x=classes, y=expected[:, j], name="expected if independent", marker_color=GREY,
                         showlegend=col == 1, text=np.round(expected[:, j]).astype(int), textposition="outside",
                         textfont=dict(size=18)), 1, col)
fig.update_yaxes(title="passengers", range=[0, 420], row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=480, font=FONT, barmode="group",
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12), margin=dict(l=70, r=20, t=60, b=100))
fig.write_image(here / "titanic_class.png", scale=2)
