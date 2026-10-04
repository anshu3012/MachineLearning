"""Titanic data: how many values are missing in each column (df.isnull().sum())."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
miss = df.isnull().sum()[::-1]                                   # first column on top
fig = go.Figure(go.Bar(x=miss.values, y=miss.index, orientation="h", marker=dict(color="#E45756", opacity=0.85),
                       text=[f"{m} ({m / len(df):.0%})" if m else "0" for m in miss.values], textposition="outside",
                       cliponaxis=False))
fig.update_layout(template="simple_white", width=900, height=620, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="Missing values per column", x=0.5),
                  xaxis=dict(title="Missing values (out of 891 rows)", range=[0, 891], tickvals=[0, 200, 400, 600, 800], showgrid=True),
                  margin=dict(l=120, r=40, t=70, b=70))
fig.write_image(here / "missing_values.png", scale=2)
fig.write_image(here / "missing_values.pdf")
