"""Empirical against a wrong theoretical probability: the share of the 891 Titanic passengers in each class (0.242,
0.207, 0.551) against "1 out of 3" (0.333), which wrongly assumes the classes are equally likely."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
p = pd.read_csv(here.parent / "data" / "titanic_train.csv").Pclass.value_counts(normalize=True).sort_index()
assert [round(v, 3) for v in p] == [0.242, 0.207, 0.551]
fig = go.Figure()
fig.add_bar(x=[f"class {i}" for i in p.index], y=p.values, marker_color="#4C78A8", name="empirical: share of 891 passengers",
            text=[f"{v:.3f}" for v in p.values], textposition="outside", textfont=dict(size=21))
fig.add_hline(y=1 / 3, line=dict(color="#E45756", dash="dash", width=3))
fig.add_annotation(x=0, y=1 / 3, text="\"1 out of 3\" = 0.333: wrong, the classes are not equally likely", showarrow=False,
                   yshift=16, xanchor="left", xshift=-60, font=dict(size=18, color="#E45756"))
fig.update_layout(template="simple_white", width=1000, height=500, font=dict(family="Latin Modern Roman", size=20),
                  showlegend=False, title=dict(text="P(class) for one passenger drawn at random", x=0.5),
                  yaxis=dict(title="probability", range=[0, 0.65]), margin=dict(l=80, r=30, t=70, b=60))
fig.write_image(here / "titanic_classes.png", scale=2)
fig.write_image(here / "titanic_classes.pdf")
