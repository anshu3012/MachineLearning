"""The recipe data from train.json: how many dishes of each cuisine (the label we would predict)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
df = pd.read_json(here.parent / "data" / "train.json")
counts = df["cuisine"].value_counts()[::-1]                       # largest on top
fig = go.Figure(go.Bar(x=counts.values, y=counts.index, orientation="h", marker=dict(color="#4C78A8", opacity=0.85),
                       text=[f"{v:,}" for v in counts.values], textposition="outside"))
fig.update_layout(template="simple_white", width=900, height=760, font=dict(family="Latin Modern Roman", size=17),
                  title=dict(text=f"{len(df):,} dishes, {len(counts)} cuisines", x=0.5),
                  xaxis=dict(title="Number of dishes", showgrid=True, range=[0, counts.max() * 1.12]),
                  margin=dict(l=120, r=20, t=70, b=60))
fig.write_image(here / "cuisines.png", scale=2)
fig.write_image(here / "cuisines.pdf")
