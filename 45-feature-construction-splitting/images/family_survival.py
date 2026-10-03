"""Plotly chart for Note 45: survival rate by family size, bars coloured by family type."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic.csv")
size = df["SibSp"] + df["Parch"] + 1
rate = df.groupby(size)["Survived"].agg(["mean", "size"])
COLOUR = {"alone": "#4C78A8", "small (2 to 4)": "#54A24B", "large (5 or more)": "#E45756"}
kind = lambda s: "alone" if s == 1 else "small (2 to 4)" if s <= 4 else "large (5 or more)"

fig = go.Figure()
for k, c in COLOUR.items():
    r = rate[[kind(s) == k for s in rate.index]]
    fig.add_trace(go.Bar(x=r.index.astype(str), y=r["mean"], name=k, marker_color=c,
                         text=[f"{m:.0%}<br>n={n}" for m, n in zip(r["mean"], r["size"])],
                         textposition="outside"))
fig.update_layout(template="simple_white", width=1000, height=480, font=dict(family="Latin Modern Roman", size=18),
                  xaxis=dict(title="Family size (SibSp + Parch + 1)", type="category"),
                  yaxis=dict(title="Survival rate", tickformat=".0%", range=[0, 0.92]),
                  legend=dict(title="Family type", x=0.72, y=0.98), margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "family_survival.png", scale=2)
fig.write_image(here / "family_survival.pdf")
