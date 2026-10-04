"""Titanic: correlation of each numeric column with Survived (df.corr(numeric_only=True))."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
r = df.corr(numeric_only=True)["Survived"].drop("Survived").sort_values()
fig = go.Figure(go.Bar(x=r.values, y=r.index, orientation="h", opacity=0.85,
                       marker=dict(color=["#54A24B" if v > 0 else "#E45756" for v in r.values]),
                       text=[f"{v:+.2f}".replace("-", "−") for v in r.values], textposition="outside",
                       textfont=dict(color="black"), cliponaxis=False))
fig.update_layout(template="simple_white", width=900, height=520, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="Which numeric columns move with survival?", x=0.5),
                  xaxis=dict(title="Correlation with Survived", range=[-0.48, 0.38], tickvals=[-0.4, -0.2, 0, 0.2, 0.4],
                             showgrid=True, zeroline=True, zerolinecolor="black"),
                  margin=dict(l=120, r=20, t=70, b=70))
fig.write_image(here / "corr_survived.png", scale=2)
fig.write_image(here / "corr_survived.pdf")
