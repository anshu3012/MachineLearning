"""Marble bag of sections 3.1 and 4: empirical shares from 200 draws against the theoretical shares from the bag's
contents (20 red, 15 blue, 15 green of 50). Run: python marbles.py -> marbles.png, marbles.pdf (Plotly)"""
from pathlib import Path
import plotly.graph_objects as go

here = Path(__file__).parent
colours = ["red", "blue", "green"]
emp, theo = [80 / 200, 70 / 200, 50 / 200], [20 / 50, 15 / 50, 15 / 50]
fill = ["#E45756", "#4C78A8", "#54A24B"]
fig = go.Figure()
fig.add_bar(x=colours, y=emp, name="empirical: count / 200 draws", marker_color=fill,
            text=["80/200", "70/200", "50/200"], textposition="outside")
fig.add_bar(x=colours, y=theo, name="theoretical: marbles / 50", marker=dict(color="white", line=dict(color=fill, width=4),
            pattern=dict(shape="/", fgcolor=fill)), text=["20/50", "15/50", "15/50"], textposition="outside")
fig.update_yaxes(range=[0, 0.5], title="probability")
fig.update_layout(template="simple_white", width=900, height=440, barmode="group", bargap=0.3,
                  font=dict(family="Latin Modern Roman", size=22), legend=dict(orientation="h", x=0.5, xanchor="center",
                  y=1.15), margin=dict(l=70, r=20, t=60, b=40))
fig.write_image(here / "marbles.png", scale=2)
fig.write_image(here / "marbles.pdf")
