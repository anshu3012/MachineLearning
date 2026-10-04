"""Plotly chart for Note ML-032: how often each value of `number` appears, and passengers per cabin deck."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
df = pd.read_csv(here.parent / "data" / "titanic.csv")

number = df["number"].value_counts()
deck = df["Cabin"].str[0].value_counts().sort_index()

fig = make_subplots(1, 2, horizontal_spacing=0.1, column_widths=[0.45, 0.55],
                    subplot_titles=["number: passengers per value", "cabin_cat: passengers per deck"])
fig.add_trace(go.Bar(x=number.index, y=number.values, text=number.values, textposition="outside",
                     marker_color=[ORANGE if v == "A" else BLUE for v in number.index]), 1, 1)
fig.add_trace(go.Bar(x=deck.index, y=deck.values, text=deck.values, textposition="outside",
                     marker_color=ORANGE), 1, 2)
fig.update_yaxes(title="passengers", range=[0, 160], row=1, col=1)
fig.update_yaxes(range=[0, 70], row=1, col=2)
fig.update_xaxes(title="value (A = alone)", type="category", row=1, col=1)
fig.update_xaxes(title="deck letter (687 passengers have no cabin)", row=1, col=2)
fig.update_layout(template="simple_white", width=1200, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=20, t=60, b=70))
fig.update_annotations(font_size=22)
fig.write_image(here / "counts.png", scale=2)
fig.write_image(here / "counts.pdf")
