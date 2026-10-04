"""Box plot of Titanic fares: a squashed box on the left and a long tail of outliers to the right."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
fare = pd.read_csv(here.parent / "data" / "titanic_train.csv")["Fare"]
q1, q3 = fare.quantile([0.25, 0.75])
n_out = int((fare > q3 + 1.5 * (q3 - q1)).sum())
# pass pandas' own quartiles and Tukey fences (1.5 x IQR), so the plot matches describe() exactly
q1, med, q3 = fare.quantile([0.25, 0.5, 0.75])
iqr = q3 - q1
inside = fare[(fare >= q1 - 1.5 * iqr) & (fare <= q3 + 1.5 * iqr)]
out = fare[(fare < q1 - 1.5 * iqr) | (fare > q3 + 1.5 * iqr)]
fig = go.Figure(go.Box(y=[0], q1=[q1], median=[med], q3=[q3], lowerfence=[inside.min()], upperfence=[inside.max()],
                       orientation="h", line=dict(color="#4C78A8", width=3), fillcolor="rgba(76,120,168,0.18)"))
fig.add_trace(go.Scatter(x=out, y=[0] * len(out), mode="markers",
                         marker=dict(color="#E45756", size=8, opacity=0.6)))
fig.add_annotation(x=fare.max(), y=0, text="3 tickets at 512.33", ax=-40, ay=-70, arrowhead=2, font=dict(size=17))
fig.add_annotation(x=300, y=0.45, text=f"{n_out} outliers above {q3 + 1.5 * (q3 - q1):.1f}", showarrow=False,
                   font=dict(size=17, color="#E45756"))
fig.add_annotation(x=q3, y=0, text="half the fares are below 14.45", ax=60, ay=75, arrowhead=2, font=dict(size=17))
fig.update_xaxes(title="Fare", range=[-10, 540])
fig.update_yaxes(visible=False, range=[-0.6, 0.7])
fig.update_layout(template="simple_white", width=1000, height=340, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=30, r=30, t=20, b=60))
fig.write_image(here / "fare_box.png", scale=2)
fig.write_image(here / "fare_box.pdf")
