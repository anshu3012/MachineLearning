"""Tidy data: the Titanic Name column packs surname, title and given names into one cell. Splitting gives one atomic
value per cell. First four passengers."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
n = pd.read_csv(here.parent / "data" / "titanic.csv").Name.head(4)
sur = n.str.split(",").str[0]
title = n.str.split(", ").str[1].str.split(".").str[0]
rest = n.str.split(". ", n=1, regex=False).str[1]
assert title.tolist() == ["Mr", "Mrs", "Miss", "Mrs"] and rest[0] == "Owen Harris"
fig = make_subplots(rows=1, cols=2, column_widths=[0.42, 0.58], specs=[[{"type": "table"}] * 2], horizontal_spacing=0.03,
                    subplot_titles=["not tidy: three facts in one cell", "tidy: one fact per cell"])
fig.add_trace(go.Table(header=dict(values=["Name"], fill_color="#E45756", font=dict(color="white", size=17), height=36),
                       cells=dict(values=[n], font=dict(size=15), height=34, align="left")), row=1, col=1)
fig.add_trace(go.Table(columnwidth=[0.8, 0.5, 1.6],
                       header=dict(values=["Surname", "Title", "Given names"], fill_color="#54A24B", font=dict(color="white", size=17), height=36),
                       cells=dict(values=[sur, title, rest], font=dict(size=15), height=34, align="left")), row=1, col=2)
for a in fig.layout.annotations:
    a.font.size = 19
fig.update_layout(width=1200, height=300, font=dict(family="Latin Modern Roman", size=16), margin=dict(l=10, r=10, t=50, b=0))
fig.write_image(here / "tidy_names.png", scale=2)
fig.write_image(here / "tidy_names.pdf")
